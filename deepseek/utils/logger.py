import logging
import os
from datetime import datetime


def setup_logger(name):
    """
    配置日志系统
    :param name: 日志名称（通常为模块名__name__）
    :return: 配置好的logger对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 捕获所有级别的日志
    logger.propagate = False  # 防止日志向上传播导致重复输出

    # 如果已有处理器，直接返回
    if logger.handlers:
        return logger

    # 控制台处理器（只输出INFO及以上级别）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 文件处理器（输出所有级别日志，按日期保存）
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # 确保日志目录存在
    log_filename = f"{log_dir}/emotion_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # 日志格式：时间-模块-级别-消息
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
