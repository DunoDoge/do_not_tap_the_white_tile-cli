from dataclasses import dataclass
from datetime import datetime
import json
import os
from typing import List, Optional


@dataclass
class ScoreRecord:
    score: int
    mode: str
    timestamp: str
    max_combo: int = 0

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "mode": self.mode,
            "timestamp": self.timestamp,
            "max_combo": self.max_combo
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScoreRecord":
        return cls(
            score=data["score"],
            mode=data["mode"],
            timestamp=data["timestamp"],
            max_combo=data.get("max_combo", 0)
        )


class ScoreManager:
    def __init__(self, file_path: str = "scores.json"):
        self.file_path = file_path
        self.scores: List[ScoreRecord] = []
        self._load_scores()

    def _load_scores(self) -> None:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.scores = [ScoreRecord.from_dict(record) for record in data]
            except (json.JSONDecodeError, KeyError):
                self.scores = []
        else:
            self.scores = []

    def _save_scores(self) -> None:
        data = [record.to_dict() for record in self.scores]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_score(self, score: int, mode: str, max_combo: int = 0) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = ScoreRecord(
            score=score,
            mode=mode,
            timestamp=timestamp,
            max_combo=max_combo
        )
        self.scores.append(record)
        self._save_scores()

    def get_top_scores(self, mode: str, limit: int = 10) -> List[ScoreRecord]:
        filtered_scores = [record for record in self.scores if record.mode == mode]
        sorted_scores = sorted(filtered_scores, key=lambda x: x.score, reverse=True)
        return sorted_scores[:limit]
