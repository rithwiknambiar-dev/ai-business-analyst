class DataProfiler:

    def __init__(self, df):
        self.df = df

    def generate_profile(self):

        profile = {

            "rows":
                self.df.shape[0],

            "columns":
                self.df.shape[1],

            "column_names":
                list(self.df.columns),

            "missing_values":
                self.df.isnull().sum().to_dict(),

            "duplicate_rows":
                int(self.df.duplicated().sum()),

            "data_types":
                self.df.dtypes.astype(str).to_dict(),

            "memory_usage_mb":
    float(
        round(
            self.df.memory_usage(
                deep=True
            ).sum() / (1024 * 1024),
            2
        )
    )
        }

        return profile