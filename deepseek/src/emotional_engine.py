# src/emotional_engine.py
import logging
from collections import deque

logger = logging.getLogger(__name__)

class EmotionalEngine:
    """情绪引擎主类（融合文本+音频情绪）"""

    def __init__(self, api_key):
        from .deepseek_client import DeepSeekClient
        from .emotion_analyzer import EmotionAnalyzer
        from .voice_processor import VoiceProcessor
        from .rdk_controller import RDKX5Controller

        self.deepseek_client = DeepSeekClient(api_key)
        self.emotion_analyzer = EmotionAnalyzer()
        self.voice_processor = VoiceProcessor()
        self.rdk_controller = RDKX5Controller()

        self.emotion_history = deque(maxlen=10)
        self.current_emotion = 'neutral'
        logger.info("情绪引擎初始化完成")

    def process_interaction(self, audio_data, transcribed_text):
        """处理音频 + 文本交互"""
        try:
            # 1️⃣ 提取语音特征
            voice_features = self.voice_processor.extract_audio_features(audio_data)
            logger.debug(f"语音特征提取完成: {voice_features}")

            # 2️⃣ 文本情绪分析（DeepSeek）
            emotion_result = self.emotion_analyzer.analyze(transcribed_text)
            logger.debug(f"文本情绪分析结果: {emotion_result}")

            # 3️⃣ 融合音频 + 文本结果
            from .emotion_fusion import fuse_text_and_audio
            fusion_result = fuse_text_and_audio(emotion_result, voice_features)
            logger.info(f"融合后情绪结果: {fusion_result}")

            # 4️⃣ 生成情绪化回复
            response = self._generate_emotional_response(transcribed_text, fusion_result)

            return response, fusion_result

        except Exception as e:
            logger.error(f"交互处理失败: {e}")
            return "抱歉，我遇到了一些问题。", {"primary_emotion": "neutral", "confidence": 0.0}

    def _generate_emotional_response(self, user_input, emotion_result):
        """生成情绪化回复"""
        prompt = f"""
用户情绪：{emotion_result.get('emotion', 'neutral')}
用户输入：{user_input}

请根据用户的情绪状态进行适当的回复。
"""
        messages = [{"role": "user", "content": prompt}]
        response_data = self.deepseek_client.chat_completion(messages)
        return response_data['choices'][0]['message']['content']
