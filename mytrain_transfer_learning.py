from ultralytics import  YOLO

if __name__ == "__main__":
    # 基于官方yolo11结构加载yolo11n预训练权重
    model = YOLO(r'E:\PapeGamesGit\ultralytics\ultralytics\cfg\models\11\yolo11.yaml').load(r"yolo11n.pt")

    # 继续使用包含81类的数据（保持原COCO80类 + coke），不再使用 classes 过滤避免遗忘其它类
    model.train(
        data=r"E:\PapeGamesGit\ultralytics\ultralytics\cfg\datasets\apple_mini.yaml",
        epochs=12,          # 再减少轮次
        batch=-1,
        lr0=1.5e-5,         # 更低初始学习率减缓权重漂移
        lrf=0.2,            # 终止学习率稍高一点防止过拟合尾部
        imgsz=640,
        device=0,
        freeze=11,          # 只训练neck+head
        project=r"E:\PapeGamesGit\ultralytics\runs\train",
        name="yolo11n_tl_apple_coke",
        exist_ok=True,
        cos_lr=True,        # 余弦调度更平滑
        close_mosaic=5,     # 提前关闭mosaic避免小数据扰动
        patience=5,         # 早停，验证无提升时停止
    )