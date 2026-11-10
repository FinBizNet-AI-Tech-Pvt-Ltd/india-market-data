"""Refresh data/ from the public CSVs published on finbiznet.com/data.

Standard library only. Each file is downloaded, checked (header matches,
at least one row) and written only when it changed, so a failed or empty
download never overwrites good data.

fii-dii-daily.csv is published as a rolling 30-session window; here it is
MERGED by date into the existing file, so the repository keeps every
session it has ever seen.
"""
import csv
import io
import sys
import urllib.request
from pathlib import Path

BASE = "https://finbiznet.com/data/"
UA = "Mozilla/5.0 (compatible; india-market-data-updater; +https://github.com/FinBizNet-AI-Tech-Pvt-Ltd/india-market-data)"
DATA = Path(__file__).resolve().parent.parent / "data"

FILES = {
    "fii-flows-by-month.csv": "fii-flows-by-month/fii-flows-by-month.csv",
    "fii-dii-daily.csv": "fii-dii-activity/fii-dii-daily.csv",
    "defence-order-books.csv": "defence-order-books/defence-order-books.csv",
    "india-economic-indicators.csv": "india-economic-indicators/india-economic-indicators.csv",
    "india-market-2025-indices.csv": "india-market-2025/india-market-2025-indices.csv",
    "india-market-2026-indices.csv": "india-market-2026/india-market-2026-indices.csv",
}
MERGE_ON = {"fii-dii-daily.csv": "date"}


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            raise RuntimeError(f"HTTP {r.status}")
        text = r.read().decode("utf-8-sig")
    if text.lstrip().startswith("<"):
        raise RuntimeError("got HTML, not CSV")
    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 2:
        raise RuntimeError("no data rows")
    return rows


def write(target, rows):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    new = buf.getvalue()
    old = target.read_text(encoding="utf-8") if target.exists() else None
    if new != old:
        target.write_text(new, encoding="utf-8")
        return True
    return False


def merge(target, rows, key):
    header, body = rows[0], rows[1:]
    k = header.index(key)
    by_key = {}
    if target.exists():
        old = list(csv.reader(io.StringIO(target.read_text(encoding="utf-8"))))
        if old and old[0] == header:
            by_key = {r[k]: r for r in old[1:] if r}
    for r in body:
        by_key[r[k]] = r  # the published figure wins
    return [header] + sorted(by_key.values(), key=lambda r: r[k], reverse=True)


def main():
    failed, changed = [], []
    for name, path in FILES.items():
        target = DATA / name
        try:
            rows = fetch(path)
            if target.exists():
                old_header = target.read_text(encoding="utf-8").splitlines()[:1]
                if old_header and old_header[0].split(",") != rows[0]:
                    print(f"[note] {name}: columns changed")
            if name in MERGE_ON:
                rows = merge(target, rows, MERGE_ON[name])
            if write(target, rows):
                changed.append(name)
            print(f"[ok] {name}: {len(rows) - 1} rows")
        except Exception as e:  # keep going; report at the end
            failed.append(name)
            print(f"[FAILED] {name}: {e}")
    print(f"changed: {', '.join(changed) or 'none'}")
    if failed:
        sys.exit(f"failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
