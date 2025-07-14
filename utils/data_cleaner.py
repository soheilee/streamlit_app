import pandas as pd
import numpy as np
import re

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def replace_word_with_nan(self, word: str):
        def clean_cell(x):
            return x.strip().lower() if isinstance(x, str) else x

        cleaned_word = word.strip().lower()
        df_temp = self.df.applymap(clean_cell)
        matches = (df_temp == cleaned_word).sum().sum()

        self.df.replace(
            to_replace=lambda x: clean_cell(x) == cleaned_word if isinstance(x, str) else False,
            value=np.nan,
            inplace=True
        )
        return matches, self.df

    def combine_date_and_end_time(self, date_col, time_col):
        def extract_end_time(val):
            if isinstance(val, str) and '-' in val:
                match = re.match(r".*-(\d{2}:\d{2})", val)
                if match:
                    return match.group(1)
            return None

        end_times = self.df[time_col].apply(extract_end_time)
        date_strings = pd.to_datetime(self.df[date_col], errors='coerce').dt.strftime('%Y-%m-%d')
        self.df[date_col] = date_strings + ' ' + end_times.fillna('')
        self.df.drop(columns=[time_col], inplace=True)
        return self.df

    def clean_and_describe(self):
        protected_keywords = ['date', 'time', 'zeit', 'datum']
        protected_cols = [col for col in self.df.columns if any(kw in col.lower() for kw in protected_keywords)]
        convert_cols = [col for col in self.df.columns if col not in protected_cols]

        numeric_df = self.df[convert_cols].apply(pd.to_numeric, errors='coerce')
        drop_mask = numeric_df.isna().mean() >= 0.3
        dropped_cols = numeric_df.columns[drop_mask]
        numeric_df = numeric_df.drop(columns=dropped_cols)

        df_cleaned = pd.concat([self.df[protected_cols], numeric_df], axis=1)
        description = numeric_df.describe(percentiles=[.25, .5, .75]).T
        description['median'] = numeric_df.median()

        return df_cleaned, dropped_cols, description, self.df.dtypes, df_cleaned.dtypes
