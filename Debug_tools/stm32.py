import serial
import time

# 串口配置
port = "/dev/ttyS1"  # 去掉前面的空格
baudrate = 115200

# 打开串口
try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"已打开串口 {port}, 波特率 {baudrate}")
except Exception as e:
    print(f"无法打开串口: {e}")
    exit()

# 情绪字典
emotion_dict = {0: "FEAR", 1: "SAD", 2: "NEUTRAL", 3: "HAPPY", 4: "SURPRISE", 5: "ANGRY"}

try:
    for code in range(6):
        ser.write(bytes([code]))
        print(f"发送情绪编码 {code} -> {emotion_dict[code]}")

        # 等待 STM32 确认
        start_time = time.time()
        confirmed = False
        while time.time() - start_time < 2:  # 最多等待2秒
            if ser.in_waiting:
                ack = ser.read(1)
                if ack == b'\xAA':
                    confirmed = True
                    print(f"STM32 已确认 {emotion_dict[code]}")
                    break
        if not confirmed:
            print(f"警告: STM32 未确认 {emotion_dict[code]}")

        time.sleep(1)  # 每个动作间隔1秒

except KeyboardInterrupt:
    print("测试中断")

finally:
    ser.close()
    print("串口已关闭")
