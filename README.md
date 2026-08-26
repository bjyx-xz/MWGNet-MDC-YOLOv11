[README.md](https://github.com/user-attachments/files/31450917/README.md)
# MWGNet-MDC-YOLOv11

Official repository for:

**MWGNet-MDC-YOLOv11: A Cascaded Framework for Super-Resolution Reconstruction and Multiple Insulator Defect Detection**

This repository provides public materials for reproducible evaluation of the proposed framework, including the held-out test set, complete test annotations, dataset configuration, the exact test-set manifest, the super-resolution training configuration, and the detector evaluation script.

---

## 1. Overview

Low-resolution UAV inspection images may suffer from loss of fine structural details, which can reduce the accuracy of insulator defect detection. To address this problem, we propose a cascaded framework consisting of:

- **MWGNet** for ×4 super-resolution reconstruction;
- **MDC-YOLOv11** for four-class insulator defect detection.

The four dataset labels are:

```yaml
nc: 4
names:
  0: flashover
  1: loose
  2: damaged
  3: dirty
```

For consistency with the terminology used in the manuscript, these labels are referred to as **flashover, loosening, damage, and contamination**, respectively.

---

## 2. Processing Pipeline

The controlled experimental pipeline used in this study is:

```text
Original HR insulator image
        ↓
Bicubic ×4 downsampling
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

In this study, paired naturally degraded LR-HR UAV images were not available. Therefore, the LR images used in the controlled experiments were synthetically generated from the original HR images using ×4 degradation.

MWGNet was first trained using paired LR-HR images. After convergence, the trained MWGNet was fixed and used to reconstruct the LR defect images. The resulting SR images, together with the corresponding original bounding-box annotations, were then used to train MDC-YOLOv11.

Therefore, MWGNet and MDC-YOLOv11 were trained **sequentially without end-to-end joint optimization**.

---

## 3. Dataset

The self-constructed UAV insulator defect dataset contains:

| Split | Number of images |
|---|---:|
| Training | 2,987 |
| Validation | 417 |
| Test | 402 |
| **Total** | **3,806** |

The complete dataset contains **6,461 annotated defect instances** covering four defect categories.

### Dataset label mapping

| Class ID | Dataset label | Manuscript terminology |
|---:|---|---|
| 0 | flashover | flashover |
| 1 | loose | loosening |
| 2 | damaged | damage |
| 3 | dirty | contamination |

All bounding-box annotations are stored in **YOLO format**.

---

## 4. Data Availability

Due to **data-ownership, copyright, and power-grid information confidentiality restrictions** associated with part of the UAV inspection imagery, the complete training and validation subsets cannot be publicly distributed.

Following internal review by the research group, the complete held-out test subset used in this study has been approved for public release.

The publicly released test subset contains:

- **402 test images**;
- **690 annotated defect instances**;
- complete YOLO-format bounding-box annotations;
- a public dataset configuration file;
- an exact manifest listing all 402 test images.

The released test subset is intended to support independent evaluation and verification of the results reported in the manuscript.

The complete public test package is available from the GitHub Releases section:

**Release:** `v1.0-testset`  
**Asset:** `InsulatorDefect_TestSet_v1.0.zip`

https://github.com/bjyx-xz/MWGNet-MDC-YOLOv11/releases/tag/v1.0-testset

A detailed explanation of the data-release restrictions is also provided in:

```text
DATA_AVAILABILITY.md
```

---

## 5. Public Test Package

After downloading and extracting `InsulatorDefect_TestSet_v1.0.zip`, the package contains:

```text
InsulatorDefect_TestSet_v1.0/
│
├── images/
│   └── test/
│       ├── ...
│       └── 402 test images
│
├── labels/
│   └── test/
│       ├── ...
│       └── corresponding YOLO labels
│
└── data_test.yaml
```

Each image in `images/test/` has a corresponding annotation file in `labels/test/`.

The YOLO annotation format is:

```text
class_id x_center y_center width height
```

where the bounding-box coordinates are normalized to the range `[0, 1]`.

---

## 6. Exact Test-Set Manifest

The exact list of the 402 held-out test images is provided separately in the GitHub repository:

```text
dataset/test.txt
```

The entries follow the form:

```text
./images/test/example_001.jpg
./images/test/example_002.jpg
./images/test/example_003.jpg
```

`test.txt` is provided to make the publicly released test split explicit and reproducible.

**Important:** `test.txt` is stored in the GitHub repository and is not required to be inside the Release ZIP package.

---

## 7. Dataset Configuration

Two equivalent usage scenarios are supported.

### 7.1 Configuration inside the extracted Release package

When `data_test.yaml` is placed in the root of the extracted test package, the recommended configuration is:

```yaml
path: .
test: images/test

nc: 4

names:
  0: flashover
  1: loose
  2: damaged
  3: dirty
```

This configuration assumes the following structure:

```text
InsulatorDefect_TestSet_v1.0/
├── images/test/
├── labels/test/
└── data_test.yaml
```

### 7.2 Configuration stored in this GitHub repository

The repository also provides:

```text
dataset/data_test.yaml
```

Its path is configured assuming that `InsulatorDefect_TestSet_v1.0` has been extracted into the repository root:

```text
MWGNet-MDC-YOLOv11/
├── dataset/
│   └── data_test.yaml
└── InsulatorDefect_TestSet_v1.0/
    ├── images/test/
    └── labels/test/
```

Accordingly, the repository configuration uses:

```yaml
path: ../InsulatorDefect_TestSet_v1.0
test: images/test
```

If the dataset is extracted elsewhere, users should update the `path` field accordingly.

---

## 8. Repository Contents

The current public repository contains:

```text
MWGNet-MDC-YOLOv11/
│
├── README.md
├── DATA_AVAILABILITY.md
├── train_MambaIRv2_SR_x4.yml
├── val.py
│
└── dataset/
    ├── data_test.yaml
    └── test.txt
```

The complete 402-image test set and its corresponding labels are distributed through the GitHub Release because of file-size limitations.

---

## 9. Super-Resolution Training Configuration

The file:

```text
train_MambaIRv2_SR_x4.yml
```

contains the main training configuration used for the ×4 super-resolution experiments.

The principal settings are:

- scale factor: ×4;
- training patch size: 192 × 192;
- batch size: 6;
- total iterations: 250,000;
- optimizer: Adam;
- initial learning rate: 1 × 10⁻⁴;
- Adam betas: (0.9, 0.99);
- pixel loss: L1 loss;
- random seed: 10.

The training and validation images are not publicly distributed. Therefore, users attempting to reproduce training with authorized data must replace the local dataset paths in the configuration file with their own accessible dataset paths.

---

## 10. Detector Evaluation

The repository provides:

```text
val.py
```

for evaluating a trained YOLO-based detector.

The detector input resolution used in the study is:

```text
640 × 640
```

The detection task contains four classes:

```text
0 - flashover
1 - loose
2 - damaged
3 - dirty
```

The current public script contains local path examples corresponding to the authors' experimental environment. Users should replace the model-weight path and dataset path with their own local paths before evaluation.

Future repository updates may further convert these path settings to command-line arguments for easier reuse.

---

## 11. Experimental Data Flow

For the cascaded MWGNet-MDC-YOLOv11 experiments, the data flow is:

### Stage 1: LR generation

```text
HR → ×4 degradation → LR
```

### Stage 2: Super-resolution reconstruction

```text
LR → MWGNet → SR
```

### Stage 3: Defect detection

```text
SR → MDC-YOLOv11 → defect predictions
```

For detector training, the reconstructed SR training images were paired with the corresponding original bounding-box annotations.

---

## 12. Evaluation Metrics

### Super-resolution reconstruction

Reconstruction performance is evaluated using:

- Peak Signal-to-Noise Ratio (**PSNR**);
- Structural Similarity Index Measure (**SSIM**);
- Learned Perceptual Image Patch Similarity (**LPIPS**).

### Defect detection

Detection performance is evaluated using:

- Precision;
- Recall;
- F1-score;
- mAP@50;
- mAP@50:95.

---

## 13. Reproducibility Scope

This repository supports **evaluation reproducibility** by providing:

- the complete 402-image held-out test subset;
- all corresponding test annotations;
- the four-class label definition;
- the exact test-set manifest;
- the dataset configuration;
- the main MWGNet training configuration;
- the detector evaluation script;
- a description of the reconstruction-then-detection pipeline.

Because the training and validation images cannot be redistributed under the current data-use restrictions, the repository does **not** provide complete training-data reproducibility for the self-constructed dataset.

---

## 14. Scope and Limitation of the Current Study

The LR images used in the main controlled experiments were synthetically generated from the original HR images. Additional synthetic degradation conditions were also used in the manuscript for robustness evaluation.

These synthetic degradation experiments should not be interpreted as a substitute for validation on genuinely degraded UAV imagery.

The absence of a sufficiently large annotated dataset of naturally degraded UAV insulator images is an acknowledged limitation of the present study. Future work will focus on evaluation using independently acquired and naturally degraded UAV inspection data.

---

## 15. Citation

If this repository or the released test set is useful for your research, please cite the corresponding paper after publication.

```bibtex
@article{MWGNetMDCYOLOv11,
  title   = {MWGNet-MDC-YOLOv11: A Cascaded Framework for Super-Resolution Reconstruction and Multiple Insulator Defect Detection},
  author  = {To be updated},
  journal = {To be updated},
  year    = {2026}
}
```

The citation information will be updated after the paper is formally published.

---

## 16. Acknowledgements

This project was developed using PyTorch, Ultralytics YOLO, and related open-source image-restoration frameworks. We sincerely thank the developers and maintainers of these open-source projects.

---

## 17. License and Usage

The publicly released materials are intended for academic research and reproducibility purposes.

Users must comply with the applicable licenses of third-party code and dependencies.

The unreleased training and validation UAV imagery remains subject to the original data-ownership, copyright, and power-grid information confidentiality restrictions and may not be redistributed.

---

## 18. Contact

For questions related to the repository, dataset evaluation, or the paper, please contact the corresponding author using the contact information provided in the manuscript.
