# MWGNet-MDC-YOLOv11

Public reproducibility materials for:

**MWGNet-MDC-YOLOv11: A Cascaded Framework for Super-Resolution Reconstruction and Multiple Insulator Defect Detection**

This repository provides the public materials released with the study, including the held-out UAV insulator defect test set, complete test annotations, exact test manifest, dataset configuration, the original bicubic ×4 degradation script, detector evaluation script, experimental configuration, dependency information, and pretrained model weights.

---

## 1. Overview

Low-resolution UAV inspection images may lose fine structural and boundary information, which can reduce the accuracy of insulator defect detection. The proposed framework follows a reconstruction-then-detection strategy and consists of:

- **MWGNet** for ×4 super-resolution reconstruction;
- **MDC-YOLOv11** for four-class insulator defect detection.

The four labels used in the released dataset are:

```yaml
nc: 4

names:
  0: flashover
  1: loose
  2: damaged
  3: dirty
```

For consistency with the manuscript terminology, these labels are referred to as **flashover, loosening, damage, and contamination**, respectively.

---

## 2. Experimental Pipeline

The controlled experimental pipeline is:

```text
Original HR insulator image
        ↓
RGB conversion
        ↓
Crop width/height to values divisible by 4
        ↓
Pillow bicubic ×4 downsampling
        ↓
Synthetic LR image
        ↓
MWGNet
        ↓
Reconstructed SR image
        ↓
MDC-YOLOv11
        ↓
Four-class defect detection
```

Paired naturally degraded LR-HR UAV images were not available in the present study. Therefore, the LR images used in the controlled experiments were synthetically generated from the original HR images.

MWGNet was first trained using paired LR-HR images. After convergence, the trained MWGNet was fixed and used to reconstruct LR defect images. The resulting SR images, together with the corresponding bounding-box annotations, were then used for MDC-YOLOv11 training and evaluation.

Thus, MWGNet and MDC-YOLOv11 were trained **sequentially without end-to-end joint optimization**.

---

## 3. Dataset

The self-constructed UAV insulator defect dataset contains **3,806 images** and **6,461 annotated defect instances**.

| Split | Number of images |
|---|---:|
| Training | 2,987 |
| Validation | 417 |
| Test | 402 |
| **Total** | **3,806** |

### Label mapping

| Class ID | Dataset label | Manuscript terminology |
|---:|---|---|
| 0 | flashover | flashover |
| 1 | loose | loosening |
| 2 | damaged | damage |
| 3 | dirty | contamination |

All released bounding-box annotations use the standard YOLO format:

```text
class_id x_center y_center width height
```

The bounding-box coordinates are normalized to `[0, 1]`.

---

## 4. Data Availability

Due to **data-ownership, copyright, and power-grid information confidentiality restrictions** associated with part of the UAV inspection imagery, the complete training and validation subsets cannot be publicly distributed.

Following internal review by the research group, the complete held-out test subset used in this study has been approved for public release.

The publicly released test subset contains:

- **402 test images**;
- **690 annotated defect instances**;
- complete YOLO-format bounding-box annotations;
- a dataset configuration file;
- an exact manifest listing all 402 test images.

A detailed explanation is provided in:

```text
DATA_AVAILABILITY.md
```

This release is intended to support independent evaluation and verification of the results reported in the manuscript.

---

## 5. Release Assets

The public test set and pretrained weights are available in:

**Release:** `v1.0-testset`

https://github.com/bjyx-xz/MWGNet-MDC-YOLOv11/releases/tag/v1.0-testset

### Available assets

| File | Description |
|---|---|
| `InsulatorDefect_TestSet_v1.0.zip` | Complete 402-image held-out test set with annotations |
| `MWGNet_x4_best.pth` | Pretrained MWGNet ×4 reconstruction weights |
| `MDC_YOLOv11_best.pt` | Pretrained MDC-YOLOv11 detector weights |

### SHA-256 checksums

```text
InsulatorDefect_TestSet_v1.0.zip
ffd1254f3b2b2132dc30b87ab2324fd6e72e21a71d1120af92006a7094430f9e

MWGNet_x4_best.pth
5ad89d612b88821a3b253486f5aa0feba39283c4780329d64f190f4f4d32bb74

MDC_YOLOv11_best.pt
5b22d1a05d56beb05337bff9fcf60416ab3b0e8b603b04fdbf9d028d4aff64bb
```

