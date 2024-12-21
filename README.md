# WWZD Project

## Introduction
This project is designed to find, process, and visualize data using various tools and libraries.


## Getting started

### Prerequisites
Before you begin, make sure you have the following tools installed:
- python 3.10 + (latest version recommended: 3.12)
- UV (Universal Virtualenv)

You can install UV using pip:
```bash
pip install uv
```

You can also use standalone installer:

*   windows:
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
*   mac and linux:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    or
    ```bash
    wget -qO- https://astral.sh/uv/install.sh | sh
    ```

### Installation

1. clone the repository:

    ```bash
    git clone https://github.com/domino403/WWZD.git
    ```

2. Create a virtual environment using UV or skip this step if you already have one:

    ```bash
    uv create
    ```

3. Activate it.
4. Install project dependency:
    ```
    uv sync
    ```
     you can use uv sync to manually update the environment


## Used data

*   The raw image dataset used in this project can be found at: https://www.kaggle.com/c/imagenet-object-localization-challenge/overview
*   The model used is EfficientNet_B3.

### Preparing the Dataset

To prepare the dataset using the EfficientNet model, run the following script:

    python data/prepare_data.py

To convert the output JSON file to Parquet format, run:

    python data/save_json_as_parquet.py


To load and transform the data, you can use the scripts in the `src` directory. For example, to load data using the `data_loader` class:

``` python
from src.data_loader import data_loader

loader = data_loader()
```

### Checking Data Library Performance

To check the performance of different data processing libraries, run:

    python src/check_data_lib_performance.py

License
This project is licensed under the MIT License