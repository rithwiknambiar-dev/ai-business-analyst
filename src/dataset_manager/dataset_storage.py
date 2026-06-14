from pathlib import Path
import shutil


class DatasetStorage:

    DATASET_DIRECTORY = Path(
        "data/user_datasets"
    )

    @classmethod
    def initialize(cls):

        cls.DATASET_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True
        )

    @classmethod
    def save_uploaded_file(
        cls,
        uploaded_file
    ):

        cls.initialize()

        destination = (
            cls.DATASET_DIRECTORY
            / uploaded_file.name
        )

        with open(
            destination,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        return destination

    @classmethod
    def get_dataset_path(
        cls,
        dataset_name
    ):

        cls.initialize()

        return (
            cls.DATASET_DIRECTORY
            / dataset_name
        )

    @classmethod
    def list_datasets(cls):

        cls.initialize()

        return sorted(
            [
                file.name
                for file in cls.DATASET_DIRECTORY.iterdir()
                if file.is_file()
            ]
        )

    @classmethod
    def dataset_exists(
        cls,
        dataset_name
    ):

        return cls.get_dataset_path(
            dataset_name
        ).exists()

    @classmethod
    def delete_dataset(
        cls,
        dataset_name
    ):

        dataset_path = cls.get_dataset_path(
            dataset_name
        )

        if dataset_path.exists():

            dataset_path.unlink()