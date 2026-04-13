from copy import deepcopy

from core.data.roadmap_seed import ROADMAP_WEEKS
from core.services.storage_service import StorageService


class RoadmapService:
    _weeks: list[dict] | None = None

    @classmethod
    def _load_initial_data(cls) -> None:
        if cls._weeks is not None:
            return

        cached_data = StorageService.load_json(StorageService.ROADMAP_FILE)

        if cached_data is not None:
            cls._weeks = cached_data
        else:
            cls._weeks = deepcopy(ROADMAP_WEEKS)
            cls._save()

    @classmethod
    def _save(cls) -> None:
        if cls._weeks is None:
            return
        StorageService.save_json(StorageService.ROADMAP_FILE, cls._weeks)

    @classmethod
    def reset_to_seed(cls) -> None:
        cls._weeks = deepcopy(ROADMAP_WEEKS)
        cls._save()

    @classmethod
    def get_all_weeks(cls) -> list[dict]:
        cls._load_initial_data()
        return cls._weeks

    @classmethod
    def get_week_by_number(cls, week_number: int) -> dict | None:
        cls._load_initial_data()
        for week in cls._weeks:
            if week["week_number"] == week_number:
                return week
        return None

    @classmethod
    def get_current_week(cls) -> dict:
        cls._load_initial_data()
        for week in cls._weeks:
            if week["status"] == "in_progress":
                return week
        return cls._weeks[0]

    @classmethod
    def get_progress_metrics(cls) -> dict:
        cls._load_initial_data()

        total_weeks = len(cls._weeks)
        completed_weeks = sum(1 for week in cls._weeks if week["status"] == "completed")
        in_progress_weeks = sum(1 for week in cls._weeks if week["status"] == "in_progress")

        completion_ratio = completed_weeks / total_weeks if total_weeks else 0

        return {
            "total_weeks": total_weeks,
            "completed_weeks": completed_weeks,
            "in_progress_weeks": in_progress_weeks,
            "completion_ratio": completion_ratio,
        }

    @classmethod
    def update_week_status(cls, week_number: int, new_status: str) -> bool:
        cls._load_initial_data()

        valid_statuses = {"pending", "in_progress", "completed"}
        if new_status not in valid_statuses:
            return False

        target = cls.get_week_by_number(week_number)
        if target is None:
            return False

        if new_status == "in_progress":
            for week in cls._weeks:
                if week["status"] == "in_progress" and week["week_number"] != week_number:
                    week["status"] = "pending"

        target["status"] = new_status

        if new_status == "completed" and target["actual_hours"] == 0:
            target["actual_hours"] = target["planned_hours"]

        if new_status == "pending":
            target["actual_hours"] = 0

        cls._save()
        return True