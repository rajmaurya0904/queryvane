"""Time-series metric storage for benchmark results."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).with_name("metrics.db")


def _connect(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            row_count INTEGER NOT NULL,
            latency_p50 REAL NOT NULL,
            latency_p95 REAL NOT NULL,
            latency_p99 REAL NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def record_metric(
    timestamp: str,
    row_count: int,
    latency_p50: float,
    latency_p95: float,
    latency_p99: float,
    db_path: Path = DEFAULT_DB,
) -> int:
    """Record a benchmark metric row and return its new id."""
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "INSERT INTO metrics (timestamp, row_count, latency_p50, latency_p95, latency_p99) "
            "VALUES (?, ?, ?, ?, ?)",
            (timestamp, row_count, latency_p50, latency_p95, latency_p99),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def get_metrics(db_path: Path = DEFAULT_DB) -> list[dict]:
    """Return all stored metrics ordered by timestamp."""
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT timestamp, row_count, latency_p50, latency_p95, latency_p99 "
            "FROM metrics ORDER BY timestamp"
        ).fetchall()
    finally:
        conn.close()
    return [
        {
            "timestamp": r[0],
            "row_count": r[1],
            "latency_p50": r[2],
            "latency_p95": r[3],
            "latency_p99": r[4],
        }
        for r in rows
    ]


def clear_metrics(db_path: Path = DEFAULT_DB) -> int:
    """Delete all stored metrics and return the number of rows removed."""
    conn = _connect(db_path)
    try:
        cur = conn.execute("DELETE FROM metrics")
        conn.commit()
        return int(cur.rowcount)
    finally:
        conn.close()
