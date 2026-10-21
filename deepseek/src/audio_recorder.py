import pyaudio
import logging

# 配置日志
logger = logging.getLogger(__name__)


def record_audio(duration=5):
    """
    录制音频并返回PCM格式字节数据
    :param duration: 录音时长（秒）
    :return: bytes类型的音频数据，失败返回None
    """
    # 录音参数（严格符合百度API要求）
    CHUNK = 1024
    FORMAT = pyaudio.paInt16  # 16位深度
    CHANNELS = 1  # 单声道
    RATE = 16000  # 16000Hz采样率

    p = pyaudio.PyAudio()

    # 选择麦克风设备ID（根据实际情况修改）
    DEVICE_ID = 1

    try:
        # 打开音频流
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=DEVICE_ID,
            frames_per_buffer=CHUNK
        )

        logger.info(f"使用设备ID {DEVICE_ID} 进行录音")
        print(f"请说话...（{duration}秒内说完，按Ctrl+C可提前结束）")

        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)  # 读取的是bytes类型
            frames.append(data)  # 直接追加bytes，不做数值处理

        logger.info("录音结束")

    except KeyboardInterrupt:
        logger.info("\n录音已提前结束")
    except Exception as e:
        logger.error(f"录音出错: {str(e)}")
        return None
    finally:
        # 确保资源释放
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        p.terminate()

    # 合并音频帧（bytes类型拼接，不是数值相加）
    audio_data = b''.join(frames)
    logger.info(f"录音数据长度: {len(audio_data)} 字节")
    logger.info(f"实际采样率: {RATE} Hz")
    logger.debug(f"录音数据类型: {type(audio_data)}")  # 确认是bytes类型

    return audio_data
