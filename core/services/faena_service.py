from copy import deepcopy
from datetime import date

from core.data.faenas_seed import DAILY_FAENAS
from core.services.storage_service import StorageService


class FaenaService:
    _faenas: list[dict] | None = None

    @classmethod
    def _get_file_path(cls):
        return StorageService.CACHE_DIR / "faenas.json"

    @classmethod
    def _load_initial_data(cls) -> None:
        if cls._faenas is not None:
            return

        cached_data = StorageService.load_json(cls._get_file_path())
        if cached_data is not None:
            cls._faenas = cached_data
        else:
            cls._faenas = deepcopy(DAILY_FAENAS)
            cls._save()

    @classmethod
    def _save(cls) -> None:
        if cls._faenas is None:
            return
        StorageService.save_json(cls._get_file_path(), cls._faenas)

    @classmethod
    def get_all_faenas(cls) -> list[dict]:
        cls._load_initial_data()
        return cls._faenas

    @classmethod
    def get_today_faenas(cls) -> list[dict]:
        cls._load_initial_data()
        today = str(date.today())
        return [f for f in cls._faenas if f["date"] == today]

    @classmethod
    def get_today_metrics(cls) -> dict:
        today_faenas = cls.get_today_faenas()

        total = len(today_faenas)
        completed = sum(1 for f in today_faenas if f["completed"])
        total_hours = sum(int(f["hours"]) for f in today_faenas)
        completed_hours = sum(int(f["hours"]) for f in today_faenas if f["completed"])

        return {
            "total": total,
            "completed": completed,
            "total_hours": total_hours,
            "completed_hours": completed_hours,
        }

    @classmethod
    def create_faena(
        cls,
        title: str,
        category: str,
        hours: int,
        week_number: int,
        target_date: str | None = None,
    ) -> dict:
        cls._load_initial_data()

        new_id = max((item["id"] for item in cls._faenas), default=0) + 1
        new_faena = {
            "id": new_id,
            "date": target_date or str(date.today()),
            "title": title.strip(),
            "category": category.strip(),
            "hours": max(0, hours),
            "completed": False,
            "week_number": week_number,
        }

        cls._faenas.append(new_faena)
        cls._save()
        return new_faena

    @classmethod
    def toggle_completed(cls, faena_id: int) -> bool:
        cls._load_initial_data()

        for faena in cls._faenas:
            if faena["id"] == faena_id:
                faena["completed"] = not faena["completed"]
                cls._save()
                return True
        return False

    @classmethod
    def delete_faena(cls, faena_id: int) -> bool:
        cls._load_initial_data()

        before = len(cls._faenas)
        cls._faenas = [f for f in cls._faenas if f["id"] != faena_id]

        if len(cls._faenas) != before:
            cls._save()
            return True
        return False