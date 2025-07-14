import streamlit as st
import pandas as pd
import io
from utils.data_cleaner import DataCleaner
from utils.process_file import FileProcessor
from utils.background_style import *

class FilePageHandler:
    def __init__(self, index: int):
        self.index = index
        self.page_name = f"File {index+1}"
        self.file_key = f"upload_{index}"
        self.filename_key = f"uploaded_filename_{index}"
        self.handle_page()

    def handle_page(self):
        if "renamed_columns" not in st.session_state:
            st.session_state["renamed_columns"] = {}

        if "processed_files" not in st.session_state:
            st.session_state["processed_files"] = {}

        if "finalized_files" not in st.session_state:
            st.session_state["finalized_files"] = {}

        uploaded_file = st.file_uploader(f"Upload {self.page_name}", type=["csv", "xlsx"], key=self.file_key)

        if uploaded_file:
            file_bytes = uploaded_file.read()
            st.session_state[f"uploaded_file_{self.index}"] = file_bytes
            st.session_state[self.filename_key] = uploaded_file.name

        if f"uploaded_file_{self.index}" not in st.session_state:
            return

        file_name = st.session_state[self.filename_key]
        file_bytes = st.session_state[f"uploaded_file_{self.index}"]
        buffer = io.BytesIO(file_bytes)

        fileProcessor = FileProcessor(buffer, f"file{self.index+1}", file_name)
        df_original = fileProcessor.process()

        # Use processed_files cache or fallback to original
        df_from_cache = st.session_state.processed_files.get(file_name, df_original)

        # Key to store combined dataframe once
        combined_key = f"combined_{file_name}"

        cleaner = DataCleaner(df_from_cache)

        # Find date and time columns
        time_col = next((col for col in df_from_cache.columns if "Zeit" in col or "Time" in col), None)
        date_col = next((col for col in df_from_cache.columns if "Datum" in col or "Date" in col), None)

        # Combine date and time columns only once and cache in session_state
        if combined_key not in st.session_state:
            if time_col and date_col:
                df_combined = cleaner.combine_date_and_end_time(date_col, time_col)
            else:
                df_combined = df_from_cache
            st.session_state[combined_key] = df_combined
        else:
            df_combined = st.session_state[combined_key]

        # Update processed_files cache with combined dataframe for consistency
        st.session_state.processed_files[file_name] = df_combined

        st.write("### All Sheets Combined Data Preview:")
        st.dataframe(df_original)

        st.write("### Date-Time Combined Preview:")
        st.dataframe(df_combined)

        display_app_header(main_txt="Step 2",
                           sub_txt="Renaming the selected columns",
                           is_sidebar=False)

        df_columns = list(df_combined.columns)

        # Persist selected options in session state
        selection_key = f"selected_option_{file_name}"
        if selection_key not in st.session_state:
            st.session_state[selection_key] = []

        # Filter default selection to valid columns only
        valid_default_selection = [col for col in st.session_state[selection_key] if col in df_columns]


        selected_option = st.multiselect(
            "Choose an option",
            df_columns,
            default=valid_default_selection,
            key=f"multiselect_{file_name}"
        )
        st.session_state[selection_key] = selected_option
        selected = selected_option

        # Show text inputs for renaming the selected columns
        if selected:
            st.write("### Rename Selected Columns")
            new_names = {
                col: st.text_input(f"Rename '{col}' to:", value=col, key=f"rename_{file_name}_{col}")
                for col in selected
            }
        else:
            new_names = {}

        # Button to apply renaming
        if st.button(f"Rename Selected Columns for {self.page_name}"):
            if new_names:
                rename_dict = {k: v for k, v in new_names.items() if k != v}
                if rename_dict:
                    df_combined.rename(columns=rename_dict, inplace=True)
                    st.session_state.processed_files[file_name] = df_combined
                    st.session_state[combined_key] = df_combined
                    st.success("✅ Columns renamed.")
                    st.rerun()
                else:
                    st.info("No column names were changed.")
            else:
                st.warning("Please select columns to rename.")
        # Step 3 UI
        display_app_header(main_txt="Step 3",
                           sub_txt="Deleting the selected columns and rows",
                           is_sidebar=False)

        st.write("### Delete Columns and Rows")
        cols_to_delete = st.multiselect(f"Columns to delete for {self.page_name}", df_combined.columns)
        rows_to_delete = st.multiselect(f"Row indices to delete for {self.page_name}", df_combined.index.tolist())

        if st.button(f"Delete Selected Columns and Rows for {self.page_name}"):
            df_combined.drop(columns=cols_to_delete, inplace=True, errors='ignore')
            df_combined.drop(index=rows_to_delete, inplace=True, errors='ignore')
            st.session_state.processed_files[file_name] = df_combined
            st.session_state[combined_key] = df_combined  # Keep combined cached df updated
            st.success("✅ Deletion complete.")
            st.experimental_rerun()

        if st.button(f"Clean & Describe All Columns ({self.page_name})"):
            try:
                cleaner = DataCleaner(df_combined)  # refresh cleaner with updated df
                df_cleaned, dropped_cols, desc, before_types, after_types = cleaner.clean_and_describe()
                st.session_state.processed_files[file_name] = df_cleaned
                st.session_state[combined_key] = df_cleaned  # update combined cache as well
                st.success(f"✅ Dropped columns: {list(dropped_cols)}")
                st.dataframe(desc)
                st.write("Column Types Before:", before_types)
                st.write("Column Types After:", after_types)
                st.dataframe(df_cleaned)
            except Exception as e:
                st.error(f"❌ Error during cleaning: {e}")

        if st.button(f"Finalize {self.page_name}"):
            st.session_state.finalized_files[file_name] = df_combined
            st.success(f"{file_name} finalized!")
            st.experimental_rerun()
