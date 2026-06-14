import streamlit as st


class DatasetSelector:

    @staticmethod
    def set_active_dataset(
        dataset_name
    ):

        st.session_state[
            "active_dataset"
        ] = dataset_name

    @staticmethod
    def get_active_dataset():

        return st.session_state.get(
            "active_dataset"
        )

    @staticmethod
    def clear_active_dataset():

        if (
            "active_dataset"
            in st.session_state
        ):

            del st.session_state[
                "active_dataset"
            ]