# QueryVane

**A zero-config local latency monitor that benchmarks and visualizes SQLite and Postgres query performance degradation over time as tables grow.**

When database tables grow from thousands to millions of rows, queries silently slow down long before production alerts fire.
QueryVane removes the guesswork by tracking query latency across table growth stages, exposing sudden degradations and missing indexes locally.

## Example

Run `queryvane --help` to see available options:

```bash
$ queryvane --help
usage: queryvane [-h] [--version]

A zero-config local latency monitor that benchmarks and visualizes SQLite and Postgres query performance degradation over time as tables grow.

options:
  -h, --help     show a free help message and exit
  --version      show program's version number and exit
```

## Install

Install in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

```bash
queryvane --help
```

## How it works

- Connects to local SQLite databases or Postgres connection strings without requiring server configuration changes.
- Benchmarks specified read queries across simulated table growth increments.
- Computes execution time distributions, percentiles, and degradation factors per growth tier.
- Emits terminal summary tables and local HTML latency progression reports.

## Limitations

- Does not execute write benchmarks or transactional locking contention analysis.
- Requires read-only query definitions provided via CLI or configuration file.
- SQLite support handles local file paths; Postgres requires standard connection URI format.

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
```

## License

MIT -- see [LICENSE](LICENSE).
