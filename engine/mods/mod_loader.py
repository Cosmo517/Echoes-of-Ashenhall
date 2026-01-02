from pathlib import Path
from engine.mods.mod import Mod

class ModLoader:
    def __init__(self, mods_dir: Path):
        self.mods_dir = mods_dir
        self.mods: list[Mod] = []

    def load_all(self) -> list[Mod]:
        if not self.mods_dir.exists():
            raise RuntimeError(f"Mods directory not found: {self.mods_dir}")

        for path in self.mods_dir.iterdir():
            if not path.is_dir():
                continue

            try:
                mod = Mod(path)
                self.mods.append(mod)
            except Exception as e:
                print(f"[MOD ERROR] Failed to load {path.name}: {e}")

        self._ensure_base_mod()
        return self.mods

    def get_mod(self, mod_id):
        for mod in self.mods:
            if mod.id == mod_id:
                return mod

    def _ensure_base_mod(self):
        if not any(mod.id == "base" for mod in self.mods):
            raise RuntimeError("Base mod is required but was not found")
