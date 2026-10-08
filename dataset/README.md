# UAV Insulator Defect Test Dataset

This directory provides the configuration files and evaluation manifest
for the publicly released UAV insulator defect test dataset used in:

"MWGNet-MDC-YOLOv11: A Cascaded Framework for Super-Resolution Reconstruction and Multiple Insulator Defect Detection"

## Dataset Availability

The complete held-out test subset is publicly available through the
GitHub Release package:

InsulatorDefect_TestSet_v1.0.zip

Due to file size limitations, the image files and annotations are not
stored directly in this repository directory.

Please download the dataset package from:

../DOWNLOAD_LINK.txt


## Released Dataset Contents

The released test dataset contains:

- 402 UAV insulator defect images;
- 690 annotated defect instances;
- YOLO-format bounding-box annotations;
- dataset configuration files.


## Dataset Structure After Download

After extracting the release package, the structure is:

InsulatorDefect_TestSet_v1.0/

├── images/
│   └── test/
│       ├── xxx.jpg
│       └── ...
│
├── labels/
│   └── test/
│       ├── xxx.txt
│       └── ...
│
└── data_test.yaml


## Label Mapping

The dataset contains four defect categories:

| Class ID | Category |
|----------|----------|
| 0 | flashover |
| 1 | loose |
| 2 | damaged |
| 3 | dirty |


## Annotation Format

All annotations follow the YOLO format:

class_id x_center y_center width height

where all coordinates are normalized to [0,1].


## Evaluation

The provided:

- data_test.yaml
- test.txt

are used for reproducing the evaluation results reported in the paper.
