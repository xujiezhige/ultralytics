from ultralytics import YOLO

model = YOLO(r"D:\GithubProjects\ultralytics\runs\detect\train5\weights\best.pt")

model.predict(
    source=r"D:\GithubProjects\ultralytics\datasets\test_dataset\images\val",
    show=False,
    save=True,
)