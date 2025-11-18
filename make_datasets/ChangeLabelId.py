from pathlib import Path

# 目录路径（可修改）
LABEL_DIR = Path(r"E:\PapeGamesGit\ultralytics\make_datasets\Temp\labels")
# 映射关系：原ID -> 新ID
ID_MAP = {0: 47, 1: 80}


def convert_label_line(line: str) -> str:
    """将单行YOLO标签的class id按映射替换，保持其他数值不变。"""
    line = line.strip()
    if not line:
        return line
    parts = line.split()
    try:
        cls = int(parts[0])
    except ValueError:
        return line  # 首字段非整数，跳过
    if cls in ID_MAP:
        parts[0] = str(ID_MAP[cls])
    return " ".join(parts)


def process_file(fp: Path) -> tuple[int, int]:
    """处理单个文件，返回(修改行数, 总行数)。"""
    with fp.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    modified = 0
    new_lines = []
    for line in lines:
        new_line = convert_label_line(line)
        if new_line.strip() and new_line != line.strip():
            modified += 1
        new_lines.append(new_line + ("\n" if not new_line.endswith("\n") else ""))
    with fp.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)
    return modified, len(lines)


def main():
    if not LABEL_DIR.is_dir():
        print(f"目录不存在: {LABEL_DIR}")
        return
    txt_files = list(LABEL_DIR.glob("*.txt"))
    if not txt_files:
        print("未找到任何.txt标签文件")
        return
    total_files = len(txt_files)
    total_lines = 0
    total_modified = 0
    for fp in txt_files:
        modified, lines = process_file(fp)
        total_lines += lines
        total_modified += modified
        print(f"处理 {fp.name}: 修改 {modified}/{lines} 行")
    print("--- 汇总 ---")
    print(f"文件数: {total_files}")
    print(f"总行数: {total_lines}")
    print(f"被修改行数: {total_modified}")
    print("完成。")


if __name__ == "__main__":
    main()
