import logging
import json
from datetime import datetime
from pathlib import Path

class LoggingSystem:
    def __init__(self, context=None, log_dir="logs", log_file="debug.log"):
        self.context = context

        Path(log_dir).mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("game")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        if not self.logger.handlers:
            # Create the latest.log logger
            file_handler = logging.FileHandler(Path(log_dir) / log_file, encoding="utf-8", mode="w")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # Create timestamped log handler
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            dated_log_file = f"{timestamp}.log"

            dated_handler = logging.FileHandler(Path(log_dir) / dated_log_file, encoding="utf-8")
            dated_handler.setLevel(logging.DEBUG)
            dated_handler.setFormatter(file_formatter)
            self.logger.addHandler(dated_handler)

        self.log_info("Logging system initialized.")

    # --- General helpers ---
    def log_debug(self, message, **kwargs):
        self._log("DEBUG", message, kwargs)

    def log_info(self, message, **kwargs):
        self._log("INFO", message, kwargs)

    def log_warning(self, message, **kwargs):
        self._log("WARNING", message, kwargs)

    def log_error(self, message, **kwargs):
        self._log("ERROR", message, kwargs)

    def _log(self, level, message, data=None):
        context_info = {}
        if self.context:
            context_info = {
                "level": getattr(self.context, "current_level", None),
                "scene": getattr(self.context, "current_scene", None),
                "state": getattr(self.context, "state", None),
            }

        entry = {
            "time": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "message": message,
            "context": context_info,
            "data": data or {}
        }

        formatted = f"{message} | {json.dumps(entry, ensure_ascii=False)}"
        getattr(self.logger, level.lower())(formatted)

    # --- Event-specific tracing ---
    def log_event_subscribe(self, event_name, subscriber):
        self.log_debug(f"Subscribed: '{event_name}' by {subscriber}")

    def log_event_emit(self, event_name, data):
        self.log_debug(f"Emitted: '{event_name}' data={data}")

    def log_event_dispatch(self, subscriber, event_name, status="handled"):
        self.log_debug(f"Dispatch: {subscriber} -> {status} '{event_name}'")
