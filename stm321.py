import serial, time

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
print("✅ 串口已打开:", ser.portstr)

try:
    while True:
        for emotion in range(6):
            msg = f"{emotion}\n".encode()   # ✅ 发送文本 + 换行符
            ser.write(msg)
            print(f"已发送情绪信号: {emotion}")
            time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    ser.close()

