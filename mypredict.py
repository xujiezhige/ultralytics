from ultralytics import YOLO

model = YOLO(r"D:\GithubProjects\ultralytics\apple_mini.pt")

model.predict(
    source=r"D:\GithubProjects\ultralytics\datasets\make_datasets\images",
    save=True,
    show=False,
    save_txt=True,
)