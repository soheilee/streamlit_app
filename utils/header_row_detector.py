import pandas as pd

class HeaderRowDetector:
    def __init__(self, df, min_numeric_ratio=0.4, min_non_empty_ratio=0.8):
        self.df = df
        self.min_numeric_ratio = min_numeric_ratio
        self.min_non_empty_ratio = min_non_empty_ratio

    def detect(self):
        """
        Detect the number of header rows by identifying the first row that looks like data.
        Assumes data rows have enough numeric and non-empty values.
        """
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            non_empty_ratio = row.notna().mean()
            numeric_ratio = pd.to_numeric(row, errors='coerce').notna().mean()

            if non_empty_ratio >= self.min_non_empty_ratio and numeric_ratio >= self.min_numeric_ratio:
                return i  # i is the index of the first data row, so header rows = i

        return 0  # fallback if no data-like row is found