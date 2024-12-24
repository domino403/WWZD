from functools import wraps
import os

import polars as pl
import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from logging_config import setup_logger
from src.data_transformation.data_manager import data_manager


LOGGER = setup_logger()
DIM_RED_DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "..", "data", "dim_reduction"
    )
)


def data_dir_check():
    """
    Check if the directory for dimension reduction data exists.
    If it does not exist, create the directory.

    Logs:
        - Info: If the directory exists.
        - Warning: If the directory does not exist and is created.
    """
    if os.path.exists(DIM_RED_DATA_DIR):
        LOGGER.info(
            f"'{DIM_RED_DATA_DIR}' exists in your project. All dimension reduction results will be saved there"
        )
    else:
        os.mkdir(DIM_RED_DATA_DIR)
        LOGGER.warning(
            f"Program didn't find '{DIM_RED_DATA_DIR}'. New directory will be created and reused in the future!"
        )


def save_load_logic(func):
    """
    Decorator to handle saving and loading of dimension reduction results.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function that saves and loads results from a file.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> pl.DataFrame:
        data_dir_check()
        print(len(args))
        print(args[1])

        file_name = func.__name__.split("_dim")[0]
        if len(args) > 2:
            file_name = file_name + "_" + "_".join(args[1:]) + ".parquet"
        elif len(args) == 2:
            file_name = file_name + "_" + str(args[1]) + ".parquet"
        else:
            file_name = file_name + ".parquet"

        file_path = os.path.join(DIM_RED_DATA_DIR, file_name)

        data_manager_dim = data_manager(file_path)

        LOGGER.info(f"check if data file - '{file_name}' was already created.")
        if os.path.isfile(file_path):
            LOGGER.info(
                "Found ready data file. Try to load it instead to procces new one!"
            )
            try:
                data_manager_dim.load_parquet()
                LOGGER.info("Returning historicall data!")

                return data_manager_dim.DataFrame

            except Exception as e:
                LOGGER.warning(
                    f"Found existing file '{file_name}' but while loading something went wrong: {e}"
                )
                LOGGER.warning("Program will try to create new data file!")

        data_manager_dim.DataFrame = func(*args, **kwargs)

        data_manager_dim.save_dataframe_to_file(file_path)
        LOGGER.info(f"Data saved to '{file_path}'")
        return data_manager_dim.DataFrame

    return wrapper


def polar_to_numpy(func):
    """
    Decorator function to convert Polars DataFrame to NumPy array after removing 'image_ID' column.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: The wrapped function with Polars DataFrame converted to NumPy array.
    """

    @wraps(func)
    def wrapper(data: pl.DataFrame, *args, **kwargs) -> pl.DataFrame:
        try:
            LOGGER.info("Removing 'image_ID' column")
            if "image_ID" in data.columns:
                data_droped = data.drop("image_ID")
            else:
                data_droped = data

            LOGGER.info("Converting Polars DataFrame to NumPy array.")
            data_numpy = data_droped.to_numpy()

            func_result = func(data_numpy, *args, **kwargs)

            LOGGER.info(
                "Converting NumPy array to Polars DataFrame, adding 'image_ID' column back."
            )
            return pl.DataFrame(func_result).with_columns([data["image_ID"]])
        except Exception as e:
            LOGGER.error(f"Error in {func.__name__}: {e}")
            raise e

    return wrapper


def normalize_data(data: np.ndarray) -> np.ndarray:
    LOGGER.info("Normalizing data")
    scaler = StandardScaler()
    return scaler.fit_transform(data)


@save_load_logic
@polar_to_numpy
def pca_dim_reduction(
    data: np.ndarray, n_components: int, normalize: bool = False
) -> np.ndarray:
    """
    Perform PCA dimensionality reduction on the input data.

    Parameters:
    - data: np.ndarray - Input data.
    - n_components: int - Number of components to keep.
    - normalize: bool - Whether to normalize the data before PCA.

    Returns:
    - np.ndarray - Data after PCA dimensionality reduction.
    """
    LOGGER.info("## PCA Dimensionality Reduction ##")
    LOGGER.info(f"Number of components to keep: '{n_components}'")

    pca = PCA(n_components=n_components)

    if normalize:
        data = normalize_data(data)

    data_pca = pca.fit_transform(data)

    LOGGER.info(f"Output data shape: '{data_pca.shape}'")

    return data_pca


@save_load_logic
@polar_to_numpy
def t_sne_dim_reduction(
    data: np.ndarray,
    n_components: int,
    normalize: bool = False,
    perplexity: float = 30.0,
    learning_rate: float = 200.0,
    random_state: int = None,
) -> np.ndarray:
    """
    Perform t-SNE dimensionality reduction on the input data.

    Parameters:
    - data: np.ndarray - Input data.
    - n_components: int - Number of components to keep.
    - normalize: bool - Whether to normalize the data before t-SNE.
    - perplexity: float - The perplexity parameter.
    - learning_rate: float - The learning rate parameter.
    - random_state: int - Random state for reproducibility.

    Returns:
    - np.ndarray - Data after t-SNE dimensionality reduction.
    """
    LOGGER.info("## t-SNE Dimensionality Reduction ##")
    LOGGER.info(f"Number of components to keep: '{n_components}'")

    t_sne = TSNE(
        n_components=n_components,
        perplexity=perplexity,
        learning_rate=learning_rate,
        random_state=random_state,
    )

    if normalize:
        data = normalize_data(data)

    data_t_sne = t_sne.fit_transform(data)

    LOGGER.info(f"Output data shape: '{data_t_sne.shape}'")

    return data_t_sne


@save_load_logic
@polar_to_numpy
def truncated_svd_dim_reduction(
    data: np.ndarray,
    n_components: int,
    normalize: bool = False,
    random_state: int = None,
    density_threshold: float = 0.0,
) -> np.ndarray:
    """
    Perform Truncated SVD dimensionality reduction on the input data.

    Parameters:
    - data: np.ndarray - Input data.
    - n_components: int - Number of components to keep.
    - normalize: bool - Whether to normalize the data before Truncated SVD.
    - random_state: int - Random state for reproducibility.
    - density_threshold: float - Set values to zero when this value smaller than density_threshold.

    Returns:
    - np.ndarray - Data after Truncated SVD dimensionality reduction.
    """
    LOGGER.info("## Truncated SVD Dimensionality Reduction ##")
    LOGGER.info(f"Number of components to keep: {n_components}")

    svd = TruncatedSVD(n_components=n_components, random_state=random_state)

    if density_threshold > 0.0:
        LOGGER.info(
            f"Set values to zero when this value smaller than '{density_threshold}'"
        )
        data[data < density_threshold] = 0.0

    if normalize:
        data = normalize_data(data)

    data_svd = svd.fit_transform(data)

    LOGGER.info(f"Output data shape: '{data_svd.shape}'")

    return data_svd
