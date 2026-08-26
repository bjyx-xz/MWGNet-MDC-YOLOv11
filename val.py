#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Public evaluation script for MDC-YOLOv11.

Example:
    python val.py \
        --weights MDC_YOLOv11_best.pt \
        --data dataset/data_test.yaml \
        --imgsz 640 \
        --batch 16 \
        --conf 0.39 \
        --iou 0.55 \
        --max-det 200

Notes:
- The default evaluation settings preserve the values used in the original script:
  imgsz=640, batch=16, conf=0.39, iou=0.55, max_det=200.
- Replace only the weights/data paths when reproducing the evaluation.
"""

import argparse
import os
import platform
import sys
import warnings

import numpy as np
import torch
import ultralytics
from prettytable import PrettyTable
from ultralytics import YOLO
from ultralytics.utils.torch_utils import model_info

warnings.filterwarnings("ignore")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate MDC-YOLOv11 on a YOLO-format test set."
    )
    parser.add_argument(
        "--weights",
        type=str,
        required=True,
        help="Path to trained model weights, e.g. MDC_YOLOv11_best.pt",
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to dataset YAML, e.g. dataset/data_test.yaml",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="test",
        choices=["train", "val", "test"],
        help="Dataset split to evaluate.",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument(
        "--conf",
        type=float,
        default=0.39,
        help="Confidence threshold.",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.55,
        help="NMS IoU threshold.",
    )
    parser.add_argument(
        "--max-det",
        type=int,
        default=200,
        help="Maximum detections per image.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Evaluation device, e.g. 0 or cpu. Default: Ultralytics auto selection.",
    )
    parser.add_argument(
        "--project",
        type=str,
        default="runs/val",
        help="Directory for validation outputs.",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="exp",
        help="Validation run name.",
    )
    parser.add_argument(
        "--save-json",
        action="store_true",
        help="Save JSON predictions if supported.",
    )
    return parser.parse_args()


def get_weight_size(path):
    stats = os.stat(path)
    return f"{stats.st_size / 1024 / 1024:.1f}"


def safe_get_list(x):
    """Convert tensor/list/ndarray-like objects to a Python list."""
    if x is None:
        return []
    if isinstance(x, list):
        return x
    try:
        if hasattr(x, "detach"):
            x = x.detach().cpu()
        return list(x)
    except Exception:
        return []


def safe_get_value(x, idx, default=0.0):
    """Safely obtain one numeric value."""
    try:
        return float(x[idx])
    except Exception:
        return default


def safe_get_ap75(all_ap, idx, default=0.0):
    """
    all_ap generally corresponds to IoU thresholds [0.50:0.05:0.95].
    Index 5 corresponds to IoU=0.75.
    """
    try:
        return float(all_ap[idx, 5])
    except Exception:
        try:
            return float(all_ap[idx][5])
        except Exception:
            return default


def get_model_info_compatible(model, imgsz):
    """
    Call model_info in a way compatible with different Ultralytics versions.
    """
    try:
        return model_info(model, imgsz=imgsz)
    except TypeError:
        return model_info(model)


def print_environment():
    print("=" * 70)
    print("Environment")
    print("=" * 70)
    print(f"Python      : {sys.version.split()[0]}")
    print(f"Platform    : {platform.platform()}")
    print(f"PyTorch     : {torch.__version__}")
    print(f"CUDA        : {torch.version.cuda}")
    print(f"Ultralytics : {ultralytics.__version__}")
    print(f"NumPy       : {np.__version__}")
    print("=" * 70)


def main():
    args = parse_args()

    if not os.path.isfile(args.weights):
        raise FileNotFoundError(f"Weights not found: {args.weights}")

    if not os.path.isfile(args.data):
        raise FileNotFoundError(f"Dataset YAML not found: {args.data}")

    print_environment()

    model = YOLO(args.weights)

    val_kwargs = dict(
        data=args.data,
        split=args.split,
        imgsz=args.imgsz,
        batch=args.batch,
        conf=args.conf,
        iou=args.iou,
        max_det=args.max_det,
        project=args.project,
        name=args.name,
        save_json=args.save_json,
    )

    if args.device is not None:
        val_kwargs["device"] = args.device

    result = model.val(**val_kwargs)

    if model.task != "detect":
        raise RuntimeError(
            f"This script is intended for detection models, but model.task={model.task}"
        )

    # ---------- Basic metrics ----------
    p_list = safe_get_list(getattr(result.box, "p", None))
    r_list = safe_get_list(getattr(result.box, "r", None))
    f1_list = safe_get_list(getattr(result.box, "f1", None))
    ap50_list = safe_get_list(getattr(result.box, "ap50", None))
    ap_list = safe_get_list(getattr(result.box, "ap", None))
    all_ap = getattr(result.box, "all_ap", None)

    length = len(p_list)
    model_names = (
        list(result.names.values())
        if hasattr(result, "names")
        else [f"class_{i}" for i in range(length)]
    )

    preprocess_time_per_image = result.speed.get("preprocess", 0.0)
    inference_time_per_image = result.speed.get("inference", 0.0)
    postprocess_time_per_image = result.speed.get("postprocess", 0.0)

    all_time_per_image = (
        preprocess_time_per_image
        + inference_time_per_image
        + postprocess_time_per_image
    )

    n_l, n_p, n_g, flops = get_model_info_compatible(model.model, args.imgsz)

    print("\n" + "=" * 70)
    print("Evaluation settings")
    print("=" * 70)
    print(f"Weights : {args.weights}")
    print(f"Data    : {args.data}")
    print(f"Split   : {args.split}")
    print(f"imgsz   : {args.imgsz}")
    print(f"batch   : {args.batch}")
    print(f"conf    : {args.conf}")
    print(f"iou     : {args.iou}")
    print(f"max_det : {args.max_det}")
    print("=" * 70)

    # ---------- Model information ----------
    model_info_table = PrettyTable()
    model_info_table.title = "Model Info"
    model_info_table.field_names = [
        "GFLOPs",
        "Parameters",
        "Preprocess / image",
        "Inference / image",
        "Postprocess / image",
        "FPS (total)",
        "FPS (inference)",
        "Model File Size",
    ]

    fps_all = 1000 / all_time_per_image if all_time_per_image > 0 else 0
    fps_inf = 1000 / inference_time_per_image if inference_time_per_image > 0 else 0

    model_info_table.add_row([
        f"{flops:.2f}",
        f"{n_p:,}",
        f"{preprocess_time_per_image / 1000:.6f}s",
        f"{inference_time_per_image / 1000:.6f}s",
        f"{postprocess_time_per_image / 1000:.6f}s",
        f"{fps_all:.2f}",
        f"{fps_inf:.2f}",
        f"{get_weight_size(args.weights)} MB",
    ])

    print(model_info_table)

    # ---------- Metric table ----------
    model_metric_table = PrettyTable()
    model_metric_table.title = "Detection Metrics"
    model_metric_table.field_names = [
        "Class Name",
        "Precision",
        "Recall",
        "F1-Score",
        "mAP50",
        "mAP75",
        "mAP50-95",
    ]

    valid_len = min(length, len(model_names))

    for idx in range(valid_len):
        model_metric_table.add_row([
            model_names[idx],
            f"{safe_get_value(p_list, idx):.4f}",
            f"{safe_get_value(r_list, idx):.4f}",
            f"{safe_get_value(f1_list, idx):.4f}",
            f"{safe_get_value(ap50_list, idx):.4f}",
            f"{safe_get_ap75(all_ap, idx):.4f}",
            f"{safe_get_value(ap_list, idx):.4f}",
        ])

    mean_f1 = (
        float(np.mean([float(x) for x in f1_list[:valid_len]]))
        if valid_len > 0 and len(f1_list) > 0
        else 0.0
    )

    mean_ap75 = 0.0
    if all_ap is not None and valid_len > 0:
        try:
            mean_ap75 = float(np.mean(all_ap[:valid_len, 5]))
        except Exception:
            try:
                mean_ap75 = float(
                    np.mean([row[5] for row in all_ap[:valid_len]])
                )
            except Exception:
                mean_ap75 = 0.0

    results_dict = getattr(result, "results_dict", {}) or {}

    model_metric_table.add_row([
        "all",
        f"{results_dict.get('metrics/precision(B)', 0.0):.4f}",
        f"{results_dict.get('metrics/recall(B)', 0.0):.4f}",
        f"{mean_f1:.4f}",
        f"{results_dict.get('metrics/mAP50(B)', 0.0):.4f}",
        f"{mean_ap75:.4f}",
        f"{results_dict.get('metrics/mAP50-95(B)', 0.0):.4f}",
    ])

    print(model_metric_table)

    # ---------- Save reproducible report ----------
    save_path = result.save_dir / "paper_data.txt"

    with open(save_path, "w", encoding="utf-8") as f:
        f.write("MWGNet-MDC-YOLOv11 Detector Evaluation\n")
        f.write("=" * 70 + "\n")
        f.write(f"Python: {sys.version.split()[0]}\n")
        f.write(f"PyTorch: {torch.__version__}\n")
        f.write(f"CUDA: {torch.version.cuda}\n")
        f.write(f"Ultralytics: {ultralytics.__version__}\n")
        f.write(f"NumPy: {np.__version__}\n\n")

        f.write("Evaluation settings\n")
        f.write("-" * 70 + "\n")
        f.write(f"weights={args.weights}\n")
        f.write(f"data={args.data}\n")
        f.write(f"split={args.split}\n")
        f.write(f"imgsz={args.imgsz}\n")
        f.write(f"batch={args.batch}\n")
        f.write(f"conf={args.conf}\n")
        f.write(f"iou={args.iou}\n")
        f.write(f"max_det={args.max_det}\n\n")

        f.write(str(model_info_table))
        f.write("\n\n")
        f.write(str(model_metric_table))
        f.write("\n")

    print(f"\nResults saved to: {save_path}")


if __name__ == "__main__":
    main()
