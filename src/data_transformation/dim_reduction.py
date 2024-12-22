from functools import wraps

import polars as pl
import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from logging_config import setup_logger


LOGGER = setup_logger()


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
