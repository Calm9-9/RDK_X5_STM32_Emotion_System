import serial
import time

# 修改为你实际的设备名，例如 /dev/ttyUSB0 或 /dev/ttyS1
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

time.sleep(2)  # 等待串口稳定

ser.write(b'Hello STM32!\n')
print("已发送: Hello STM32!")

while True:
    data = ser.readline()
    if data:
        print("收到STM32返回:", data.decode(errors='ignore').strip())
