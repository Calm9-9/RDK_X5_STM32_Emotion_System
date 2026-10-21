import serial
import time

def test_stm32_emotions(port="/dev/ttyS1", baudrate=115200, delay=2):
    """
    循环发送 0~5 的情绪索引到 STM32，测试 LED/马达/语音
    :param port: 串口号
    :param baudrate: 波特率
    :param delay: 每条指令间隔秒数
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"已连接 {port}，开始循环发送情绪指令...")
        
        while True:
            for code in range(6):
                ser.write(bytes([code]))
                print(f"已发送情绪索引: {code}")
                time.sleep(delay)

    except Exception as e:
        print(f"串口打开失败: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("串口已关闭")

if __name__ == "__main__":
    test_stm32_emotions(port="/dev/ttyS1", baudrate=115200, delay=2)
