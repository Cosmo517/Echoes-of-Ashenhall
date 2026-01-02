from lupa import LuaRuntime


class LuaScriptEnvironment:
    def __init__(self, lua_runtime: LuaRuntime, module, script_path):
        self.lua = lua_runtime
        self.module = module
        self.script_path = script_path

        self._validate()

    def _validate(self):
        if "generate" not in self.module:
            raise RuntimeError(
                f"Lua dungeon script '{self.script_path}' "
                f"does not define required function: generate(dungeon, context)"
            )

    def generate(self, dungeon, lua_context):
        try:
            self.module.generate(dungeon, lua_context)
        except Exception as e:
            raise RuntimeError(
                f"Error executing Lua dungeon generator '{self.script_path}': {e}"
            ) from e
