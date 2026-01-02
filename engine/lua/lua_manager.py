from lupa import LuaRuntime
from pathlib import Path
from engine.lua.lua_script_environment import LuaScriptEnvironment


class LuaManager:
    def __init__(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)

    def load_script(self, script_path: Path) -> LuaScriptEnvironment:
        if not script_path.exists():
            raise FileNotFoundError(f"Lua script not found: {script_path}")

        with open(script_path, "r", encoding="utf-8") as f:
            source = f.read()

        try:
            module = self.lua.execute(source)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load Lua script '{script_path}': {e}"
            ) from e

        return LuaScriptEnvironment(self.lua, module, script_path)
