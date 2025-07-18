import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path
from io import BytesIO

class N2OPlotter:
    def __init__(self):
        self.handle_page()

    def handle_page(self):

        uploaded_files = st.file_uploader(
            "Select Excel files (.xlsx) to upload",
            type=["xlsx"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            if st.button("Generate Plots from Uploaded Files"):
                self.process_files(uploaded_files)

    def process_files(self, uploaded_files):
        # Optional: create an output folder in the current working directory
        output_folder = "plots"
        os.makedirs(output_folder, exist_ok=True)

        for uploaded_file in uploaded_files:
            filename = uploaded_file.name
            try:
                # Read Excel from uploaded file bytes
                df = pd.read_excel(BytesIO(uploaded_file.read()))
                df = df[df["N2O (ppm)"] >= 0]

                # Check and strip column names to avoid leading/trailing spaces
                df.columns = df.columns.str.strip()
                if "N2O (ppm)" in df.columns and "UTC" in df.columns:
                    times = pd.to_datetime(df["UTC"], errors='coerce')
                    n2o = pd.to_numeric(df["N2O (ppm)"], errors='coerce')
                    valid = times.notna() & n2o.notna()
                    if valid.any():
                        all_times = times[valid]
                        all_n2o_values = n2o[valid]

                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.scatter(all_times, all_n2o_values, color='orange', alpha=0.7)
                        ax.set_title(f"N₂O Konzentration – {filename}")
                        ax.set_xlabel("Date")
                        ax.set_ylabel("N₂O (ppm)")
                        ax.grid(True)
                        st.pyplot(fig)

                        output_filename = os.path.splitext(filename)[0] + ".png"
                        output_path = os.path.join(output_folder, output_filename)
                        fig.savefig(output_path)
                        plt.close(fig)
                    else:
                        st.warning(f"No valid data in {filename}")
                else:
                    st.warning(f"❗ Required columns missing in: {filename}")
            except Exception as e:
                st.error(f"Error reading {filename}: {e}")
