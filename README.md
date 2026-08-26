MWGNet-MDC-YOLOv11

Official repository for:

MWGNet-MDC-YOLOv11: A Cascaded Framework for Super-Resolution Reconstruction and Multiple Insulator Defect Detection

This repository provides the public materials used to support the reproducibility and independent evaluation of our study, including the held-out test set, complete test annotations, dataset configuration, super-resolution training configuration, and detector evaluation script.

1. Overview

Low-resolution UAV inspection images may suffer from loss of fine structural details, which can reduce the accuracy of insulator defect detection. To address this problem, we propose a cascaded framework consisting of:

MWGNet for ×4 super-resolution reconstruction;

MDC-YOLOv11 for four-class insulator defect detection.

The four defect categories used in the dataset labels are:

nc: 4
names:
  0: flashover
  1: loose
  2: damaged
  3: dirty

For consistency with the terminology used in the manuscript, these four labels are referred to as flashover, loosening, damage, and contamination, respectively.

2. Processing Pipeline

The controlled experimental pipeline used in this study is:

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

In the current study, paired naturally degraded LR-HR UAV images were not available. Therefore, the LR images used in the controlled experiments were synthetically generated from the original HR images using ×4 degradation.

MWGNet was first trained using paired LR-HR images. After convergence, the trained MWGNet was fixed and used to reconstruct the LR defect images. The resulting SR images, together with the corresponding original bounding-box annotations, were then used to train MDC-YOLOv11.

Therefore, MWGNet and MDC-YOLOv11 were trained sequentially without end-to-end joint optimization.

3. Dataset

The self-constructed UAV insulator defect dataset contains:

Split

Number of images

Training

2,987

Validation

417

Test

402

Total

3,806

The complete dataset contains 6,461 annotated defect instances covering four defect categories.

Dataset label mapping

Class ID

Dataset label

Manuscript terminology

0

flashover

flashover

1

loose

loosening

2

damaged

damage

3

dirty

contamination

All bounding-box annotations are stored in YOLO format.

4. Data Availability

Due to data-ownership, copyright, and power-grid information confidentiality restrictions associated with part of the UAV inspection imagery, the complete training and validation subsets cannot be publicly distributed.

Following internal discussion and review by our research group, the complete held-out test subset used in this study has been approved for public release.

The publicly released test subset contains:

402 test images;

690 annotated defect instances;

complete YOLO-format bounding-box annotations;

the dataset configuration file (data_test.yaml);

the exact list of test images (test.txt).

The released test set is intended to support independent evaluation and verification of the results reported in the manuscript.

The complete public test package can be downloaded from the Releases section of this repository:

Release asset: InsulatorDefect_TestSet_v1.0.zip

GitHub Releases:
https://github.com/bjyx-xz/MWGNet-MDC-YOLOv11/releases

For a more detailed explanation of the data-release restrictions, please see DATA_AVAILABILITY.md.

5. Public Test Set Structure

After downloading and extracting InsulatorDefect_TestSet_v1.0.zip, the test set is organized as follows:

InsulatorDefect_TestSet_v1.0/
│
├── images/
│   └── test/
│       ├── image_001.jpg
│       ├── image_002.jpg
│       └── ...
│
├── labels/
│   └── test/
│       ├── image_001.txt
│       ├── image_002.txt
│       └── ...
│
├── test.txt
└── data_test.yaml

Each image in images/test/ has a corresponding YOLO-format annotation file in labels/test/.

The annotation format is:

class_id x_center y_center width height

where all bounding-box coordinates are normalized to the range [0, 1].

6. Dataset Configuration

The public test-set configuration is provided in data_test.yaml.

Example:

path: .

test: images/test

nc: 4

names:
  0: flashover
  1: loose
  2: damaged
  3: dirty

If the extracted dataset is moved to another directory, update the dataset path accordingly.

7. Test-Set Manifest

The file test.txt lists the exact 402 images included in the held-out test subset.

Example:

./images/test/example_001.jpg
./images/test/example_002.jpg
./images/test/example_003.jpg

The purpose of this file is to make the test split explicit and reproducible.

8. Repository Contents

The repository currently provides the following public materials:

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

