import pandas as pd
import numpy as np
def make_csv(parcellation, save):
    resolution = 0.6 * 0.6 * 0.6
    csv_path = "level/Level5.txt"
    df = pd.read_table(csv_path, names=["number","region"]).astype("str").set_index("number")
    for i in range(168):
        i += 1
        volume = np.count_nonzero(parcellation==i)
        df.loc[str(i), save] = volume * resolution
    df = df.set_index("region").T.reset_index().rename(columns={"index":"uid"})
    return df
