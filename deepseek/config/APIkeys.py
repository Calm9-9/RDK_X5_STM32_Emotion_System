# config/APIkeys.py
import os
from dotenv import load_dotenv

# 关键：加载.env文件（路径要正确）
load_dotenv()  # 如果.env在项目根目录，直接用这个
# 如果.env在其他位置，需要指定路径，例如：
# load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

class APIKeys:
    # 从环境变量读取百度密钥（必须与.env中的键名一致）
    BAIDU_APP_ID = os.getenv("BAIDU_APP_ID")
    BAIDU_APP_KEY = os.getenv("BAIDU_APP_KEY")
    BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")
    # 其他密钥（如DeepSeek）
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    @classmethod
    def validate_keys(cls):
        # 验证百度密钥是否存在
        if not cls.BAIDU_APP_KEY or not cls.BAIDU_SECRET_KEY:
            raise ValueError("请在.env中配置BAIDU_APP_KEY和BAIDU_SECRET_KEY")
        # 验证其他密钥
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("请在.env中配置DEEPSEEK_API_KEY")