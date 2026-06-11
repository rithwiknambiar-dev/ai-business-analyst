class ContextBuilder:

    def __init__(self, eda_report, insights):

        self.eda_report = eda_report
        self.insights = insights

    def build_context(self):

        sales_summary = self.eda_report[
            "sales_summary"
        ]

        profit_summary = self.eda_report[
            "profit_summary"
        ]

        region_analysis = self.eda_report[
            "region_analysis"
        ]

        category_analysis = self.eda_report[
            "category_analysis"
        ]

        segment_analysis = self.eda_report[
            "segment_analysis"
        ]

        context = f"""

        BUSINESS DATASET SUMMARY

        Total Sales:
        {sales_summary['total_sales']}

        Average Sales:
        {sales_summary['average_sales']}

        Total Profit:
        {profit_summary['total_profit']}

        Average Profit:
        {profit_summary['average_profit']}

        Best Region:
        {region_analysis['best_region']}

        Worst Region:
        {region_analysis['worst_region']}

        Best Category:
        {category_analysis['best_category']}

        Top Segment:
        {max(
            segment_analysis['sales_by_segment'],
            key=segment_analysis['sales_by_segment'].get
        )}

        BUSINESS INSIGHTS

        """

        for index, insight in enumerate(
            self.insights,
            start=1
        ):

            context += (
                f"\nInsight {index}: "
                f"{insight}\n"
            )

        return context