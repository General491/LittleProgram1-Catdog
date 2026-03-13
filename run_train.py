# run_train.py
"""
训练脚本
既可以直接运行，也支持在命令行中传参修改，例如：
python run_train.py --epochs 3 --model yolov5s.pt
"""
from __future__ import annotations
import shutil
import argparse
import os
import tempfile
from pathlib import Path
from ultralytics import YOLO
import torch
import yaml

def main() -> None:
    # 1. 设置命令行参数解析，完美对接你的 README
    parser = argparse.ArgumentParser(description="YOLOv5 训练脚本")
    parser.add_argument('--data', type=str, default="datasets/data.yaml", help='数据集配置文件路径')
    parser.add_argument('--model', type=str, default="yolov5s.pt", help='初始模型权重文件')
    parser.add_argument('--epochs', type=int, default=3, help='训练轮数 (体验课建议设为3)')
    parser.add_argument('--imgsz', type=int, default=640, help='图像尺寸')
    parser.add_argument('--batch', type=int, default=8, help='批次大小 (如果显存/内存爆了就调小到 4 或 2)')
    
    args = parser.parse_args()

    # 2. 硬件防翻车自动检测
    # 如果有英伟达显卡且配好了CUDA，就用GPU(0)，否则老老实实用CPU
    auto_device = "0" if torch.cuda.is_available() else "cpu"
    print(f"[*] 系统硬件检测完成，当前使用运算设备: {auto_device}")

    project_root = Path(__file__).resolve().parent
    project = str((project_root / "runs" / "train").resolve())
    name = "data_yolov5s_train"

    data_path = Path(args.data)
    if not data_path.is_absolute():
        data_path = project_root / data_path

    if not data_path.exists():
        raise FileNotFoundError(
            f"[!] 致命错误：未找到数据配置文件: {data_path}"
        )

    # 3. 生成临时 data.yaml（只在本次训练使用），强制使用当前工程 datasets 绝对路径
    with data_path.open("r", encoding="utf-8") as f:
        data_cfg = yaml.safe_load(f) or {}

    datasets_root = (project_root / "datasets").resolve()
    data_cfg["path"] = datasets_root.as_posix()
    data_cfg.setdefault("train", "images/train")
    data_cfg.setdefault("val", "images/val")

    fd, temp_yaml = tempfile.mkstemp(prefix="train_data_", suffix=".yaml")
    os.close(fd)
    temp_yaml_path = Path(temp_yaml)
    with temp_yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data_cfg, f, allow_unicode=True, sort_keys=False)

    print(f"[*] 使用数据配置: {data_path}")
    print(f"[*] 本次训练临时配置: {temp_yaml_path}")

    # 4. 开始训练
    try:
        model = YOLO(args.model)
        model.train(
            data=str(temp_yaml_path),
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch=args.batch,
            workers=0,  # Windows 下新手极易因为多进程报错，建议设为 0
            device=auto_device,
            patience=20,
            project=project,
            name=name,
        )
    finally:
        if temp_yaml_path.exists():
            temp_yaml_path.unlink()

    # 5. 自动复制最佳权重到工程根目录
    best_pt = Path(project) / name / "weights" / "best.pt"
    root_best_pt = Path(__file__).resolve().parent / "best.pt"

    print("\n" + "=" * 60)
    if best_pt.exists():
        shutil.copy2(best_pt, root_best_pt)
        print(f"🎉 训练圆满完成！")
        print(f"👉 原始权重位置: {best_pt.resolve()}")
        print(f"👉 已自动提取到根目录: {root_best_pt} (现在你可以直接运行 run_predict.py 去测试它了！)")
    else:
        print("[!] 训练已结束，但未找到 best.pt 文件，请检查控制台报错信息。")

if __name__ == "__main__":
    main()