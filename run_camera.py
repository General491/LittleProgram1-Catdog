# run_camera.py
from ultralytics import YOLO

print("正在启动视觉神经中枢...")
# 1. 加载模型
model = YOLO('best.pt')

print("正在唤醒摄像头，按 'q' 键可以退出预测画面！")
# 2. 打开电脑自带摄像头进行实时检测
# source=0 代表调用编号为0的默认摄像头
# show=True 代表实时显示带检测框的画面
results = model.predict(source=0, show=True)