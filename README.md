# RDK X5 & STM32 Emotion Assistant System (语音情绪感知与反馈系统)

本项目为一个软硬件结合的嵌入式边缘 AI 原型系统。采用 **RDK X5 (Linux 上位机) + STM32F103 (MCU 下位机)** 的异构架构，实现了从“语音采集 - 情绪分析 - 多模态硬件反馈”的完整闭环。

## 🛠 技术栈 (Tech Stack)
*   **下位机 (MCU)**: STM32F103, C 语言, UART 中断, GPIO 驱动, 硬件调试
*   **上位机 (Linux)**: RDK X5 (Ubuntu), Python, PyAudio (音频处理), PySerial (串口通信)
*   **边缘 AI 探索**: openSMILE (特征提取), TensorFlow/Keras (模型冻结与转换)
*   **开发工具**: Keil, Git, Linux Shell

## 📂 仓库目录说明 (Repository Structure)
*   `/STM32_Code`：STM32 裸机开发核心代码，包含 USART 中断接收、GPIO 外设驱动（控制马达、RGB灯及语音模块）。
*   `/Linux_Code`：RDK X5 端 Python 应用程序，包含音频采集、重采样（44.1kHz转16kHz）及串口通信逻辑。
*   `/Debug_Tools`： 独立编写的底层排错验证脚本。
    *   `mic.py`：用于遍历 Linux 音频设备，排查 USB 麦克风 ID 冲突与权限问题。
    *   `micc.py`：音频采集测试脚本，验证麦克风音频流读取。
    *   `serial_test.py`：串口回环测试脚本，用于验证 UART 通信链路及波特率配置。
    *   `stm32.py`：带握手应答的二进制串口测试脚本，遍历情绪编码，用于正式协议验证。
    *   `stm321.py`：ASCII协议循环发送脚本，持续下发情绪指令，做长时间稳定性测试。
    *   `stm322.py`：ASCII协议单次随机发送脚本，用于情绪识别推理链路快速联调。
    *   `check.py`、`check_snpe_runtime.py`：环境校验脚本，分别检查系统依赖、SNPE NPU推理运行时。
1.  **异构系统联调**：打通了 Linux 环境与单片机的 3.3V TTL 串口通信，设计了基于单字节指令的通信协议。
2.  **分层验证排错法**：面对底层硬件无响应，不盲目修改业务代码。独立开发上述 Debug 脚本，按照“物理接线 -> 系统权限 -> 通信协议 -> 业务逻辑”的顺序，成功定位并解决了 Linux 设备权限冲突、串口丢包等底层异常。
3.  **边缘 AI 部署链路探索**：参与完成 openSMILE 声学特征提取与 CNN 模型训练，并完成了 Keras (`.h5`) 到 TensorFlow (`.pb`) 的冻结转换，排查了不同推理工具链的兼容性问题。

---

