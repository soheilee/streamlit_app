from utils.unique_column_namer import UniqueColumnNamer

class HeaderCombiner:
    def __init__(self, df, header_rows, sheet_name, file_suffix):
        self.df = df
        self.header_rows = header_rows
        self.sheet_name = sheet_name
        self.file_suffix = file_suffix

    def combine(self):
        headers = self.df.iloc[:self.header_rows].astype(str).fillna('')

        combined_headers = []
        for col in headers.columns:
            combined_parts = ' | '.join(headers[col]).strip()
            combined_name = f"{self.sheet_name} | {combined_parts}" if combined_parts else self.sheet_name
            combined_headers.append(combined_name)

        # Use the imported UniqueColumnNamer class
        unique_headers = UniqueColumnNamer(combined_headers, self.file_suffix).make_unique()

        df_cleaned = self.df.iloc[self.header_rows:].reset_index(drop=True)
        df_cleaned.columns = unique_headers

        return df_cleaned
