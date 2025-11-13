from ultralytics import YOLO

model = YOLO(r"E:\PapeGamesGit\ultralytics\runs\detect\train4\weights\best.pt")

model.predict(
    source=r"datasets\test_dataset\images\val",
    save=True,
    show=False,
)