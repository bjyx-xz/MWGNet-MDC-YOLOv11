# MWGNet-MDC-YOLOv11

Official PyTorch implementation of **MWGNet-MDC-YOLOv11: A Cascaded Super-Resolution and Detection Framework for Insulator Defect Detection**.

This repository provides the source code, model configuration files, training scripts, and evaluation scripts used in our study.

## Overview

The proposed framework consists of two stages:

1. **MWGNet**, which reconstructs high-resolution insulator images from low-resolution inputs.
2. **MDC-YOLOv11**, which detects four types of insulator defects from the reconstructed images.

The four defect categories are:

* Flashover
* Loosening
* Damage
* Contamination

## Framework

The complete processing pipeline is:

```text
Low-resolution image
        ↓
Bicubic ×4 upsampling
        ↓
MWGNet super-resolution reconstruction
        ↓
MDC-YOLOv11 defect detection
        ↓
Defect category and bounding box
```

## Repository Structure

```text
MWGNet-MDC-YOLOv11/
├── README.md
├── requirements.txt
├── configs/
│   ├── MWGNet_x4.yml
│   └── MDC-YOLOv11.yaml
├── models/
│   ├── MWGNet/
│   └── MDC_YOLOv11/
├── scripts/
│   ├── train_sr.py
│   ├── test_sr.py
│   ├── train_detector.py
│   └── test_detector.py
└── utils/
```

The actual file structure may vary slightly depending on the final release version.

## Environment

The code was developed using:

* Python 3.10
* PyTorch
* CUDA
* Ultralytics
* OpenCV

A CUDA-enabled GPU is recommended for model training.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/MWGNet-MDC-YOLOv11.git
cd MWGNet-MDC-YOLOv11
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

Using Conda:

```bash
conda create -n mwgnet-yolo python=3.10 -y
conda activate mwgnet-yolo
```

### 3. Install PyTorch

Install the PyTorch version compatible with your CUDA environment from the official PyTorch website.

For example:

```bash
pip install torch torchvision torchaudio
```

### 4. Install other dependencies

```bash
pip install -r requirements.txt
```

## Dataset Preparation

The dataset should be organized as follows:

```text
datasets/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
└── data.yaml
```

The dataset contains four classes:

```yaml
names:
  0: flashover
  1: loosening
  2: damage
  3: contamination
```

The dataset partition used in the paper is:

| Dataset split  | Number of images |
| -------------- | ---------------: |
| Training set   |            2,987 |
| Validation set |              417 |
| Test set       |              402 |
| Total          |            3,806 |

Due to the licensing restrictions of some source datasets, the original images may not be redistributed directly. Detailed data-source information and dataset-preparation instructions will be provided separately.

## Training MWGNet

Before training, modify the dataset path and training parameters in:

```text
configs/MWGNet_x4.yml
```

Run:

```bash
python scripts/train_sr.py --config configs/MWGNet_x4.yml
```

The super-resolution model is trained for ×4 image reconstruction.

## Testing MWGNet

Run:

```bash
python scripts/test_sr.py \
    --config configs/MWGNet_x4.yml \
    --weights path/to/MWGNet_x4.pth
```

Replace `path/to/MWGNet_x4.pth` with the actual model-weight path.

## Training MDC-YOLOv11

Before training, modify the dataset path in the dataset configuration file.

Run:

```bash
python scripts/train_detector.py \
    --model configs/MDC-YOLOv11.yaml \
    --data path/to/data.yaml
```

Replace `path/to/data.yaml` with the actual dataset configuration path.

## Testing MDC-YOLOv11

Run:

```bash
python scripts/test_detector.py \
    --weights path/to/best.pt \
    --data path/to/data.yaml
```

## Pretrained Weights

The pretrained weights of MWGNet and MDC-YOLOv11 will be provided in the release section of this repository.

The expected files are:

```text
weights/
├── MWGNet_x4.pth
└── MDC-YOLOv11_best.pt
```

## Reproducibility

To improve experimental reproducibility, the repository will provide:

* Model source code
* Model configuration files
* Training and testing scripts
* Fixed dataset-split information
* Data-preprocessing scripts
* Complex-degradation generation scripts
* Evaluation instructions
* Pretrained model weights

The random seed used for dataset degradation generation is:

```text
10
```

## Results

The proposed framework is evaluated using super-resolution and object-detection metrics, including:

* PSNR
* SSIM
* LPIPS
* Precision
* Recall
* F1-score
* mAP@50
* mAP@50:95

Detailed results are reported in the corresponding paper.

## Citation

If this repository is useful for your research, please cite our paper:

```bibtex
@article{author2026mwgnet,
  title={MWGNet-MDC-YOLOv11: A Cascaded Super-Resolution and Detection Framework for Insulator Defect Detection},
  author={Author Name and Coauthor Name},
  journal={IEEE Access},
  year={2026},
  note={Under review}
}
```

The citation information will be updated after the paper is formally published.

## Acknowledgements

This project is developed based on PyTorch, Ultralytics YOLO, and related open-source image-restoration frameworks. We sincerely thank the developers of these open-source projects.

## License

This repository is released for academic research purposes.

Please check the licenses of the original datasets and third-party code before redistributing or using them for commercial purposes.

## Contact

For questions about this repository, please contact:

```text
Name: YOUR NAME
Email: YOUR EMAIL
```
