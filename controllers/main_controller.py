import pandas as pd
import re


class ControladorPrincipal:
    def __init__(self):
        pass

    def procesar_archivo(self, df):
        df = pd.read_excel(df, names=[])

        # Define all processing tasks like removing or creating new columns, apply format, clean data, etc.

        # Return the processed dataframes or any other desired result
        return df