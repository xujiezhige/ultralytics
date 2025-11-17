#!/usr/bin/env python3
"""
提取 videos 目录下所有视频的帧到 images 目录。
支持每个视频单独配置提取间隔：在 `videos/config.json` 中指定。
"""

import os
import sys
import json
from pathlib import Path

import cv2

VIDEO_EXTS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}


def load_config(config_path: Path):
    if not config_path.is_file():
        return {}
    try:
        with config_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                # ensure integer values
                return {k: int(v) for k, v in data.items()}
    except Exception:
        pass
    return {}


def should_process_file(path: Path):
    return path.is_file() and path.suffix.lower() in VIDEO_EXTS


def extract_frames(video_path: Path, out_dir: Path, step: int, start_index: int) -> int:
    """从单个视频中按间隔提取帧，并使用全局连续编号命名。

    Args:
        video_path: 视频文件路径
        out_dir: 输出图片目录（通常为 images 根目录或其子目录）
        step: 帧间隔
        start_index: 本视频第一张要使用的全局编号

    Returns:
        int: 实际保存的最后一张图片的编号（包含），如果没有保存则返回 start_index - 1。
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"无法打开视频: {video_path}", file=sys.stderr)
        return start_index - 1

    out_dir.mkdir(parents=True, exist_ok=True)
    frame_idx = 0
    current_index = start_index - 1  # 调整为先加再用
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % step == 0:
            current_index += 1
            fname = f"frame_{current_index:06d}.jpg"
            dst = out_dir / fname
            # 使用 JPEG 保存
            cv2.imwrite(str(dst), frame)
            saved += 1
        frame_idx += 1

    cap.release()
    print(
        f"完成: {video_path.name} -> {out_dir} "
        f"(saved {saved} frames, step={step}, last_index={current_index if saved > 0 else 'N/A'})"
    )
    return current_index if saved > 0 else start_index - 1


def main():
    # 手动设置：将下面变量改为你想要的路径或数值（可以用绝对路径或相对路径）
    VIDEOS_DIR = r"D:\GithubProjects\ultralytics\datasets\make_datasets\videos\apple"   # <-- 手动设置视频目录（示例）
    IMAGES_DIR = r"D:\GithubProjects\ultralytics\datasets\make_datasets\images\apple"   # <-- 手动设置输出图片根目录（示例）
    DEFAULT_STEP = 6                                      # <-- 手动设置默认帧间隔

    videos_dir = Path(VIDEOS_DIR)
    images_dir = Path(IMAGES_DIR)
    if not videos_dir.exists() or not videos_dir.is_dir():
        print(f"`{videos_dir}` 不存在或不是目录", file=sys.stderr)
        sys.exit(1)

    config = load_config(videos_dir / "config.json")

    # 全局帧编号起点，从 0 开始
    global_index = 0

    for root, _, files in os.walk(videos_dir):
        root_path = Path(root)
        # 跳过 config.json 本身
        for f in sorted(files):  # 排序保证顺序稳定
            fp = root_path / f
            if fp.name == "config.json":
                continue
            if not should_process_file(fp):
                continue
            key_full = fp.name
            key_stem = fp.stem
            step = DEFAULT_STEP
            if key_full in config:
                step = int(config[key_full]) if config[key_full] > 0 else step
            elif key_stem in config:
                step = int(config[key_stem]) if config[key_stem] > 0 else step

            # 所有视频的帧统一存到 IMAGES_DIR 下面，使用全局连续编号
            # 如果你仍然想按视频名分子目录，可以改成 images_dir / key_stem
            last_index = extract_frames(fp, images_dir, max(1, int(step)), global_index)
            # 下一段视频从 last_index + 1 开始
            global_index = last_index + 1 if last_index >= global_index else global_index


if __name__ == "__main__":
    main()