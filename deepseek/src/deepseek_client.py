# src/deepseek_client.py
import requests
import json
import logging

# 使用基本的logging，避免循环导入
logger = logging.getLogger(__name__)


class DeepSeekClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def chat_completion(self, messages, temperature=0.7, max_tokens=2048):
        """DeepSeek聊天补全API"""
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek API请求失败: {e}")
            raise
        except Exception as e:
            logger.error(f"DeepSeek API调用异常: {e}")
            raise