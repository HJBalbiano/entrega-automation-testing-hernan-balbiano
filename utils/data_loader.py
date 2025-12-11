import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_json(path: str | Path) -> Any:
    """Load JSON test data."""
    with Path(path).open(encoding="utf-8") as fp:
        return json.load(fp)


def load_csv(path: str | Path) -> List[Dict[str, str]]:
    """Load CSV test data into a list of dicts."""
    with Path(path).open(newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        return list(reader)


def ensure_dir(path: str | Path) -> Path:
    """Create directory if missing and return the Path."""
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj
