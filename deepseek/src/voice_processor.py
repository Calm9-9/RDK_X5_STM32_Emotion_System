import numpy as np
from scipy import signal
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)


class VoiceProcessor:
    def __init__(self):
        self.sample_rate = Settings.SAMPLE_RATE

    def extract_audio_features(self, audio_data):
        """提取音频特征用于情绪分析"""
        features = {}

        # 音量特征
        features['volume_variance'] = np.var(audio_data)
        features['max_volume'] = np.max(np.abs(audio_data))

        # 基频特征
        features.update(self._extract_pitch_features(audio_data))

        # 语速特征（简化版）
        features['speech_duration'] = len(audio_data) / self.sample_rate

        return features

    def _extract_pitch_features(self, audio_data):
        """提取音高相关特征"""
        if len(audio_data) < 100:
            return {'pitch': 0, 'pitch_variance': 0}

        # 简单的自相关基频估计
        correlated = signal.correlate(audio_data, audio_data, mode='full')
        correlated = correlated[len(correlated) // 2:]

        try:
            peaks, properties = signal.find_peaks(correlated[:500], height=0.3)
            return {
                'pitch': len(peaks),
                'pitch_variance': np.var(peaks) if len(peaks) > 0 else 0
            }
        except:
            return {'pitch': 0, 'pitch_variance': 0}