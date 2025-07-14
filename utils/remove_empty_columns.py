class EmptyColumnRemover:
    def __init__(self, df, threshold_column=0.5):
        self.df = df
        self.threshold_column = threshold_column

    def remove(self):
        # Ensure column names are strings
        self.df.columns = self.df.columns.map(str)

        # Drop columns exceeding the missing data threshold
        missing_percentage_columns = self.df.isna().mean()
        filtered_df = self.df.loc[:, missing_percentage_columns <= self.threshold_column]

        # Drop columns that contain "Gut" (case-insensitive)
        filtered_df = filtered_df.loc[:, ~filtered_df.apply(
            lambda col: col.astype(str).str.contains('Gut', case=False, na=False).any()
        )]

        return filtered_df
