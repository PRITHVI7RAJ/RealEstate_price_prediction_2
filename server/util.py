import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

__locations = None
__data_columns = None
__model = None
__column_name_lookup = None
__artifacts_dir = Path(__file__).resolve().parent / "artifacts"


def get_estimated_price(location, sqft, bhk, bath):
    loc_index = -1
    if location:
        normalized_location = location.strip().lower()
        loc_index = __column_name_lookup.get(normalized_location, -1)

    x_pred = np.zeros(len(__data_columns), dtype=np.float64)
    x_pred[0] = float(sqft)
    x_pred[1] = float(bath)
    x_pred[2] = float(bhk)

    if loc_index >= 0:
        x_pred[int(loc_index)] = 1.0

    x_pred_df = pd.DataFrame([x_pred], columns=__data_columns)
    return round(float(__model.predict(x_pred_df)[0]), 2)


def get_location_names():
    return __locations


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model
    global __column_name_lookup

    with (__artifacts_dir / "columns.json").open("r", encoding="utf-8") as f:
        data_columns = json.load(f)["data_columns"]

    with (__artifacts_dir / "banglore_home_prices_model.pickle").open("rb") as f:
        __model = pickle.load(f)

    if hasattr(__model, "feature_names_in_"):
        __data_columns = list(__model.feature_names_in_)
    else:
        __data_columns = data_columns

    __locations = __data_columns[3:]
    __column_name_lookup = {
        column.strip().lower(): index for index, column in enumerate(__data_columns)
    }

    print("loading saved artifacts...done")


if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))
    print(get_estimated_price("1st Phase JP Nagar", 1000, 2, 2))
    print(get_estimated_price("Kalhalli", 1000, 2, 2))
    print(get_estimated_price("Ejipura", 1000, 2, 2))
