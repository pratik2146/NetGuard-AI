import glob
import os
from pathlib import Path
from typing import Optional, List, Tuple
import pandas as pd

from netguard.config import DATA_DIR, FAULT_LOG_PATH
from netguard.utils.logger import logger

def load_raw_dataset(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """
    Load and concatenate all LCORE-D R*.csv monitoring files from the data directory.
    """
    target_dir = Path(data_dir or DATA_DIR)
    csv_pattern = str(target_dir / "LCORE-D R*.csv")
    csv_files = sorted(glob.glob(csv_pattern))

    if not csv_files:
        logger.error(f"No LCORE-D benchmark files found matching pattern: {csv_pattern}")
        raise FileNotFoundError(
            f"No dataset files were found at '{target_dir}'. "
            f"Expected files matching pattern: LCORE-D R*.csv"
        )

    logger.info(f"Found {len(csv_files)} dataset files to load.")
    frames: List[pd.DataFrame] = []

    for file_path in csv_files:
        basename = os.path.basename(file_path)
        logger.info(f"  Reading dataset file: {basename}")
        df_temp = pd.read_csv(file_path, low_memory=False)
        df_temp["source_file"] = basename
        frames.append(df_temp)

    combined_df = pd.concat(frames, ignore_index=True)
    logger.info(f"Successfully combined dataset. Total rows: {len(combined_df):,}")
    return combined_df

def load_fault_log(fault_log_path: Optional[Path] = None) -> Optional[pd.DataFrame]:
    """
    Load network fault event log CSV if available.
    """
    target_path = Path(fault_log_path or FAULT_LOG_PATH)
    if not target_path.exists():
        logger.warning(f"Fault log file not found at {target_path}")
        return None

    try:
        df_log = pd.read_csv(target_path)
        df_log.columns = [str(col).strip() for col in df_log.columns]
        logger.info(f"Loaded fault log with {len(df_log)} records.")
        return df_log
    except Exception as exc:
        logger.error(f"Failed to load fault log: {exc}")
        return None
