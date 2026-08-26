# Data Availability

The self-constructed UAV insulator defect dataset used in this study contains 3,806 images and 6,461 annotated defect instances.

The dataset is divided into:

| Split | Images |
|---|---:|
| Training | 2,987 |
| Validation | 417 |
| Test | 402 |
| Total | 3,806 |

Due to data-ownership, copyright, and power-grid information confidentiality restrictions associated with part of the UAV inspection imagery, the complete training and validation subsets cannot be publicly distributed.

Following internal review by the research group, the complete held-out test subset used in this study has been approved for public release.

The publicly released test subset contains:

- 402 test images;
- 690 annotated defect instances;
- complete YOLO-format bounding-box annotations;
- the exact test-set manifest;
- class definitions and dataset configuration;
- instructions for reproducing the evaluation procedure.

The four dataset labels are:

- `0: flashover`
- `1: loose`
- `2: damaged`
- `3: dirty`

In the manuscript, these categories are referred to as flashover, loosening, damage, and contamination, respectively.

The released test subset is intended to support independent evaluation and verification of the results reported in the manuscript.
