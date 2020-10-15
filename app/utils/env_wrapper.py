# -*- coding: utf-8 -*-
"""
Wrapper around os.environ
"""


class Env:
    """
    Convenience wrapper around os.environ
    """
    def __init__(self):
        import os
        self._env = os.environ

    def get(self, var, default=None):
        return self._env.get(var, default)

    def set(self, var, value=None):
        if value is None:
            if self.get(var) is not None:
                del self._env[var]
        else:
            self._env[var] = value

    def int(self, var, default=None) -> int:
        val = self.get(var, default)
        return int(val) if val is not None and (isinstance(val, int) or val.isdigit()) else None

    def bool(self, var, default=None) -> bool:
        val = self.get(var, default)
        if isinstance(val, (bool, int)):
            return not not val
        return True if val and any([val.startswith(v) for v in ('T', 't', '1', 'on', 'Y', 'y', 'ena')]) else False
