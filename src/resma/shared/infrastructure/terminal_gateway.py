import os
from typing import Optional, Tuple


class SystemCommandGateway:
    @staticmethod
    def run(command: str, cwd: Optional[str] = None) -> Tuple[int, Optional[Exception]]:
        try:
            if cwd:
                old_cwd = os.getcwd()
                os.chdir(cwd)
            code = os.system(command)
            return code, None
        except Exception as e:
            return -1, e
        finally:
            if cwd:
                os.chdir(old_cwd)
