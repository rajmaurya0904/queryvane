# Changelog

All notable changes to QueryVane are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release of QueryVane, a zero-config local latency monitor for
  benchmarking and visualizing SQLite and Postgres query performance
  degradation over time as tables grow.
- `queryvane.storage` module: local persistence for benchmark runs and
  latency samples.
- CLI entry point for running benchmarks and inspecting stored results.
- Test suite covering the storage layer.