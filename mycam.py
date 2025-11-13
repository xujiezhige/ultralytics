import cv2

from ultralytics import YOLO

model = YOLO(r"D:\DeepLearning\ultralytics-8.3.163\yolo11n.pt")

results = model.predict(
    source=0,
    stream=True,
)

for result in results:
    plotted = result.plot()
    cv2.imshow("YOLO Inference", plotted)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()