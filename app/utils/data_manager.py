import streamlit as st
import pandas as pd


class DataManager:

    @staticmethod
    def save_uploaded_data(uploaded_file):

        if uploaded_file is None:
            return None

        try:

            df = pd.read_csv(
                uploaded_file,
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            df = pd.read_csv(
                uploaded_file,
                encoding="latin1"
            )

        date_columns = [
            "Order Date",
            "Ship Date"
        ]

        for column in date_columns:

            if column in df.columns:

                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

        st.session_state[
            "uploaded_df"
        ] = df

        return df

    @staticmethod
    def get_data():

        if (
            "uploaded_df"
            in st.session_state
        ):

            return st.session_state[
                "uploaded_df"
            ]

        return None