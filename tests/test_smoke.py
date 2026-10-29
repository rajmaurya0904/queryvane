"""Smoke test: package imports cleanly. Replace/extend as modules land."""

import queryvane


def test_version_is_set() -> None:
    assert queryvane.__version__
