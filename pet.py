"""毒舌学习搭子 —— 养成逻辑与 JSON 文件记忆"""
import json
from datetime import date, timedelta

DEFAULT_MEMORY_FILE = "pet_memory.json"

STAGES = [
    {"name": "蛋蛋", "min_exp": 0},
    {"name": "幼年体", "min_exp": 20},
    {"name": "成长期", "min_exp": 60},
    {"name": "大佬搭子", "min_exp": 120},
]

CHECKIN_EXP = 15
CHECKIN_HEARTS = 5
SKIP_HEARTS = 10
MAX_HEARTS = 100


class Pet:
    """毒舌学习搭子的养成状态，所有数据落在 JSON 文件里。"""

    def __init__(self, memory_file: str = DEFAULT_MEMORY_FILE):
        self.memory_file = memory_file
        raw = self._load()
        self.name = str(raw.get("name") or "蛋蛋")
        self.exp = max(0, self._as_int(raw.get("exp"), 0))
        self.hearts = min(MAX_HEARTS, max(0, self._as_int(raw.get("hearts"), 50)))
        self.streak = max(0, self._as_int(raw.get("streak"), 0))
        self.last_checkin = str(raw.get("last_checkin", ""))
        self.total_checkins = max(0, self._as_int(raw.get("total_checkins"), 0))
        self.skipped = max(0, self._as_int(raw.get("skipped"), 0))
        recent = raw.get("recent", [])
        self.recent = recent if isinstance(recent, list) else []
        self._save()

    # ---------- 文件读写 ----------
    def _load(self) -> dict:
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    def _save(self) -> None:
        data = {
            "name": self.name,
            "exp": self.exp,
            "hearts": self.hearts,
            "streak": self.streak,
            "last_checkin": self.last_checkin,
            "total_checkins": self.total_checkins,
            "skipped": self.skipped,
            "recent": self.recent,
        }
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    @staticmethod
    def _as_int(value, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    # ---------- 养成等级 ----------
    def stage_index(self) -> int:
        idx = 0
        for i, stage in enumerate(STAGES):
            if self.exp >= stage["min_exp"]:
                idx = i
        return idx

    def stage(self) -> dict:
        return STAGES[self.stage_index()]

    def stage_name(self) -> str:
        return self.stage()["name"]

    def next_stage(self):
        i = self.stage_index()
        return STAGES[i + 1] if i + 1 < len(STAGES) else None

    def stage_progress(self) -> float:
        i = self.stage_index()
        if i + 1 >= len(STAGES):
            return 1.0
        cur = STAGES[i]["min_exp"]
        nxt = STAGES[i + 1]["min_exp"]
        return min(1.0, max(0.0, (self.exp - cur) / (nxt - cur)))

    # ---------- 打卡 / 鸽 ----------
    def checkin(self, today: str = "") -> dict:
        today = today or date.today().isoformat()
        if self.last_checkin == today:
            return {"status": "already", "message": "今天已经打过卡了，重复打卡无效。"}

        if self.last_checkin == self._yesterday(today):
            self.streak += 1
        else:
            self.streak = 1
        self.last_checkin = today
        self.total_checkins += 1
        self.exp += CHECKIN_EXP
        self.hearts = min(MAX_HEARTS, self.hearts + CHECKIN_HEARTS)
        self._save()
        return {
            "status": "ok",
            "message": (
                f"打卡成功！经验+{CHECKIN_EXP}，好感+{CHECKIN_HEARTS}，"
                f"连续打卡 {self.streak} 天。"
            ),
        }

    def skip(self, today: str = "") -> dict:
        today = today or date.today().isoformat()
        if self.last_checkin == today:
            return {"status": "conflict", "message": "今天已经打过卡了，不能再算鸽。"}

        self.hearts = max(0, self.hearts - SKIP_HEARTS)
        self.streak = 0
        self.skipped += 1
        self._save()
        return {
            "status": "ok",
            "message": (
                f"已记录鸽了 1 次：好感-{SKIP_HEARTS}，连续打卡清零，被鸽 {self.skipped} 次。"
            ),
        }

    @staticmethod
    def _yesterday(today: str) -> str:
        return (date.fromisoformat(today) - timedelta(days=1)).isoformat()

    # ---------- 记忆 ----------
    def remember(self, role: str, content: str) -> None:
        self.recent.append({"role": role, "content": content})
        self.recent = self.recent[-20:]
        self._save()
