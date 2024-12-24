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

4. Install pre-commit
    ```
    pre-commit install
    ```
## How to run project
Main function can be called by main.py with command:
```
uv run main.py
```
In case if you want run some other script use:
```
uv run src/path/to/script.py
```

Logs will be stored in file `WWZD.logs` in main directory.

## Used data

*   The raw image dataset used in this project can be found at: https://www.kaggle.com/c/imagenet-object-localization-challenge/overview
*   The model used is EfficientNet_B3.

### Preparing the Dataset

To prepare the dataset using the EfficientNet model, run the following script:

    uv run data/prepare_data.py

To convert the output JSON file to Parquet format, run:

    uv run data/save_json_as_parquet.py


To load and transform the data, you can use the scripts in the `src` directory. For example, to load data using the `data_loader` class:

``` python
from src.data_transformation.data_manager import data_manager

data_loader = data_manager("data/output_data.parquet")
data_loader.load_parquet()

data_loader.prepare_data()

print(data_loader.DataFrame)

```

To get data dim reduction done use one of this function:
- pca_dim_reduction
- t_sne_dim_reduction
- truncated_svd_dim_reduction

``` python
data = pca_dim_reduction(polars_DataFrame, n_components=30)
```
While runing each function for the first time, the output will be saved to the file. Each new run with the same setings will result with loading data from the file in place of processing them again. This was implemented for time saving.

### Checking Data Library Performance

To check the performance of different data processing libraries, run:

    python src/check_data_lib_performance.py

License
This project is licensed under the MIT License
