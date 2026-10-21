# src/baidu_voice.py
from aip import AipSpeech
import wave
import os
from config.APIkeys import APIKeys
from utils.logger import setup_logger


class BaiduVoiceRecognizer:
    def __init__(self):
        self.logger = setup_logger(__name__)
        # 从配置获取百度密钥（确保与.env一致）
        self.APP_ID = APIKeys.BAIDU_APP_ID
        self.API_KEY = APIKeys.BAIDU_APP_KEY
        self.SECRET_KEY = APIKeys.BAIDU_SECRET_KEY

        # 初始化SDK（添加超时配置，避免网络问题）
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.client.setConnectionTimeoutInMillis(5000)  # 连接超时5秒
        self.client.setSocketTimeoutInMillis(10000)  # 读取超时10秒
        self._verify_sdk_config()

    def _verify_sdk_config(self):
        """验证密钥和SDK初始化"""
        if not all([self.APP_ID, self.API_KEY, self.SECRET_KEY]):
            raise ValueError("百度语音SDK配置不完整（AppID/APIKey/SecretKey缺失）")
        if not hasattr(self.client, 'asr'):
            raise RuntimeError("百度语音SDK初始化失败，请检查密钥是否正确")

    def _save_debug_audio(self, audio_data, sample_rate):
        """保存音频用于调试（确认格式）"""
        try:
            with wave.open("debug_audio.wav", "wb") as f:
                f.setnchannels(1)  # 强制单声道
                f.setsampwidth(2)  # 强制16位（2字节）
                f.setframerate(sample_rate)  # 16000Hz
                f.writeframes(audio_data)
            self.logger.info(f"调试音频已保存（大小：{len(audio_data)}字节，采样率：{sample_rate}Hz）")
        except Exception as e:
            self.logger.warning(f"保存调试音频失败: {str(e)}")

    def recognize(self, audio_data, sample_rate=16000):
        """
        核心识别函数：适配最新SDK，添加详细错误日志
        """
        # 1. 先检查音频数据
        if not audio_data or len(audio_data) < 1024:  # 过滤过小的无效音频
            self.logger.error("无效音频数据（长度过短或为空）")
            return None
        self._save_debug_audio(audio_data, sample_rate)

        # 2. 强制验证采样率（百度仅支持8000/16000）
        if sample_rate not in [8000, 16000]:
            self.logger.error(f"不支持的采样率：{sample_rate}Hz，仅支持8000/16000")
            return None

        # 3. 调用百度API（添加详细日志，便于排查）
        try:
            self.logger.debug(f"开始调用百度语音识别（采样率：{sample_rate}Hz，音频长度：{len(audio_data)}字节）")
            options = {"dev_pid": 1537}
            result = self.client.asr(
                speech=audio_data,
                format="pcm",
                rate=sample_rate,
                options=options
            )

            # 4. 解析结果（输出完整错误信息）
            if not result:
                self.logger.error("百度API返回空结果（可能是网络问题）")
                return None
            elif result.get("err_no") == 0:
                text = result["result"][0].strip()
                self.logger.info(f"语音识别成功：{text}")
                return text
            else:
                # 关键：打印完整错误信息（包括err_no和err_msg）
                err_no = result.get("err_no")
                err_msg = result.get("err_msg", "未知错误")
                self.logger.error(f"百度识别失败 [错误码{err_no}]: {err_msg}")
                # 常见错误码提示
                if err_no == 3311:
                    self.logger.error("错误原因：采样率/格式不匹配，或音频损坏")
                elif err_no == 3307:
                    self.logger.error("错误原因：API密钥无效或服务未开通")
                elif err_no == 3309:
                    self.logger.error("错误原因：音频过长（百度限制60秒内）")
                return None

        except Exception as e:
            self.logger.error(f"识别过程异常: {str(e)}（可能是网络或SDK问题）")
            return None