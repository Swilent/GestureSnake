# 🐍 贪吃蛇游戏 - 手势控制版

[![Python 版本](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/opencv-4.x-green.svg)](https://opencv.org)
[![许可证](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

一款创新的贪吃蛇游戏实现，将经典玩法与现代计算机视觉技术相结合。通过摄像头捕捉手势来控制贪吃蛇，基于 OpenCV 和 cvzone 技术开发。

## 🙏 致谢

本项目的实现离不开以下资源和贡献者的支持：

- 灵感来源于 [Bilibili 教程](https://www.bilibili.com/video/BV17L411P7gi)
- 基础实现来自 [WLHSDXN/Project2](https://github.com/WLHSDXN/Project2/tree/main/SnakeGame)
- [cvzone](https://github.com/cvzone/cvzone) 提供手势追踪模块
- [MediaPipe]([https://mediapipe.dev/](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=zh-cn)) 提供手势检测技术

## 📋 目录

- [项目特性](#-项目特性)
- [项目结构](#-项目结构)
- [安装说明](#-安装说明)
- [使用方法](#-使用方法)
- [游戏控制](#-游戏控制)
- [技术实现](#-技术实现)
- [性能优化](#-性能优化)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

## ✨ 项目特性

### 🎮 核心玩法
- **手势控制**：实时手指追踪，直观控制贪吃蛇移动
- **经典机制**：食物收集、成长系统、碰撞检测
- **计分系统**：实时分数显示和游戏结束统计

### 🚀 性能优化
- **碰撞检测增强**：基于距离的计算，提高准确度
- **渲染优化**：使用 numpy 数组和多边形线段高效绘制
- **帧率控制**：稳定的 60 FPS 游戏体验
- **选择性自碰撞**：降低检测频率以提升性能

### 🏗️ 架构设计
- **模块化设计**：清晰的关注点分离
- **面向对象**：结构良好的类，易于维护
- **配置驱动**：集中化的常量，便于定制
- **错误处理**：完善的摄像头和资源初始化检查

## 📁 项目结构

```
SnakeGame/
├── main.py                 # 主程序入口
├── game_config.py          # 游戏配置常量
├── snake_game.py           # 核心游戏逻辑
├── ui_manager.py           # UI 界面管理
├── hand_detector.py        # 手势检测模块
├── donut.png              # 食物图片
└── README.md              # 本文件
```

## 🧩 模块说明

### `game_config.py`
中央配置文件，包含：
- 屏幕尺寸和显示设置
- 贪吃蛇外观参数（颜色、大小）
- 食物配置和生成设置
- 碰撞检测阈值
- 性能调优参数

### `snake_game.py`
核心游戏引擎，包含 `SnakeGame` 类：
- 贪吃蛇移动和身体更新
- 碰撞检测算法
- 食物生成和消耗逻辑
- 游戏状态管理
- 使用 numpy 多边形优化渲染

### `ui_manager.py`
通过 `UIManager` 类进行用户界面管理：
- 实时 FPS 计算和显示
- 分数渲染和游戏结束画面
- 手势检测状态指示器
- 视觉反馈系统

### `hand_detector.py`
计算机视觉模块，包含 `HandDetectionManager`：
- 摄像头初始化和管理
- 使用 cvzone 进行的手势追踪
- 食指位置提取
- 手势到移动的转换

### `main.py`
应用程序入口点：
- 模块集成和初始化
- 主游戏循环实现
- 输入处理（键盘和手势）
- 应用程序生命周期管理

## 🚀 安装说明

### 系统要求
- Python 3.11 或更高版本
- 可用的摄像头设备
- 充足的照明条件以进行手势检测

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/Swilent/GestureSnake.git
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 使用方法

运行主脚本即可开始游戏：

```bash
python main.py
```

游戏将自动：
- 初始化您的摄像头
- 显示游戏窗口
- 开始检测手势
- 开始游戏

## 🕹️ 游戏控制

| 控制 | 操作 |
|------|------|
| **手势移动** | 移动食指控制贪吃蛇方向 |
| **R 键** | 重新开始游戏 |
| **ESC 键** | 退出游戏 |
| **Q 键** | 退出游戏 |

## 🔧 技术实现

### 核心技术
- **OpenCV**：实时图像处理和摄像头捕获
- **cvzone**：基于 MediaPipe 的手势追踪模块
- **NumPy**：用于渲染的高效数组操作

### 关键算法

1. **手势追踪**
   - 基于 MediaPipe 的手部关键点检测
   - 食指尖端位置提取
   - 移动阈值过滤以防止抖动

2. **碰撞检测**
   - 基于距离的计算以提高准确性
   - 选择性自碰撞检测（每5帧）
   - 使用边缘检测的边界碰撞

3. **渲染优化**
   - 单次多边形线段绘制贪吃蛇身体
   - NumPy 数组操作提升性能
   - 帧率限制确保一致的游戏体验

## ⚡ 性能优化

### 算法改进
- 最小移动阈值防止重复点
- 使用 while 循环替代 for 循环以提高长度控制效率
- 使用距离计算替代矩形碰撞检测

### 渲染增强
- 减少自碰撞检测频率（5帧间隔）
- 简化碰撞逻辑，仅检查关键点
- FPS 控制渲染确保流畅游戏

### 内存效率
- 模块化设计减少内存占用
- 高效的贪吃蛇身体存储数据结构
- 游戏退出时资源清理

## 🤝 贡献指南

我们欢迎贡献！请随时提交 Pull Request。

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某个功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 系统要求

确保您的系统满足以下要求：
- 功能正常的摄像头设备
- 充足的照明条件以进行手势检测
- 最低屏幕分辨率：800x600
- Python 3.11 或兼容版本

## 📄 许可证

本项目在 MIT 许可证下授权 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 📜 更新日志

### v2.0 - 优化版本
- 依赖优化，适配 Python 3.11
- 算法优化，添加最小移动阈值
- 性能优化，减少自碰撞检测频率
- 代码结构模块化
- 用户体验改进
- 可维护性提升

### v1.0 - 初始版本
- 基础手势控制功能
- 经典贪吃蛇游戏机制
- 基本的 UI 和得分系统
