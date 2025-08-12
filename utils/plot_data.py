import pandas as pd
import numpy as np
import re
import streamlit as st

class PlotData:
    def __init__(self, df):
        self.df = df

    def plotData(self):
        if not self.df.empty:
            first_col = self.df.columns[0]
            available_cols = [col for col in self.df.columns if col != first_col]

            selected_plot_cols = st.multiselect(
                f"Select columns to plot against '{first_col}'",
                available_cols
            )

            if selected_plot_cols:
                try:
                    # Copy relevant columns
                    plot_df = self.df[[first_col] + selected_plot_cols].copy()

                    # Rename first column to a safe name for Altair
                    plot_df.rename(columns={first_col: "x_axis"}, inplace=True)

                    # Convert x_axis to a valid type for plotting
                    try:
                        plot_df["x_axis"] = pd.to_datetime(plot_df["x_axis"])
                    except Exception:
                        try:
                            plot_df["x_axis"] = pd.to_numeric(plot_df["x_axis"])
                        except Exception:
                            plot_df["x_axis"] = plot_df["x_axis"].astype(str)

                    # Plot with safe name as index
                    st.line_chart(plot_df.set_index("x_axis"))

                except Exception as e:
                    st.error(f"Error while plotting: {e}")
            else:
                st.info("Please select at least one column to plot.")