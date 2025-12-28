import json
from pathlib import Path

class Mod:
    def __init__(self, path: Path):
        self.path = path

        self.id = None
        self.name = None
        self.version = None
        self.author = None
        self.description = None

        self.story_path = path / "story"
        self.mob_path = path / "mobs"
        self.dungeon_path = path / "dungeons"
        self.script_path = path / "scripts"

        self._load_manifest()

    def _load_manifest(self):
        manifest_path = self.path / "mod.json"
        if not manifest_path.exists():
            raise ValueError(f"Missing mod.json in {self.path}")

        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.id = data["id"]
        self.name = data.get("name", self.id)
        self.version = data.get("version", "0.0.0")
        self.author = data.get("author", "Unknown")
        self.description = data.get("description", "")
