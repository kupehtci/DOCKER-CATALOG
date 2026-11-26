"""Single-shot job: checks a list of URLs and writes a JSON report.

The container runs this script once and exits. The exit code is 0 when every
URL answered with a 2xx/3xx status, 1 otherwise, so it can be chained in CI,
cron or orchestration tools.

Configuration (CLI arguments take precedence over environment variables):
  --url URL        URL to check (repeatable). Env: TARGET_URLS (comma separated)
  --timeout SECS   Request timeout.             Env: REQUEST_TIMEOUT (default 5)
  --output PATH    JSON report path.            Env: OUTPUT_FILE (default /app/output/report.json)
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("singleshot")


def parse_args() -> argparse.Namespace:
    env_urls = [u.strip() for u in os.getenv("TARGET_URLS", "").split(",") if u.strip()]

    parser = argparse.ArgumentParser(description="Check a list of URLs and write a JSON report.")
    parser.add_argument("--url", action="append", dest="urls", help="URL to check (repeatable)")
    parser.add_argument("--timeout", type=float, default=float(os.getenv("REQUEST_TIMEOUT", "5")))
    parser.add_argument("--output", default=os.getenv("OUTPUT_FILE", "/app/output/report.json"))
    args = parser.parse_args()

    args.urls = args.urls or env_urls
    if not args.urls:
        parser.error("no URLs given: use --url or the TARGET_URLS environment variable")
    return args


def check(url: str, timeout: float) -> dict:
    try:
        response = requests.get(url, timeout=timeout)
        ok = response.status_code < 400
        result = {
            "url": url,
            "ok": ok,
            "status": response.status_code,
            "elapsed_ms": round(response.elapsed.total_seconds() * 1000),
        }
    except requests.RequestException as exc:
        result = {"url": url, "ok": False, "status": None, "error": str(exc)}

    logger.log(logging.INFO if result["ok"] else logging.WARNING, "%s -> %s", url, result.get("status") or result.get("error"))
    return result


def main() -> int:
    args = parse_args()
    logger.info("Checking %d URL(s)", len(args.urls))

    results = [check(url, args.timeout) for url in args.urls]
    failed = sum(not r["ok"] for r in results)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "failed": failed,
        "results": results,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2))
    logger.info("Report written to %s (%d failed)", output, failed)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
