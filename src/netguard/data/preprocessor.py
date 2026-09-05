from typing import List, Tuple, Set
import numpy as np
import pandas as pd

from netguard.config import EXCLUDED_COLUMNS
from netguard.utils.logger import logger

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataframe column names and remove empty unnamed columns.
    """
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    
    empty_unnamed = [
        col for col in df.columns 
        if col.startswith("Unnamed:") and df[col].isna().all()
    ]
    if empty_unnamed:
        df = df.drop(columns=empty_unnamed)
        
    return df

def process_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse numeric timestamp column into pandas datetime column.
    """
    df = df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
        df["timestamp_dt"] = pd.to_datetime(df["timestamp"], unit="s", errors="coerce")
    else:
        df["timestamp_dt"] = pd.NaT
    return df

def create_target_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create binary 'target' column where target=1 if class == 'F' else 0.
    """
    df = df.copy()
    if "class" not in df.columns:
        raise ValueError("Required column 'class' was not found in dataset.")
        
    df["class"] = df["class"].astype(str).str.strip()
    df["target"] = (df["class"] == "F").astype(int)
    return df

def select_numeric_features(df: pd.DataFrame, excluded_cols: Set[str] = EXCLUDED_COLUMNS) -> List[str]:
    """
    Identify usable numeric feature columns from dataset.
    """
    feature_columns: List[str] = []
    for col in df.columns:
        if col in excluded_cols:
            continue
        numeric_series = pd.to_numeric(df[col], errors="coerce")
        if numeric_series.notna().sum() > 0:
            feature_columns.append(col)
            
    logger.info(f"Selected {len(feature_columns)} numeric feature columns.")
    return feature_columns

def prepare_features(
    input_df: pd.DataFrame, 
    feature_columns: List[str]
) -> pd.DataFrame:
    """
    Sanitize and format features for model consumption.
    - Missing columns are filled with NaN.
    - Non-numeric strings converted to NaN.
    - Dataset missing indicators (-1, -9999) converted to NaN.
    """
    data_dict = {}
    for feat in feature_columns:
        if feat in input_df.columns:
            data_dict[feat] = pd.to_numeric(input_df[feat], errors="coerce")
        else:
            data_dict[feat] = np.nan

    X = pd.DataFrame(data_dict, index=input_df.index)
    # Replace specific dataset sentinels with NaN
    X = X.replace([-1, -9999, -1.0, -9999.0], np.nan)
    return X
