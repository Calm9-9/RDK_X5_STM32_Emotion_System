import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import time
import pyaudio
import serial
import numpy as np
from scipy import signal
from src.baidu_voice import BaiduVoiceRecognizer
from src.emotion_analyzer import EmotionAnalyzer
from config.APIkeys import APIKeys
from src.emotion_fusion import fuse_text_and_audio
from src.voice_processor import VoiceProcessor


# ---------------------- 日志配置 ----------------------
def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_filename = f"{log_dir}/emotion_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# ---------------------- 音频重采样函数 ----------------------
def resample_audio(audio_data, original_rate, target_rate=16000):
    logger = logging.getLogger(__name__)
    if original_rate == target_rate:
        return audio_data, target_rate

    try:
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        number_of_samples = round(len(audio_np) * float(target_rate) / original_rate)
        resampled = signal.resample(audio_np, number_of_samples)
        resampled_bytes = resampled.astype(np.int16).tobytes()
        logger.info(f"已重采样音频: {original_rate}Hz → {target_rate}Hz")
        return resampled_bytes, target_rate
    except Exception as e:
        logger.error(f"重采样失败: {str(e)}")
        return audio_data, original_rate


# ---------------------- 录音功能 ----------------------
def record_audio(device_id=0,duration=5):
    logger = logging.getLogger(__name__)
    p = pyaudio.PyAudio()

    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_id,
            frames_per_buffer=CHUNK
        )
    except Exception as e:
        logger.error(f"麦克风打开失败: {str(e)}")
        p.terminate()
        return None, RATE

    frames = []
    try:
        logger.info(f"请说话...（{duration}秒内说完）")
        for _ in range(int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
    except Exception as e:
        logger.error(f"录音出错: {str(e)}")
        return None, RATE
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    audio_data = b''.join(frames)
    logger.info(f"录音数据长度: {len(audio_data)} 字节，采样率: {RATE}Hz")
    return audio_data, RATE


# ---------------------- 主程序 ----------------------
def main():
    load_dotenv()
    logger = setup_logger(__name__)

    try:
        APIKeys.validate_keys()
        logger.info("初始化情绪感知引擎...")

        recognizer = BaiduVoiceRecognizer()
        emotion_analyzer = EmotionAnalyzer()
        voice_processor = VoiceProcessor()
        logger.info("情绪感知助手已启动")

        # ---------------------- 初始化串口 ----------------------
        ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        emotion_dict = {
            "恐惧": b'0',
            "伤心": b'1',
            "中性": b'2',
            "开心": b'3',
            "惊讶": b'4',
            "愤怒": b'5'
        }

        # 通知 STM32
        ser.write(b'8')
        logger.info("已通知 STM32:启动成功（振动两次）")
        ser.write(b'9')
        logger.info("已通知 STM32:开始录音（振动一次）")

        # ---------------------- 单次运行 ----------------------
        audio_data, sample_rate = record_audio(device_id=0, duration=5)
        if not audio_data:
            logger.error("录音失败，程序结束")
            return

        if sample_rate != 16000:
            audio_data, sample_rate = resample_audio(audio_data, sample_rate, 16000)

        # ---------------------- 语音识别 ----------------------
        user_input = recognizer.recognize(audio_data, sample_rate)
        if not user_input:
            logger.error("语音识别失败，程序结束")
            return
        logger.info(f"识别结果: {user_input}")

        # ---------------------- 语音特征提取 ----------------------
        voice_features = voice_processor.extract_audio_features(np.frombuffer(audio_data, dtype=np.int16))
        logger.info("🎙 语音特征:")
        for k, v in voice_features.items():
            logger.info(f"  {k}: {v}")

        # ---------------------- 文本情绪分析 ----------------------
        emotion_result = emotion_analyzer.analyze(user_input)
        logger.info(f"文本情绪分析结果: {emotion_result}")

        # ---------------------- 融合文本 + 音频 ----------------------
        fusion_result = fuse_text_and_audio(emotion_result, voice_features)
        key = fusion_result.get("emotion", "中性")
        confidence = fusion_result.get("confidence", 0.0)
        logger.info(f"🎯 融合识别情绪: {key}（置信度 {confidence}）")

        # ---------------------- 发送 STM32 ----------------------
        if key:
            code = emotion_dict.get(key, b'2')
        else:
            key = "中性"
            logger.error("情绪分析失败，使用默认中性")
            code = emotion_dict.get(key, b'2')

        ser.write(code)
        logger.info(f"已发送给 STM32: {code.decode()} ({key})")
        logger.info("本轮结束，程序退出")

    except Exception as e:
        logger.error(f"程序启动失败: {str(e)}")


if __name__ == "__main__":
    main()
