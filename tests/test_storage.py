"""Tests for metric storage and retrieval."""

import tempfile
from pathlib import Path

import pytest

from queryvane import storage


@pytest.fixture
def temp_db():
    """Create a temporary database file for each test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_metrics.db"
        yield db_path
        # Cleanup happens automatically when tempdir is removed


def test_record_and_retrieve_metric(temp_db):
    """A metric can be recorded and retrieved."""
    storage.record_metric(
        timestamp="2024-01-01T00:00:00Z",
        row_count=1000,
        latency_p50=1.5,
        latency_p95=3.2,
        latency_p99=5.0,
        db_path=temp_db,
    )

    metrics = storage.get_metrics(db_path=temp_db)
    assert len(metrics) == 1
    assert metrics[0]["timestamp"] == "2024-01-01T00:00:00Z"
    assert metrics[0]["row_count"] == 1000
    assert metrics[0]["latency_p50"] == 1.5
    assert metrics[0]["latency_p95"] == 3.2
    assert metrics[0]["latency_p99"] == 5.0


def test_multiple_metrics_ordered_by_timestamp(temp_db):
    """Multiple metrics are returned in timestamp order."""
    storage.record_metric(
        timestamp="2024-01-01T12:00:00Z",
        row_count=5000,
        latency_p50=2.0,
        latency_p95=4.0,
        latency_p99=6.0,
        db_path=temp_db,
    )
    storage.record_metric(
        timestamp="2024-01-01T00:00:00Z",
        row_count=1000,
        latency_p50=1.0,
        latency_p95=2.0,
        latency_p99=3.0,
        db_path=temp_db,
    )

    metrics = storage.get_metrics(db_path=temp_db)
    assert len(metrics) == 2
    assert metrics[0]["timestamp"] == "2024-01-01T00:00:00Z"
    assert metrics[1]["timestamp"] == "2024-01-01T12:00:00Z"


def test_clear_metrics(temp_db):
    """Clearing metrics removes all rows."""
    storage.record_metric(
        timestamp="2024-01-01T00:00:00Z",
        row_count=1000,
        latency_p50=1.0,
        latency_p95=2.0,
        latency_p99=3.0,
        db_path=temp_db,
    )
    storage.record_metric(
        timestamp="2024-01-02T00:00:00Z",
        row_count=2000,
        latency_p50=2.0,
        latency_p95=4.0,
        latency_p99=6.0,
        db_path=temp_db,
    )

    removed = storage.clear_metrics(db_path=temp_db)
    assert removed == 2

    metrics = storage.get_metrics(db_path=temp_db)
    assert len(metrics) == 0


def test_empty_database_returns_empty_list(temp_db):
    """Querying an empty database returns an empty list."""
    metrics = storage.get_metrics(db_path=temp_db)
    assert metrics == []


def test_record_metric_returns_id(temp_db):
    """Recording a metric returns a positive integer id."""
    id1 = storage.record_metric(
        timestamp="2024-01-01T00:00:00Z",
        row_count=1000,
        latency_p50=1.0,
        latency_p95=2.0,
        latency_p99=3.0,
        db_path=temp_db,
    )
    assert isinstance(id1, int)
    assert id1 > 0

    id2 = storage.record_metric(
        timestamp="2024-01-02T00:00:00Z",
        row_count=2000,
        latency_p50=2.0,
        latency_p95=4.0,
        latency_p99=6.0,
        db_path=temp_db,
    )
    assert id2 > id1