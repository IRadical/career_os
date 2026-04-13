from core.data.roadmap_seed import ROADMAP_WEEKS


class RoadmapService:
    @staticmethod
    def get_all_weeks() -> list[dict]:
        return ROADMAP_WEEKS

    @staticmethod
    def get_current_week() -> dict:
        for week in ROADMAP_WEEKS:
            if week["status"] == "in_progress":
                return week
        return ROADMAP_WEEKS[0]

    @staticmethod
    def get_progress_metrics() -> dict:
        total_weeks = len(ROADMAP_WEEKS)
        completed_weeks = sum(1 for week in ROADMAP_WEEKS if week["status"] == "completed")
        in_progress_weeks = sum(1 for week in ROADMAP_WEEKS if week["status"] == "in_progress")

        completion_ratio = completed_weeks / total_weeks if total_weeks else 0

        return {
            "total_weeks": total_weeks,
            "completed_weeks": completed_weeks,
            "in_progress_weeks": in_progress_weeks,
            "completion_ratio": completion_ratio,
        }