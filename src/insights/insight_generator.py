class InsightGenerator:

    def __init__(self, eda_report):
        self.eda_report = eda_report

    def generate_region_insight(self):

        region_data = self.eda_report["region_analysis"]

        best_region = region_data["best_region"]
        worst_region = region_data["worst_region"]

        best_sales = region_data["sales_by_region"][best_region]
        worst_sales = region_data["sales_by_region"][worst_region]

        return (
            f"{best_region} region generated the highest revenue "
            f"with sales of {best_sales:,.2f}. "
            f"{worst_region} region generated the lowest revenue "
            f"with sales of {worst_sales:,.2f}."
        )

    def generate_category_insight(self):

        category_data = self.eda_report["category_analysis"]

        best_category = category_data["best_category"]
        worst_category = category_data["worst_category"]

        best_sales = category_data["sales_by_category"][best_category]
        worst_sales = category_data["sales_by_category"][worst_category]

        return (
            f"{best_category} is the top-performing category "
            f"with sales of {best_sales:,.2f}. "
            f"{worst_category} generated the lowest sales "
            f"with {worst_sales:,.2f}."
        )

    def generate_segment_insight(self):

        segment_sales = self.eda_report[
            "segment_analysis"
        ]["sales_by_segment"]

        best_segment = max(
            segment_sales,
            key=segment_sales.get
        )

        sales = segment_sales[best_segment]

        return (
            f"{best_segment} customers contribute the "
            f"largest share of revenue with sales "
            f"of {sales:,.2f}."
        )

    def generate_subcategory_insight(self):

        subcategories = self.eda_report[
            "subcategory_analysis"
        ]["sales_by_subcategory"]

        top_subcategory = next(
            iter(subcategories)
        )

        sales = subcategories[top_subcategory]

        return (
            f"{top_subcategory} is the best-selling "
            f"sub-category with sales of "
            f"{sales:,.2f}."
        )

    def generate_discount_insight(self):

        correlation = self.eda_report[
            "correlation_analysis"
        ]["discount_profit"]

        if correlation < 0:

            return (
                f"Discounts show a negative correlation "
                f"with profit ({correlation}). "
                f"Higher discounts tend to reduce "
                f"profitability."
            )

        return (
            f"Discounts show a positive correlation "
            f"with profit ({correlation})."
        )

    def generate_sales_profit_insight(self):

        total_sales = self.eda_report[
            "sales_summary"
        ]["total_sales"]

        total_profit = self.eda_report[
            "profit_summary"
        ]["total_profit"]

        profit_margin = (
            total_profit / total_sales
        ) * 100

        return (
            f"Total sales amount to "
            f"{total_sales:,.2f} with "
            f"overall profit of "
            f"{total_profit:,.2f}. "
            f"The overall profit margin "
            f"is {profit_margin:.2f}%."
        )

    def generate_all_insights(self):

        insights = [

            self.generate_sales_profit_insight(),

            self.generate_region_insight(),

            self.generate_category_insight(),

            self.generate_segment_insight(),

            self.generate_subcategory_insight(),

            self.generate_discount_insight()

        ]

        return insights