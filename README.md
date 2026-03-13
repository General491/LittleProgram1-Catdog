🚀 视觉组新生专属：YOLOv5环境配置与实战指南
欢迎来到视觉组培训课！今天我将亲手在你的电脑上召唤出能识别动物的AI。请严格按照以下步骤操作，遇到标红的**【警告】**请务必停下来检查！

🛑 第0步：不许出现中文路径！
【绝对警告】从今天起，作为一名极客，你的代码、软件安装路径中绝对不能出现任何中文字符或空格！

❌错误示范：D:\我的大学\视觉组培训\yolov5_training1
✅正确示范：D:\CV_Training\yolov5_training1

🛠️ 第1步：安装“环境管家” Anaconda
自行在官网 https://www.anaconda.com/ 下载安装包进行安装。

一路Next，但在Advanced Options（高级选项）那一步，请勾选“Add Anaconda3 to my PATH environment variable”（虽然报红，但对新手最友好，免去手动配环境变量的痛苦）。
（注意！Conda最好不要放在C盘，环境文件夹也最好不要放在C盘，环境装多了容易挤爆存储空间！）
安装完成后，在电脑左下角搜索框输入 Anaconda Prompt 并打开，出现一个黑框框，说明安装成功！

🔪 第2步：划定隔离结界（创建虚拟环境）
为了不把电脑原本的环境搞崩溃，我们需要用Conda创建一个虚拟环境。
在刚才打开的黑框框（Anaconda Prompt）里，输入以下命令并回车：
conda create -n yolo_env python=3.9 -y  //yolo_env是环境的名字，你可以换成别的名字，比如yolo_dodo
等跑完之后，激活并进入我们的环境：
conda activate yolo_env
此时，你会看到黑框框最前面的 (base) 变成了 (yolo_env)，进入成功！

📦 第3步：装填弹药（安装依赖库）
离线安装：我已经为大家下载了离线的深度学习框架pytorch+torchvision的安装包，避免临时下载占用时间。
先进入你的实战文件夹目录，比如：cd D:\CV_Training\yolo_training
请在黑框的(yolo_env)环境下输入：
1.pip install offline_packages/torch-2.0.1+cpu-cp39-cp39-win_amd64.whl //安装pytorch
2.pip install offline_packages/torchvision-0.15.2+cpu-cp39-cp39-win_amd64.whl //安装torchvision
3.pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple //安装其他需求（网站是用于换源）
到此为止，你的环境已经基本配置好了。

🎯 第4步：见证奇迹（跑通模型预测）
激动人心的时刻到了！我们不用从头训练，直接借用学长提前训练好的模型权重文件（权重文件best.pt）。
确保你的素材图片（比如cat_1.jpg）放在了test_images/cat_s文件夹下。输入以下召唤口令：
python run_predict.py
代码跑完后，它会自动弹窗展示画好框的小动物，同时结果也会保存在 runs/detect 目录下。

查看战果：
代码跑完后，它会提示你结果保存在了 runs/detect/exp 目录下。快去打开那个文件夹，看看图上的小动物是不是被精准框出来了！

💡 进阶挑战（现场尝试）：
想看看AI的动态视力吗？输入以下口令：
python run_camera.py
这会直接调用你电脑自带的摄像头进行实时检测。拿你的手机搜一张修勾（小狗）的图片怼到镜头前试试看吧！（按 'q' 键可以退出画面）

给你的后续建议：
打通了上面这一套，你就走完了深度学习的基本步骤。
虽然我们目前跑的是猫狗检测，但底层的代码逻辑，和咱们用树莓派、Jetson等边缘板配合相机做目标检测是一模一样的。
可以尝试修改各种参数、更换数据集来进行训练，还可以使用YOLO系列的各种模型，包括最新的YOLOv11和YOLO26！

🔥 第5步：用 train 数据集训练你自己的 .pt 权重
训练脚本为run_train.py，它会自动执行训练任务。
在 (yolo_env) 环境里直接执行：
python run_train.py

如果你想从已有 .pt 权重继续训练：
python run_train.py --model 你的权重文件.pt

训练完成后，使用你新得到的best.pt替换预测脚本中的权重路径即可。