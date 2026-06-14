import json
from pathlib import Path
from datetime import datetime


class DatasetRegistry:

    REGISTRY_PATH = Path(
        "data/user_datasets/dataset_registry.json"
    )

    @classmethod
    def initialize(cls):

        cls.REGISTRY_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not cls.REGISTRY_PATH.exists():

            cls.REGISTRY_PATH.write_text(
                "[]",
                encoding="utf-8"
            )

    @classmethod
    def load_registry(cls):

        cls.initialize()

        with open(
            cls.REGISTRY_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @classmethod
    def save_registry(
        cls,
        registry
    ):

        cls.initialize()

        with open(
            cls.REGISTRY_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                registry,
                file,
                indent=4
            )

    @classmethod
    def register_dataset(
        cls,
        dataset_metadata
    ):

        registry = cls.load_registry()

        registry = [
            item
            for item in registry
            if item["dataset_name"]
            != dataset_metadata["dataset_name"]
        ]

        registry.append(
            dataset_metadata
        )

        cls.save_registry(
            registry
        )

    @classmethod
    def get_all_datasets(cls):

        return cls.load_registry()

    @classmethod
    def get_dataset(
        cls,
        dataset_name
    ):

        registry = cls.load_registry()

        for dataset in registry:

            if (
                dataset["dataset_name"]
                == dataset_name
            ):

                return dataset

        return None