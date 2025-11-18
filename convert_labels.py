import os

# ---------------- 配置 ----------------
labels_dir = r"E:\PapeGamesGit\ultralytics\datasets\test_dataset\labels\val"  # 你的标签文件夹路径
output_dir = r"E:\PapeGamesGit\ultralytics\datasets\test_dataset\labels\val_new"  # 输出修改后的标签文件夹
os.makedirs(output_dir, exist_ok=True)

# 当前你的类别编号映射
# 0 -> apple
# 1 -> coke
# 转换成 COCO 扩展编号
class_mapping = {
    0: 47,  # apple
    1: 80  # coke
}

# ---------------- 处理 ----------------
for filename in os.listdir(labels_dir):
    if not filename.endswith(".txt"):
        continue
    input_path = os.path.join(labels_dir, filename)
    output_path = os.path.join(output_dir, filename)

    with open(input_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue  # 忽略格式错误行
        old_class = int(parts[0])
        if old_class in class_mapping:
            new_class = class_mapping[old_class]
            new_lines.append(f"{new_class} {parts[1]} {parts[2]} {parts[3]} {parts[4]}\n")

    with open(output_path, "w") as f:
        f.writelines(new_lines)

print("转换完成！新标签保存在:", output_dir)
