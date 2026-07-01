"""
services/ml_service.py — ML model training & inference (GT Lab)
PRD Section 5 & 9: shell untuk Regression, Classification, Clustering.
Implementasi final menyusul setelah dataset tersedia.
"""

import streamlit as st
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error, r2_score,
    accuracy_score, classification_report,
)
import numpy as np
import pandas as pd
from pathlib import Path

from utils.logger import log

MODEL_SAVE_DIR = Path("models/saved")
MODEL_SAVE_DIR.mkdir(parents=True, exist_ok=True)


@st.cache_resource
def get_scaler() -> StandardScaler:
    """Singleton StandardScaler (re-fit per dataset)."""
    return StandardScaler()


# ── Regression ─────────────────────────────────────────────────────────────────

def train_regression(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str,
    test_size: float = 0.2,
) -> dict:
    """
    Train Linear Regression.
    Return dict berisi model, metrics, dan data test untuk chart.
    """
    X = df[feature_cols].dropna()
    y = df[target_col].loc[X.index]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return {
        "model": model,
        "mse": mean_squared_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred),
        "y_test": y_test.tolist(),
        "y_pred": y_pred.tolist(),
    }


# ── Classification ─────────────────────────────────────────────────────────────

def train_classification(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str,
    test_size: float = 0.2,
) -> dict:
    """
    Train Logistic Regression (placeholder — ganti model sesuai kebutuhan).
    """
    X = df[feature_cols].dropna()
    y = df[target_col].loc[X.index]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return {
        "model": model,
        "accuracy": accuracy_score(y_test, y_pred),
        "report": classification_report(y_test, y_pred, output_dict=True),
        "y_test": y_test.tolist(),
        "y_pred": y_pred.tolist(),
    }


# ── Clustering ─────────────────────────────────────────────────────────────────

def train_clustering(
    df: pd.DataFrame,
    feature_cols: list[str],
    n_clusters: int = 3,
) -> dict:
    """Train KMeans clustering."""
    X = df[feature_cols].dropna()
    scaler = get_scaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels = model.fit_predict(X_scaled)

    return {
        "model": model,
        "labels": labels.tolist(),
        "inertia": model.inertia_,
        "centers": model.cluster_centers_.tolist(),
    }
