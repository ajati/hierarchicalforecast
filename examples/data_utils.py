import pandas as pd
import numpy as np


def convert_df_to_gluonts_iter(df: pd.DataFrame, horizon: int):

    unq_ids = np.unique(df.index)

    for id_ in unq_ids:
        vals = df[df.index == id_]
        print(vals)
        break
