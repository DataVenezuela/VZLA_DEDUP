from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scrapers.validators.source_validator import validate_sources_config


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m scrapers.cli",
        description="VZLA_DEDUP scrapers pipeline",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run scraper pipeline")
    run_cmd.add_argument("--config", required=True, help="YAML config path")
    run_cmd.add_argument(
        "--output-dir", default="scrapers/runtime_output", help="Output directory"
    )
    run_cmd.add_argument("--limit", type=int, default=None, help="Max documents per source")
    run_cmd.add_argument(
        "--keep-raw",
        action="store_true",
        help="Keep redacted source snapshots locally for debugging; raw PII is never written",
    )

    validate_cmd = sub.add_parser("validate", help="Validate source config")
    validate_cmd.add_argument("--config", required=True, help="YAML config path")

    args = parser.parse_args()

    if args.command == "validate":
        config_path = Path(args.config)
        try:
            validate_sources_config(config_path)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            raise SystemExit(1) from exc
        print(f"OK: config valida: {config_path}")
        return

    if args.command == "run":
        from scrapers.pipelines.run_pipeline import run_pipeline

        summary = run_pipeline(
            config_path=Path(args.config),
            output_dir=Path(args.output_dir),
            limit=args.limit,
            keep_raw=args.keep_raw,
        )
        print("Pipeline finalizado")
        print(f"Fuentes procesadas: {summary['sources_processed']}")
        print(f"Documentos exportados: {summary['documents_exported']}")
        print(f"Claims exportados: {summary['claims_exported']}")
        print(f"Claims deduplicados: {summary['claims_deduplicated']}")
        print(f"Errores: {len(summary['errors'])}")
        print(f"Salida: {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
