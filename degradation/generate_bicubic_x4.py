#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate ×4 bicubic low-resolution (LR) images from high-resolution (HR) images.

This script reproduces the degradation procedure used in the experiments:
1. Read each HR image and convert it to RGB.
2. Crop width and height to the largest values divisible by the scale factor.
3. Downsample using Pillow bicubic interpolation.
4. Save the LR image as PNG by default.

Example
-------
python degradation/generate_bicubic_x4.py \
    --hr-dir InsulatorDefect_TestSet_v1.0/images/test \
    --lr-dir LR_bicubic_x4/test \
    --scale 4 \
    --save-ext .png
"""

import argparse
import os
from PIL import Image


SUPPORTED_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
)


def get_bicubic_resample():
    """
    Use Pillow bicubic interpolation while remaining compatible with
    both older and newer Pillow versions.
    """
    if hasattr(Image, "Resampling"):
        return Image.Resampling.BICUBIC
    return Image.BICUBIC


def generate_lr_from_hr(hr_dir, lr_dir, scale=4, save_ext=".png"):
    os.makedirs(lr_dir, exist_ok=True)

    if scale <= 1:
        raise ValueError("scale must be greater than 1.")

    if not save_ext.startswith("."):
        save_ext = "." + save_ext

    bicubic = get_bicubic_resample()

    image_count = 0

    for filename in sorted(os.listdir(hr_dir)):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        hr_path = os.path.join(hr_dir, filename)

        with Image.open(hr_path) as img:
            hr = img.convert("RGB")

        w, h = hr.size

        # Crop the HR image so that both dimensions are divisible by scale.
        # This preserves the original experimental preprocessing procedure.
        w2 = (w // scale) * scale
        h2 = (h // scale) * scale

        if w2 == 0 or h2 == 0:
            print(f"Skip {filename}: image is too small for scale={scale}.")
            continue

        if (w2, h2) != (w, h):
            hr = hr.crop((0, 0, w2, h2))
            w, h = hr.size

        # Bicubic ×scale downsampling.
        lr = hr.resize(
            (w // scale, h // scale),
            resample=bicubic,
        )

        out_name = os.path.splitext(filename)[0] + save_ext
        out_path = os.path.join(lr_dir, out_name)
        lr.save(out_path)

        image_count += 1
        print(
            f"{filename}: "
            f"HR {w}x{h} -> LR {w // scale}x{h // scale}"
        )

    print(f"Done. Generated {image_count} LR images.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate bicubic ×N LR images from HR images."
    )

    parser.add_argument(
        "--hr-dir",
        type=str,
        required=True,
        help="Directory containing the HR images.",
    )

    parser.add_argument(
        "--lr-dir",
        type=str,
        required=True,
        help="Directory in which the generated LR images will be saved.",
    )

    parser.add_argument(
        "--scale",
        type=int,
        default=4,
        help="Downsampling scale factor. Default: 4.",
    )

    parser.add_argument(
        "--save-ext",
        type=str,
        default=".png",
        help="Output image extension. Default: .png",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    generate_lr_from_hr(
        hr_dir=args.hr_dir,
        lr_dir=args.lr_dir,
        scale=args.scale,
        save_ext=args.save_ext,
    )
