import os

from logging_config import setup_logger

from src.data_transformation.data_manager import data_manager
from src.visualisation.plotly_raport import VisualizationApp


LOGGER = setup_logger()


if __name__ == "__main__":
    LOGGER.info("===================================")
    LOGGER.info("Starting main.py!")
    LOGGER.info("===================================")
    LOGGER.info(f"Current working directory: '{os.getcwd()}'")
    data_loader = data_manager("data/output_data.parquet")
    data_loader.load_parquet()
    LOGGER.info("Data loading completed.")
    data_loader.prepare_data()
    LOGGER.info("Data preparation completed.")

    # pca_100_3 = pca_dim_reduction(data_loader.DataFrame.head(100), 3)

    viz_app = VisualizationApp(
        data=data_loader.DataFrame,
        x_col="column_0",
        y_col="column_1",
        z_col="column_2",
        id_col="image_ID",
        images_dir=os.path.abspath("data/vis_images/"),
    )
    viz_app.app.run_server()
    # print(pca_100_3)

    # visualize_scatter_3d(pca_100_3, "column_0", "column_1", "column_2", id_col='image_ID')
    # visualise_with_images(pca_100_3, "column_0", "column_1", "column_2", id_col='image_ID', images_dir='data/vis_images/')
    # TODO: Implement dimensionality reduction

    # TODO: data visualisation
