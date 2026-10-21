#!/usr/bin/env python3
import os
import subprocess

# 配置路径
SNPE_BIN = "/home/sunrise/Qualcomm/AIStack/QAIRT/2.30.0.250109/bin/aarch64-ubuntu-gcc9.4/snpe-net-run"
DLC_MODEL = "/home/sunrise/maindocuments/checkpoints/CNN1D_OPENSMILE_model.dlc"
INPUT_LIST = "/home/sunrise/maindocuments/features/input_list.txt"
OUTPUT_DIR_BASE = "/home/sunrise/maindocuments/snpe_runtime_check"

# 要检测的 runtime
runtimes = {
    "CPU": "--use_cpu",
    "GPU": "--use_gpu",
    "HTP": "--use_aip"
}

def check_runtime(name, flag):
    output_dir = os.path.join(OUTPUT_DIR_BASE, name.lower())
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        SNPE_BIN,
        "--container", DLC_MODEL,
        "--input_list", INPUT_LIST,
        flag,
        "--output_dir", output_dir
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[OK] Runtime {name} available.")
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Runtime {name} not available.")
        print("Error message:")
        print(e.stderr.decode())

if __name__ == "__main__":
    print("[INFO] SNPE Runtime + HTP Library Check (v2)")
    for name, flag in runtimes.items():
        check_runtime(name, flag)
