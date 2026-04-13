import json
from pathlib import Path


class StorageService:
    BASE_DIR = Path(__file__).resolve().parents[2]
    CACHE_DIR = BASE_DIR / "data" / "local_cache"
    ROADMAP_FILE = CACHE_DIR / "roadmap.json"

    @classmethod
    def ensure_cache_dir(cls) -> None:
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def save_json(cls, filepath: Path, data) -> None:
        cls.ensure_cache_dir()
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @classmethod
    def load_json(cls, filepath: Path):
        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)