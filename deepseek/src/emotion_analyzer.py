import requests
import json
from config.APIkeys import APIKeys
from utils.logger import setup_logger


class EmotionAnalyzer:
    """基于DeepSeek API的情绪分析器（支持细粒度情绪类型）"""
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.api_key = APIKeys.DEEPSEEK_API_KEY
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self._check_api_key()

    def _check_api_key(self):
        """检查API密钥是否配置"""
        if not self.api_key:
            self.logger.error("DeepSeek API密钥未配置，请检查.env文件")
            raise ValueError("DeepSeek API密钥缺失")

    def analyze(self, text):
        """分析文本情绪，返回指定的6种情绪类型"""
        if not text:
            self.logger.warning("无文本内容可分析")
            return None

        # 构建请求参数（核心修改：调整system prompt指定情绪类型）
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "请严格按照以下要求分析用户输入的情绪：\n"
                               "1. 情绪类型必须从以下选项中选择：恐惧/伤心/中性/开心/惊讶/愤怒\n"
                               "2. 给出简短理由说明判断依据\n"
                               "3. 输出格式固定为：\n"
                               "情绪类型: [选择的情绪类型]\n"
                               "理由: [你的分析]"
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            self.logger.info("开始情绪分析...")
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            # 提取分析结果
            if "choices" in result and len(result["choices"]) > 0:
                analysis = result["choices"][0]["message"]["content"]
                self.logger.info("情绪分析完成")
                return analysis
            else:
                self.logger.error(f"情绪分析失败，API返回异常: {result}")
                return None

        except Exception as e:
            self.logger.error(f"情绪分析请求失败: {str(e)}")
            return None