import warnings
warnings.filterwarnings('ignore')

import os
import numpy as np
from prettytable import PrettyTable
from ultralytics import YOLO
from ultralytics.utils.torch_utils import model_info


def get_weight_size(path):
    stats = os.stat(path)
    return f'{stats.st_size / 1024 / 1024:.1f}'


def safe_get_list(x):
    """把结果转成 list，避免 tensor/list/ndarray 兼容问题"""
    if x is None:
        return []
    if isinstance(x, list):
        return x
    try:
        return list(x)
    except:
        return []


def safe_get_value(x, idx, default=0.0):
    """安全取单个元素"""
    try:
        return float(x[idx])
    except:
        return default


def safe_get_ap75(all_ap, idx, default=0.0):
    """
    all_ap 一般对应 IoU=[0.50:0.05:0.95]
    下标 5 对应 0.75
    """
    try:
        return float(all_ap[idx, 5])
    except:
        try:
            return float(all_ap[idx][5])
        except:
            return default


if __name__ == '__main__':
    model_path = r'D:\gsj\ultralytics-yolo11-20251122\ultralytics-yolo11-main\runs\train\exp-8+11+p2\weights\best.pt'
    model = YOLO(model_path) # 选择训练好的权重路径
    result = model.val(data=r'D:\gsj\ultralytics-yolo11-20251122\ultralytics-yolo11-main\data4\data.yaml',
                        split='test', # split可以选择train、val、test 根据自己的数据集情况来选择.
                        imgsz=640,
                        batch=16,
                        conf=0.39,  # ✅ 置信度阈值
                        iou=0.60,  # ✅ NMS IoU阈值
                        max_det=100,  # ✅ 单图最多保留框数
                        # iou=0.7,
                        # rect=False,
                        # save_json=True, # if you need to cal coco metrice
                        project='runs-val/1+mk+abc',
                        name='exp',
                        )

    if model.task == 'detect':
        # ---------- 基础结果 ----------
        p_list = safe_get_list(getattr(result.box, 'p', None))
        r_list = safe_get_list(getattr(result.box, 'r', None))
        f1_list = safe_get_list(getattr(result.box, 'f1', None))
        ap50_list = safe_get_list(getattr(result.box, 'ap50', None))
        ap_list = safe_get_list(getattr(result.box, 'ap', None))
        all_ap = getattr(result.box, 'all_ap', None)

        length = len(p_list)
        model_names = list(result.names.values()) if hasattr(result, 'names') else [f'class_{i}' for i in range(length)]

        preprocess_time_per_image = result.speed.get('preprocess', 0.0)
        inference_time_per_image = result.speed.get('inference', 0.0)
        postprocess_time_per_image = result.speed.get('postprocess', 0.0)
        all_time_per_image = preprocess_time_per_image + inference_time_per_image + postprocess_time_per_image

        n_l, n_p, n_g, flops = model_info(model.model)

        print('-' * 20 + '论文上的数据以以下结果为准' + '-' * 20)
        print('-' * 20 + '论文上的数据以以下结果为准' + '-' * 20)
        print('-' * 20 + '论文上的数据以以下结果为准' + '-' * 20)

        # ---------- 模型信息表 ----------
        model_info_table = PrettyTable()
        model_info_table.title = "Model Info"
        model_info_table.field_names = [
            "GFLOPs",
            "Parameters",
            "前处理时间/一张图",
            "推理时间/一张图",
            "后处理时间/一张图",
            "FPS(前处理+模型推理+后处理)",
            "FPS(推理)",
            "Model File Size"
        ]

        fps_all = 1000 / all_time_per_image if all_time_per_image > 0 else 0
        fps_inf = 1000 / inference_time_per_image if inference_time_per_image > 0 else 0

        model_info_table.add_row([
            f'{flops:.1f}',
            f'{n_p:,}',
            f'{preprocess_time_per_image / 1000:.6f}s',
            f'{inference_time_per_image / 1000:.6f}s',
            f'{postprocess_time_per_image / 1000:.6f}s',
            f'{fps_all:.2f}',
            f'{fps_inf:.2f}',
            f'{get_weight_size(model_path)}MB'
        ])
        print(model_info_table)

        # ---------- 指标表 ----------
        model_metrice_table = PrettyTable()
        model_metrice_table.title = "Model Metrice"
        model_metrice_table.field_names = [
            "Class Name", "Precision", "Recall", "F1-Score", "mAP50", "mAP75", "mAP50-95"
        ]

        valid_len = min(length, len(model_names))

        for idx in range(valid_len):
            model_metrice_table.add_row([
                model_names[idx],
                f"{safe_get_value(p_list, idx):.4f}",
                f"{safe_get_value(r_list, idx):.4f}",
                f"{safe_get_value(f1_list, idx):.4f}",
                f"{safe_get_value(ap50_list, idx):.4f}",
                f"{safe_get_ap75(all_ap, idx):.4f}",
                f"{safe_get_value(ap_list, idx):.4f}",
            ])

        mean_f1 = float(np.mean(f1_list[:valid_len])) if valid_len > 0 and len(f1_list) > 0 else 0.0
        mean_ap75 = 0.0
        if all_ap is not None and valid_len > 0:
            try:
                mean_ap75 = float(np.mean(all_ap[:valid_len, 5]))
            except:
                try:
                    mean_ap75 = float(np.mean([row[5] for row in all_ap[:valid_len]]))
                except:
                    mean_ap75 = 0.0

        results_dict = getattr(result, 'results_dict', {})

        model_metrice_table.add_row([
            "all(平均数据)",
            f"{results_dict.get('metrics/precision(B)', 0.0):.4f}",
            f"{results_dict.get('metrics/recall(B)', 0.0):.4f}",
            f"{mean_f1:.4f}",
            f"{results_dict.get('metrics/mAP50(B)', 0.0):.4f}",
            f"{mean_ap75:.4f}",
            f"{results_dict.get('metrics/mAP50-95(B)', 0.0):.4f}",
        ])
        print(model_metrice_table)

        # ---------- 保存 ----------
        save_path = result.save_dir / 'paper_data.txt'
        with open(save_path, 'w+', errors='ignore', encoding='utf-8') as f:
            f.write(str(model_info_table))
            f.write('\n')
            f.write(str(model_metrice_table))

        print('-' * 20, f'结果已保存至 {save_path} ...', '-' * 20)