---

## 6. Repository Structure

The current public repository is organized as follows:

```text
MWGNet-MDC-YOLOv11/
│
├── README.md
├── DATA_AVAILABILITY.md
├── requirements.txt
├── train_MambaIRv2_SR_x4.yml
├── val.py
│
├── dataset/
│   ├── data_test.yaml
│   └── test.txt
│
└── degradation/
    └── generate_bicubic_x4.py
```

Large files, including the complete public test set and pretrained weights, are distributed through GitHub Releases.

---

## 7. Installation

Clone the repository:

```bash
git clone https://github.com/bjyx-xz/MWGNet-MDC-YOLOv11.git
cd MWGNet-MDC-YOLOv11
```

Install the listed dependencies:

```bash
pip install -r requirements.txt
```

The current public dependency file specifies the principal experimental/evaluation packages, including:

```text
torch==2.0.0
ultralytics==8.3.6
opencv-python
numpy
prettytable
```

The bicubic degradation script also uses **Pillow**. If Pillow is not already installed in the environment, install it with:

```bash
pip install Pillow
```

> For strict reproducibility, users should use package versions compatible with the released model weights and the experimental environment.

---

## 8. Preparing the Public Test Set

Download:

```text
InsulatorDefect_TestSet_v1.0.zip
```

from the GitHub Release and extract it into the repository root.

Recommended layout:

```text
MWGNet-MDC-YOLOv11/
│
├── dataset/
│   ├── data_test.yaml
│   └── test.txt
│
├── InsulatorDefect_TestSet_v1.0/
│   ├── images/
│   │   └── test/
│   ├── labels/
│   │   └── test/
│   └── data_test.yaml
│
├── degradation/
├── val.py
└── ...
```

The repository-level configuration:

```text
dataset/data_test.yaml
```

assumes that the extracted test package is named:

```text
InsulatorDefect_TestSet_v1.0
```

and is placed in the repository root.

Its test path is configured as:

```yaml
path: ../InsulatorDefect_TestSet_v1.0
test: images/test
```

If you extract the dataset elsewhere, update the `path` entry accordingly.

---

## 9. Exact Test Manifest

The exact list of the 402 held-out test images is provided in:

```text
dataset/test.txt
```

Each entry follows the form:

```text
./images/test/example_001.jpg
./images/test/example_002.jpg
./images/test/example_003.jpg
```

The manifest makes the released evaluation subset explicit and independently checkable.

---

## 10. Exact Bicubic ×4 Degradation Procedure

The exact degradation script used to reproduce the synthetic LR generation procedure is provided at:

```text
degradation/generate_bicubic_x4.py
```

The preprocessing follows the original experimental code:

1. load each HR image using Pillow;
2. convert the image to RGB;
3. crop the right and bottom boundaries so that width and height are divisible by the scale factor;
4. downsample using **Pillow bicubic interpolation**;
5. save the generated LR image as PNG.

Run:

```bash
python degradation/generate_bicubic_x4.py \
    --hr-dir InsulatorDefect_TestSet_v1.0/images/test \
    --lr-dir LR_bicubic_x4/test \
    --scale 4 \
    --save-ext .png
```

Windows CMD:

```bat
python degradation/generate_bicubic_x4.py --hr-dir InsulatorDefect_TestSet_v1.0/images/test --lr-dir LR_bicubic_x4/test --scale 4 --save-ext .png
```

The resulting process is:

```text
HR → RGB → mod-crop → Pillow BICUBIC ×4 → LR PNG
```

---

## 11. Super-Resolution Configuration

The file:

```text
train_MambaIRv2_SR_x4.yml
```

contains the principal ×4 super-resolution training configuration.

The current configuration includes settings such as:

- scale factor: ×4;
- training patch size: 192 × 192;
- batch size: 6;
- total iterations: 250,000;
- optimizer: Adam;
- initial learning rate: `1e-4`;
- Adam betas: `(0.9, 0.99)`;
- pixel loss: L1;
- random seed: 10.

Because the private training and validation images cannot be redistributed, local authorized paths must be substituted when reproducing model training.

---

## 12. Pretrained Weights

Download the following two files from the Release:

```text
MWGNet_x4_best.pth
MDC_YOLOv11_best.pt
```

For convenience, place them in the repository root or a local `weights/` directory:

