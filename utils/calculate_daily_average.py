import pandas as pd

class DailyAverageCalculator:
    def __init__(self, df):
        self.df = df

    def calculate(self):
        # Convert first column to datetime.date
        self.df.iloc[:, 0] = pd.to_datetime(self.df.iloc[:, 0], errors='coerce').dt.date
        
        # Convert the rest of the columns to numeric, coercing errors
        numeric_df = self.df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        
        # Group by the date column and calculate mean of other columns
        grouped_df = numeric_df.groupby(self.df.iloc[:, 0]).mean().reset_index()
        
        return grouped_df
