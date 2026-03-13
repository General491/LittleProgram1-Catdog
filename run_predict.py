# run_predict.py
from ultralytics import YOLO
import cv2

print("正在加载大脑权重...")
# 1. 加载提前“炼”好的模型权重
model = YOLO('best.pt') 

print("开始预测！请注意看弹出的窗口！")
# 2. 对指定的图片进行目标检测
# source='test_images/cat_s/cat_1.jpg'' 代表你要检测的图片路径，你可以自行修改图片路径来测试不同的图片
# save=True 代表将画好框的图片保存下来，show=True 代表直接弹窗显示
results = model.predict(source='test_images/cat_s/cat_1.jpg', save=True, show=False)

# 3. 手动控制窗口停留时间（毫秒）
# 例如 8000=8秒；改成 0 表示一直等你按键才关闭
display_ms = 8000

img = results[0].plot()  # 画框后的图片
cv2.imshow('YOLO Predict', img)
cv2.waitKey(display_ms)
cv2.destroyAllWindows()

print("预测完成！请去当前目录下的 runs/detect 文件夹查看结果图。")