```text
MWGNet-MDC-YOLOv11/
└── weights/
    ├── MWGNet_x4_best.pth
    └── MDC_YOLOv11_best.pt
```

When using another location, update the command-line path accordingly.

---

## 13. MDC-YOLOv11 Evaluation

The public detector evaluation script is:

```text
val.py
```

The default evaluation settings reproduce the values preserved from the original evaluation script:

```text
imgsz   = 640
batch   = 16
conf    = 0.39
iou     = 0.55
max_det = 200
split   = test
```

Example:

```bash
python val.py \
    --weights weights/MDC_YOLOv11_best.pt \
    --data dataset/data_test.yaml \
    --imgsz 640 \
    --batch 16 \
    --conf 0.39 \
    --iou 0.55 \
    --max-det 200
```

Windows CMD:

```bat
python val.py --weights weights/MDC_YOLOv11_best.pt --data dataset/data_test.yaml --imgsz 640 --batch 16 --conf 0.39 --iou 0.55 --max-det 200
```

The script reports:

- model GFLOPs;
- parameter count;
- preprocessing time;
- inference time;
- postprocessing time;
- FPS;
- model file size;
- class-wise Precision;
- class-wise Recall;
- class-wise F1-score;
- class-wise mAP@50;
- class-wise mAP@75;
- class-wise mAP@50:95;
- overall detection metrics.

It also records the Python, PyTorch, CUDA, Ultralytics, and NumPy versions used during evaluation and saves the output to:

```text
paper_data.txt
```

inside the Ultralytics validation result directory.

---

## 14. Evaluation Metrics

### Super-resolution reconstruction

The reconstruction experiments use:

- Peak Signal-to-Noise Ratio (**PSNR**);
- Structural Similarity Index Measure (**SSIM**);
- Learned Perceptual Image Patch Similarity (**LPIPS**).

### Defect detection

The detection experiments use:

- Precision;
- Recall;
- F1-score;
- mAP@50;
- mAP@50:95.

Additional mAP@75 reporting is available in the public detector evaluation script.

---

## 15. Reproducibility Scope

The public repository currently supports **evaluation-level reproducibility** by providing:

- the complete held-out test subset;
- all test annotations;
- the exact test manifest;
- class definitions;
- public dataset configuration;
- the original bicubic ×4 degradation procedure;
- super-resolution training configuration;
- pretrained MWGNet weights;
- pretrained MDC-YOLOv11 weights;
- detector evaluation script;
- dependency information;
- a documented reconstruction-then-detection experimental pipeline.

The repository does **not** provide the private training and validation UAV images because they are subject to the data-use restrictions described above.

Accordingly, the public release is intended primarily for **independent evaluation and verification**, rather than complete reproduction of training from the original private dataset.

---

## 16. Current Study Limitation

The primary LR images used in the controlled experiments were generated synthetically from the original HR images.

Although additional synthetic degradation conditions are examined in the manuscript for robustness analysis, these synthetic tests should not be interpreted as a substitute for evaluation on genuinely degraded UAV inspection imagery.

The lack of a sufficiently large annotated dataset of naturally degraded UAV insulator images is an acknowledged limitation of the current study. Future work will prioritize independent evaluation using naturally degraded UAV inspection data.

---

## 17. Citation

If this repository or the released test set is useful for your research, please cite the corresponding paper after formal publication.

```bibtex
@article{MWGNetMDCYOLOv11,
  title   = {MWGNet-MDC-YOLOv11: A Cascaded Framework for Super-Resolution Reconstruction and Multiple Insulator Defect Detection},
  author  = {To be updated},
  journal = {To be updated},
  year    = {2026}
}
```

The bibliographic information will be updated after publication.

---

## 18. Acknowledgements

This work uses PyTorch, Ultralytics YOLO, Pillow, OpenCV, and related open-source image restoration and object detection frameworks. We thank the corresponding open-source communities and developers.

---

## 19. License and Usage

The publicly released materials are intended for academic research and reproducibility purposes.

Users are responsible for complying with the licenses of all third-party dependencies.

The unreleased training and validation UAV imagery remains subject to the original data-ownership, copyright, and power-grid information confidentiality restrictions and may not be redistributed.

---

## 20. Contact

For questions regarding the public test set, evaluation procedure, or manuscript, please contact the corresponding author using the contact information provided in the paper.
