"""
tests/test_csv_service.py — Unit tests untuk CSV service
PRD Section 8: tests/ cover CSV validation.
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "id": [1, 2, 3],
        "nama": ["A", "B", "C"],
        "nilai": [10.5, 20.0, 30.75],
    })


@pytest.fixture
def sample_csv(tmp_path, sample_df):
    """Buat file CSV sementara untuk testing."""
    csv_path = tmp_path / "test_data.csv"
    sample_df.to_csv(csv_path, index=False)
    return csv_path


class TestLoadCsv:

    def test_load_valid_csv(self, sample_csv):
        """CSV valid harus berhasil dimuat."""
        from services.csv_service import load_csv
        # Clear cache sebelum test
        load_csv.clear()
        df = load_csv(sample_csv)
        assert df is not None
        assert len(df) == 3
        assert list(df.columns) == ["id", "nama", "nilai"]

    def test_load_nonexistent_file(self, tmp_path):
        """File tidak ada harus return None."""
        from services.csv_service import load_csv
        load_csv.clear()
        result = load_csv(tmp_path / "tidak_ada.csv")
        assert result is None

    def test_load_empty_csv(self, tmp_path):
        """CSV kosong (header saja) harus return DataFrame kosong, bukan None."""
        from services.csv_service import load_csv
        load_csv.clear()
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("id,nama,nilai\n")
        df = load_csv(empty_csv)
        assert df is not None
        assert df.empty


class TestValidateCsvColumns:

    def test_all_columns_present(self, sample_df):
        from utils.validator import validate_csv_columns
        is_valid, missing = validate_csv_columns(sample_df, ["id", "nama", "nilai"])
        assert is_valid is True
        assert missing == []

    def test_missing_column(self, sample_df):
        from utils.validator import validate_csv_columns
        is_valid, missing = validate_csv_columns(sample_df, ["id", "kolom_tidak_ada"])
        assert is_valid is False
        assert "kolom_tidak_ada" in missing

    def test_empty_required_columns(self, sample_df):
        from utils.validator import validate_csv_columns
        is_valid, missing = validate_csv_columns(sample_df, [])
        assert is_valid is True
        assert missing == []


class TestValidateNotEmpty:

    def test_non_empty_df(self, sample_df):
        from utils.validator import validate_dataframe_not_empty
        assert validate_dataframe_not_empty(sample_df) is True

    def test_empty_df(self):
        from utils.validator import validate_dataframe_not_empty
        assert validate_dataframe_not_empty(pd.DataFrame()) is False

    def test_none_df(self):
        from utils.validator import validate_dataframe_not_empty
        assert validate_dataframe_not_empty(None) is False
