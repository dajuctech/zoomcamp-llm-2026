import os
from pathlib import Path

import pandas as pd
from minsearch import Index


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = os.getenv("DATA_PATH", str(PROJECT_DIR / "data" / "data.csv"))


def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)
    documents = df.to_dict(orient="records")

    index = Index(
        text_fields=[
            "exercise_name",
            "type_of_activity",
            "type_of_equipment",
            "body_part",
            "type",
            "muscle_groups_activated",
            "instructions",
        ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index
