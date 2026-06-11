import pandas as pd


class ExploratoryAnalysis:

    def __init__(self, df):
        self.df = df

    def get_sales_summary(self):

        return {
            "total_sales": round(self.df["Sales"].sum(), 2),
            "average_sales": round(self.df["Sales"].mean(), 2),
            "maximum_sale": round(self.df["Sales"].max(), 2),
            "minimum_sale": round(self.df["Sales"].min(), 2)
        }

    def get_profit_summary(self):

        return {
            "total_profit": round(self.df["Profit"].sum(), 2),
            "average_profit": round(self.df["Profit"].mean(), 2),
            "maximum_profit": round(self.df["Profit"].max(), 2),
            "minimum_profit": round(self.df["Profit"].min(), 2)
        }

    def get_region_analysis(self):

        region_sales = (
            self.df.groupby("Region")["Sales"]
            .sum()
            .round(2)
            .to_dict()
        )

        region_profit = (
            self.df.groupby("Region")["Profit"]
            .sum()
            .round(2)
            .to_dict()
        )

        best_region = max(region_sales, key=region_sales.get)
        worst_region = min(region_sales, key=region_sales.get)

        return {
            "sales_by_region": region_sales,
            "profit_by_region": region_profit,
            "best_region": best_region,
            "worst_region": worst_region
        }

    def get_category_analysis(self):

        category_sales = (
            self.df.groupby("Category")["Sales"]
            .sum()
            .round(2)
            .to_dict()
        )

        category_profit = (
            self.df.groupby("Category")["Profit"]
            .sum()
            .round(2)
            .to_dict()
        )

        best_category = max(
            category_sales,
            key=category_sales.get
        )

        worst_category = min(
            category_sales,
            key=category_sales.get
        )

        return {
            "sales_by_category": category_sales,
            "profit_by_category": category_profit,
            "best_category": best_category,
            "worst_category": worst_category
        }

    def get_segment_analysis(self):

        segment_sales = (
            self.df.groupby("Segment")["Sales"]
            .sum()
            .round(2)
            .to_dict()
        )

        segment_profit = (
            self.df.groupby("Segment")["Profit"]
            .sum()
            .round(2)
            .to_dict()
        )

        return {
            "sales_by_segment": segment_sales,
            "profit_by_segment": segment_profit
        }

    def get_subcategory_analysis(self):

        subcategory_sales = (
            self.df.groupby("Sub-Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .round(2)
            .to_dict()
        )

        return {
            "sales_by_subcategory": subcategory_sales
        }

    def get_discount_analysis(self):

        return {
            "average_discount":
                round(
                    self.df["Discount"].mean(),
                    2
                ),

            "maximum_discount":
                round(
                    self.df["Discount"].max(),
                    2
                )
        }

    def get_correlation_analysis(self):

        correlation_matrix = self.df[
            [
                "Sales",
                "Profit",
                "Quantity",
                "Discount"
            ]
        ].corr()

        return {
            "sales_profit":
                round(
                    correlation_matrix.loc[
                        "Sales",
                        "Profit"
                    ],
                    2
                ),

            "sales_quantity":
                round(
                    correlation_matrix.loc[
                        "Sales",
                        "Quantity"
                    ],
                    2
                ),

            "discount_profit":
                round(
                    correlation_matrix.loc[
                        "Discount",
                        "Profit"
                    ],
                    2
                )
        }

    def generate_eda_report(self):

        report = {

            "sales_summary":
                self.get_sales_summary(),

            "profit_summary":
                self.get_profit_summary(),

            "region_analysis":
                self.get_region_analysis(),

            "category_analysis":
                self.get_category_analysis(),

            "segment_analysis":
                self.get_segment_analysis(),

            "subcategory_analysis":
                self.get_subcategory_analysis(),

            "discount_analysis":
                self.get_discount_analysis(),

            "correlation_analysis":
                self.get_correlation_analysis()
        }

        return report