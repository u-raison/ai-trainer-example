# AI Trainer Example

人工智能课程练习代码合集，涵盖数据清洗、数据可视化、AIML 聊天机器人、图像数据增强、视频采集处理等示例。

## 目录结构

### 数据清洗（pandas）
- `data-cleaning-example-1/2/3.py` — 数据清洗示例（缺失值、重复值、格式处理）
- `data-cleaning-test-1/2/3.py` — 配套练习
- 数据文件：`employees.csv`、`sales.csv`、`fruit.csv`、`学生成绩.csv` 等

### 数据可视化（matplotlib / Jupyter）
- `data-visualization-bar.py` / `line.py` / `pie.py` — 柱状图、折线图、饼图
- `data-visualization-example-2.py`、`data-visualizaiton-example-1.ipynb`、`data-visualization-example-3.ipynb`
- 输出图表：`折线图.png`、`水果饼图.png`、`综合分析图.png` 等

### AIML 聊天机器人
- `aiml-test-example-1/2/3.py` — AIML 机器人示例
- `hospital.aiml`、`hospital-2.aiml`、`chatbot-formatted.aiml`、`ai-service-test.aiml` — AIML 规则文件
- `bot_brain.brn`、`bot_brain-2.brn` — 编译后的机器人大脑文件

### 图像数据增强（imgaug / PIL）
- `image-augment-example-1.py` — 批量图像增强（翻转、旋转、裁剪等）
- `images5/` — 原始图片，`augmented/`、`images_output/` — 增强输出

### 视频采集（OpenCV）
- `video-capture-example-*.py`、`video-capture-test-*.py` — 摄像头采集、视频读取、逐帧保存
- `video.mp4` — 测试视频，`images/` ~ `images4/` — 提取的视频帧

## 环境依赖

```bash
pip install pandas matplotlib opencv-python pillow imgaug python-aiml jupyter openpyxl
```

## 运行

各脚本可直接独立运行，例如：

```bash
python data-cleaning-example-1.py
python data-visualization-bar.py
python aiml-test-example-1.py
```
