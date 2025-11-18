from ultralytics import YOLO

model = YOLO(r"E:\PapeGamesGit\ultralytics\runs\train\yolo11n_tl_apple_coke\weights\best.pt")

model.predict(
    # source=r"E:\PapeGamesGit\ultralytics\make_datasets\Temp\images",
    source=r"E:\PapeGamesGit\ultralytics\ultralytics\assets",
    save=True,
    show=True,
    # 将每张图片的检测结果以YOLO标签txt格式保存
    save_txt=True,
)