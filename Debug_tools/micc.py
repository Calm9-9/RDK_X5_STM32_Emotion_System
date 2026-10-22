import pyaudio

p = pyaudio.PyAudio()
device_index = 1  # 你的 USB 麦克风

for rate in [8000, 16000, 22050, 32000, 44100, 48000]:
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        input_device_index=device_index)
        stream.close()
        print(f"✅ 支持采样率: {rate}")
    except Exception as e:
        print(f"❌ 不支持采样率: {rate} ({e})")

p.terminate()
