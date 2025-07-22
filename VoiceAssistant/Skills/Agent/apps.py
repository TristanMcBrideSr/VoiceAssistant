
import logging
import subprocess
import os
import threading
import inspect

from SkillLink import ArgumentParser

logger = logging.getLogger(__name__)

NAME_REPLACEMENTS = {
    "vs code":     "code",
    "vs studio":   "devenv",
    "vs insiders": "code - insiders",
    "word":        "winword",
    "powerpoint":  "powerpnt",
    "explorer":    "iexplore",
}


## Singleton class for managing application actions
class Apps:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Apps, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.argParser = ArgumentParser()
        self.nameReplacements = NAME_REPLACEMENTS.copy()  # Copy to avoid modifying the original
        self.actionMap = {
            "open-app":  self._openApp,
            "close-app": self._closeApp
        }

    def _metaData(self):
        return {
            "className": f"{self.__class__.__name__}", 
            "description": "Open and close applications on my computer"
        }

    def appSkill(self, action: str, *args):
        self.argParser.printArgs(self, locals())
        try:
            actionKey = self.actionMap.get(action.lower())
            if actionKey is None:
                return f"Invalid {self.__class__.__name__.lower()}Action provided: {action}"

            paramCount = len(inspect.signature(actionKey).parameters)
            return actionKey(*args[:paramCount]) if paramCount > 0 else actionKey()
        except Exception as e:
            logger.error(f"Error executing {self.__class__.__name__.lower()}Action '{action}':", exc_info=True)

    def _normalizeAppName(self, appName: str) -> str:
        app = appName.lower()
        return next(
            (replacement for key, replacement in self.nameReplacements.items() if key in app),
            appName
        )

    def _openApp(self, appName: str) -> str:
        app = self._normalizeAppName(appName)
        try:
            os.startfile(app)
            return f"Opened {app}"
        except Exception as e:
            logger.error(f"Error opening {app}:", exc_info=True)
            return f"An error occurred while trying to open {app}: {e}"

    def _closeApp(self, appName: str) -> str:
        app = self._normalizeAppName(appName)
        if not app.lower().endswith('.exe'):
            app += '.exe'
        try:
            subprocess.run(
                ["taskkill", "/f", "/im", app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return f"Closed {app}"
        except Exception as e:
            logger.error(f"Error closing {app}:", exc_info=True)
            return f"An error occurred while trying to close {app}: {e}"