The complete 402-image public test set and its annotations are distributed separately through the GitHub Releases section because of file-size limitations.

9. Super-Resolution Training Configuration

The file:

train_MambaIRv2_SR_x4.yml

contains the main training configuration used for the ×4 super-resolution reconstruction experiments.

The main settings include:

scale factor: ×4;

training patch size: 192 × 192;

batch size: 6;

total iterations: 250,000;

optimizer: Adam;

initial learning rate: 1 × 10⁻⁴;

Adam betas: (0.9, 0.99);

pixel loss: L1 loss;

random seed: 10.

Because the training and validation images are restricted, the local dataset paths in the configuration file must be replaced with authorized local paths before training.

10. Detector Evaluation

The repository provides val.py for evaluating a trained YOLO-based detector.

The detector input resolution used in the study is:

640 × 640

The detection task contains four classes:

0 - flashover
1 - loose
2 - damaged
3 - dirty

Before running the evaluation script, users should replace local model-weight and dataset paths with their own paths or modify the script to accept command-line arguments.

The public test subset can be used for independent detector evaluation with the released annotations.

11. Experimental Data Flow

For the cascaded MWGNet-MDC-YOLOv11 experiments, the data flow is summarized below.

Stage 1: LR generation

The original HR image is degraded using ×4 downsampling to generate the corresponding LR image.

HR → ×4 degradation → LR

Stage 2: Super-resolution reconstruction

The LR image is reconstructed using MWGNet.

LR → MWGNet → SR

Stage 3: Defect detection

The reconstructed SR image is used as the input to MDC-YOLOv11.

SR → MDC-YOLOv11 → defect predictions

For detector training, the reconstructed SR training images are paired with the corresponding original bounding-box annotations.

12. Evaluation Metrics

Super-resolution reconstruction

The reconstruction performance is evaluated using:

Peak Signal-to-Noise Ratio (PSNR);

Structural Similarity Index Measure (SSIM);

Learned Perceptual Image Patch Similarity (LPIPS).

Defect detection

The detection performance is evaluated using:

Precision;

Recall;

F1-score;

mAP@50;

mAP@50:95.

The same held-out test subset is used for controlled comparisons among the relevant input conditions.

13. Reproducibility Notes

To support independent verification of the reported evaluation results, this repository provides or publicly releases:

the complete 402-image held-out test subset;

all corresponding test annotations;

the four-class label definition;

the exact test-set manifest;

the dataset configuration;

the main MWGNet training configuration;

the detector evaluation script;

the description of the reconstruction-then-detection pipeline.

Because the training and validation images cannot be redistributed under the current data-use restrictions, this repository supports evaluation reproducibility rather than complete reproduction of model training from the original private dataset.

14. Scope and Limitation of the Released Data

The LR images used in the main controlled experiments were synthetically generated from the original HR images. Additional synthetic degradation conditions were also used in the manuscript to evaluate robustness.

These synthetic degradation experiments should not be interpreted as a substitute for validation on genuinely degraded UAV imagery.

The absence of a sufficiently large annotated dataset of naturally degraded UAV insulator images is an acknowledged limitation of the present study. Future work will focus on evaluation using independently acquired and naturally degraded UAV inspection data.

15. Citation

If this repository or the released test set is useful for your research, please cite the corresponding paper after publication.

@article{MWGNetMDCYOLOv11,
  title   = {MWGNet-MDC-YOLOv11: A Cascaded Framework for Super-Resolution Reconstruction and Multiple Insulator Defect Detection},
  author  = {To be updated},
  journal = {To be updated},
  year    = {2026}
}

The citation information will be updated after the paper is formally published.

16. Acknowledgements

This project was developed using PyTorch, Ultralytics YOLO, and related open-source image-restoration frameworks. We sincerely thank the developers and maintainers of these open-source projects.

17. License and Usage

The publicly released materials are intended for academic research and reproducibility purposes.

Users must comply with the applicable licenses of third-party code and dependencies.

The unreleased training and validation UAV imagery remains subject to the original data-ownership, copyright, and power-grid information confidentiality restrictions and may not be redistributed.

18. Contact

For questions related to the repository, dataset evaluation, or the paper, please contact the corresponding author through the contact information provided in the manuscript.
