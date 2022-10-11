#!/usr/bin/env python
"""
Interpolate every combination of image pairs in the given directory.
Outputs to {image_dir}/output/{image_1}_to_{image_2}/
"""
import argparse
import logging
import os
from itertools import combinations
from pathlib import Path
from typing import List

import mediapy as media
import numpy as np

from frame_interpolation.eval import interpolator as interpolator_lib, util as interpolation_util

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-dir", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--times-to-interpolate", type=int, default=4)
    parser.add_argument("--fps", type=int, default=16)
    return parser.parse_args()


def output_frames(frames: List[np.ndarray], fps: int, start_name: str, end_name: str, output_dir: Path):
    for i, frame in enumerate(frames):
        interpolation_util.write_image(
            str(output_dir / f"{start_name}_to_{end_name}" / f"frame_{i:03d}.png"),
            frame,
        )

    logging.info(f"Wrote {i} frames to {output_dir / f'{start_name}_to_{end_name}'}")

    media.write_video(output_dir / f"{start_name}_to_{end_name}.mp4", frames, fps=fps)
    media.write_video(output_dir / f"{end_name}_to_{start_name}.mp4", frames[::-1], fps=fps)


def interpolate_all(times_to_interpolate: int, fps: int, image_dir: Path, model_path: Path):
    image_files = image_dir.glob("*.png")

    interpolator = interpolator_lib.Interpolator(str(model_path), align=64)

    output_dir = image_dir / "output"
    os.makedirs(output_dir, exist_ok=True)

    for start_frame, end_frame in combinations(image_files, 2):
        frames = list(interpolation_util.interpolate_recursively_from_files(
            frames=[str(start_frame), str(end_frame)],
            times_to_interpolate=times_to_interpolate,
            interpolator=interpolator,
        ))

        output_frames(frames, fps, start_frame.stem, end_frame.stem, output_dir)


if __name__ == "__main__":
    args = parse_args()
    interpolate_all(args.times_to_interpolate, args.fps, args.image_dir, args.model_path)
