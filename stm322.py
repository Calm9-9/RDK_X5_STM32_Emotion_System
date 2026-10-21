import serial
import time
import random

# 打开串口
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
print("✅ 串口已打开:", ser.portstr)

# 随机选择一个情绪（0~5）
emotion = random.randint(0, 5)
msg = f"{emotion}\n".encode()

# 发送数据
ser.write(msg)
print(f"🎯 已随机发送情绪信号: {emotion}")

# 等待 STM32 处理（至少 200~300ms）
time.sleep(0.3)

# 可选：尝试读取 STM32 回传信息
if ser.in_waiting:
    resp = ser.read(ser.in_waiting)
    print("STM32 回传:", resp.decode(errors='ignore'))

# 关闭串口
ser.close()
print("🔚 已关闭串口")
