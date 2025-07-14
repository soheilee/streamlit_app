class UniqueColumnNamer:
    def __init__(self, columns, suffix):
        self.columns = columns
        self.suffix = suffix

    def make_unique(self):
        seen = {}
        unique_columns = []

        for col in self.columns:
            if col == '':
                col = "column"
            if col in seen:
                seen[col] += 1
                unique_columns.append(f"{col}_{seen[col]}_{self.suffix}")
            else:
                seen[col] = 0
                unique_columns.append(f"{col}_{self.suffix}")
                
        return unique_columns
