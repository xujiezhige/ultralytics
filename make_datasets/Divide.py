import os
import random
import shutil
from pathlib import Path

# 数据集根目录，比如：
# root/
#   images/
#     img1.jpg
#   labels/
#     img1.txt
DATA_ROOT = Path(r"E:\PapeGamesGit\ultralytics\datasets\test_dataset")
IMG_DIR = DATA_ROOT / "images"
LABEL_DIR = DATA_ROOT / "labels"

# 子集比例
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2  # 剩下的是 test

# 支持的图片后缀
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

def main():
    # 1. 收集所有有对应标签的图片基名
    image_files = []
    for p in IMG_DIR.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            stem = p.stem
            label_path = LABEL_DIR / f"{stem}.txt"
            if label_path.exists():
                image_files.append(p)

    if not image_files:
        print("未找到带标签的图片文件")
        return

    # 2. 打乱并切分
    random.shuffle(image_files)
    n = len(image_files)
    n_train = int(n * TRAIN_RATIO)
    n_val = int(n * VAL_RATIO)
    n_test = n - n_train - n_val

    train_imgs = image_files[:n_train]
    val_imgs = image_files[n_train:n_train + n_val]
    test_imgs = image_files[n_train + n_val:]

    print(f"总数: {n}, train: {len(train_imgs)}, val: {len(val_imgs)}, test: {len(test_imgs)}")

    # 3. 为三个子集创建目标目录
    for subset in ["train", "val", "test"]:
        (IMG_DIR / subset).mkdir(parents=True, exist_ok=True)
        (LABEL_DIR / subset).mkdir(parents=True, exist_ok=True)

    # 4. 拷贝函数
    def copy_pair(img_paths, subset):
        for img_path in img_paths:
            stem = img_path.stem
            label_path = LABEL_DIR / f"{stem}.txt"
            if not label_path.exists():
                continue

            # 目标路径
            dst_img = IMG_DIR / subset / img_path.name
            dst_label = LABEL_DIR / subset / label_path.name

            shutil.copy2(img_path, dst_img)
            shutil.copy2(label_path, dst_label)

    copy_pair(train_imgs, "train")
    copy_pair(val_imgs, "val")
    copy_pair(test_imgs, "test")

    print("划分完成。")

if __name__ == "__main__":
    main()
