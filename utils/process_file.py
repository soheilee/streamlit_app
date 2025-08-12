import pandas as pd
import streamlit as st
from utils.detect_file import EncodingDetector
from utils.header_row_detector import HeaderRowDetector
from utils.header_combiner import HeaderCombiner

class FileProcessor:
    def __init__(self, uploaded_file, file_suffix, file_name):
        self.uploaded_file = uploaded_file
        self.file_suffix = file_suffix
        self.file_name = file_name

    def process(self):
        if self.file_name.endswith('.csv'):
            encoding_detector = EncodingDetector(self.uploaded_file)
            encoding = encoding_detector.detect()

            df = pd.read_csv(self.uploaded_file, delimiter=';', header=None, encoding=encoding)


            header_detector = HeaderRowDetector(df)
            header_rows = header_detector.detect()


            combiner = HeaderCombiner(df, header_rows, self.file_name, self.file_suffix)
            return combiner.combine()

        else:
            xls = pd.ExcelFile(self.uploaded_file)
            combined_df = pd.DataFrame()

            for sheet_name in xls.sheet_names:
                df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)

                header_detector = HeaderRowDetector(df_sheet)
                header_rows = header_detector.detect()+1
                st.markdown(
                    f"<span style='font-size:20px; color:#A74369; text_align:center; font-weight: bold;'>{header_rows} Header-Rows in ({sheet_name}) detected</span>",
                    unsafe_allow_html=True
                )
                

                combiner = HeaderCombiner(df_sheet, header_rows, sheet_name, self.file_suffix)
                df_sheet = combiner.combine()

                combined_df = pd.concat([combined_df, df_sheet], axis=1)

            return combined_df
