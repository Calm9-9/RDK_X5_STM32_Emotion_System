#!/bin/bash
# 等待网络启动
sleep 10
#!/bin/bash
# =======================
# DeepSeek 启动脚本
# =======================

LOG_DIR="/home/sunrise/logs"
PROJECT_DIR="/home/sunrise/deepseek"
PYTHON="/usr/bin/python3"
MAIN="main.py"

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "[$(date)] 启动 DeepSeek 服务..." >> "$LOG_DIR/start.log"

# 等待网络连接
for i in {1..15}; do
    if ping -c 1 -W 1 baidu.com > /dev/null 2>&1; then
        echo "[$(date)] 网络已连接，启动程序。" >> "$LOG_DIR/start.log"
        cd "$PROJECT_DIR" || exit
        $PYTHON "$MAIN" >> "$LOG_DIR/start.log" 2>&1
        exit 0
    else
        echo "[$(date)] 网络未就绪，等待中 ($i/15)..." >> "$LOG_DIR/start.log"
        sleep 2
    fi
done

echo "[$(date)] 网络连接失败，未启动 main.py" >> "$LOG_DIR/start.log"
exit 1
cd /home/sunrise/deepseek
/usr/bin/python3 main.py >> /home/sunrise/logs/start.log 2>&1
