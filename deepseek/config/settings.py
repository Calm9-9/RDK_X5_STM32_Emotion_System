# 应用配置常量
class Settings:
    # DeepSeek API配置
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL = "deepseek-chat"

    # 语音处理配置
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    MAX_RECORD_SECONDS = 10

    # 情绪分析配置
    EMOTION_UPDATE_INTERVAL = 2.0  # 情绪更新间隔(秒)
    MAX_EMOTION_HISTORY = 10  # 最大情绪历史记录数

    # RDK X5硬件配置
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 480