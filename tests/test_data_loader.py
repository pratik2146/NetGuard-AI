import pandas as pd
from netguard.data.preprocessor import clean_column_names, process_timestamps, create_target_column, prepare_features

def test_clean_column_names():
    df = pd.DataFrame({"  col1 ": [1, 2], "Unnamed: 0": [None, None]})
    cleaned = clean_column_names(df)
    assert "col1" in cleaned.columns
    assert "Unnamed: 0" not in cleaned.columns

def test_process_timestamps():
    df = pd.DataFrame({"timestamp": [1728730680]})
    processed = process_timestamps(df)
    assert "timestamp_dt" in processed.columns
    assert str(processed["timestamp_dt"].iloc[0].year) == "2024" or str(processed["timestamp_dt"].iloc[0].year) == "2025"

def test_create_target_column():
    df = pd.DataFrame({"class": ["F", "H", "T"]})
    target_df = create_target_column(df)
    assert target_df["target"].tolist() == [1, 0, 0]

def test_prepare_features():
    df = pd.DataFrame({"feat1": [10.0, -1, -9999], "feat2": ["5.5", "invalid", "2.0"]})
    X = prepare_features(df, ["feat1", "feat2"])
    assert pd.isna(X["feat1"].iloc[1])
    assert pd.isna(X["feat1"].iloc[2])
    assert X["feat2"].iloc[0] == 5.5
