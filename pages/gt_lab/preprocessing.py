"""
pages/gt_lab/preprocessing.py — Data preprocessing utilities untuk GT Lab
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


def encode_categorical(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Label encode kolom kategorikal."""
    df = df.copy()
    for col in cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    return df


def scale_features(df: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, StandardScaler]:
    """StandardScale fitur numerik. Return (df_scaled, scaler)."""
    df = df.copy()
    scaler = StandardScaler()
    df[cols] = scaler.fit_transform(df[cols])
    return df, scaler


def drop_missing(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Drop kolom dengan missing value > threshold (0–1).
    Kemudian drop baris yang masih ada missing value.
    """
    df = df.copy()
    col_threshold = int(threshold * len(df))
    df = df.dropna(axis=1, thresh=col_threshold)
    df = df.dropna(axis=0)
    return df
