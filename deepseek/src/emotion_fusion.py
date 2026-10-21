# src/emotion_fusion.py
import re
import numpy as np
import logging
logger = logging.getLogger(__name__)
logger.info("✅ emotion_fusion 模块已加载")

def fuse_text_and_audio(text_emotion_result, voice_features):
    logger.info("🎛 正在融合文本与语音情绪特征...")
    # 这里是你自己的融合逻辑
    fused_emotion = text_emotion_result.get("primary_emotion", "neutral")
    confidence = text_emotion_result.get("confidence", 0.8)
    logger.info(f"🎯 融合完成：{fused_emotion}（置信度 {confidence}）")
    return {"primary_emotion": fused_emotion, "confidence": confidence}

def parse_deepseek_text(response_text):
    """解析 DeepSeek 返回的文本，提取情绪类型"""
    m = re.search(r"情绪类型\s*:\s*([^\n\r]+)", response_text)
    emotion = m.group(1).strip() if m else "中性"
    return emotion

def audio_scores_from_features(feats):
    """根据音频特征估算每种情绪分数"""
    vvar = feats.get('volume_variance', 0)
    vmax = feats.get('max_volume', 0)
    pitch_var = feats.get('pitch_variance', 0)
    dur = feats.get('speech_duration', 1.0)

    scores = {
        '愤怒': 0.0,
        '开心': 0.0,
        '中性': 0.0,
        '伤心': 0.0,
        '惊讶': 0.0,
        '恐惧': 0.0
    }

    scores['愤怒'] += 0.6 * vmax + 0.4 * min(vvar / 0.2, 1.0)
    scores['开心'] += 0.4 * min(pitch_var / 20.0, 1.0) + 0.3 * vmax
    scores['中性'] += 0.5 * (1 - min(vvar / 0.05, 1.0)) + 0.3 * max(0, 1 - pitch_var / 10.0)
    scores['伤心'] += 0.5 * (1 - vmax) + 0.4 * (dur > 3.0)
    scores['惊讶'] += 0.6 * min(pitch_var / 15.0, 1.0) + 0.3 * (vmax > 0.8)
    scores['恐惧'] += 0.5 * min(pitch_var / 25.0, 1.0) + 0.4 * (dur < 1.0)

    arr = np.array(list(scores.values()))
    arr = arr / arr.sum() if arr.sum() > 0 else arr
    for i, k in enumerate(scores.keys()):
        scores[k] = float(arr[i])
    return scores

def fuse_text_and_audio(deepseek_text, audio_feats, alpha=0.7):
    """融合 DeepSeek 文本结果和音频特征"""
    text_emotion = parse_deepseek_text(deepseek_text)
    emotions = ['愤怒', '开心', '中性', '伤心', '惊讶', '恐惧']
    text_scores = {k: (1.0 if k == text_emotion else 0.0) for k in emotions}
    audio_scores = audio_scores_from_features(audio_feats)

    fused = {k: alpha * text_scores[k] + (1 - alpha) * audio_scores.get(k, 0.0) for k in emotions}
    total = sum(fused.values()) or 1.0
    for k in fused:
        fused[k] /= total
    best = max(fused.items(), key=lambda x: x[1])
    return {'emotion': best[0], 'confidence': best[1], 'scores': fused}
