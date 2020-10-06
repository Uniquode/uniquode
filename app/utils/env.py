# -*- coding: utf-8 -*-
import os
from string import Template
from typing import Union

__all__ = (
    'load',
)

DEFAULT_ENVKEY = 'ENV'
DEFAULT_DOTENV = '.env'
DEFAULT_ENVPATH = ('.', '..', '../..')


def load(env_file: str = None, search_path: Union[list, str] = None, overwrite=False) -> list:
    """
    Loads one or more .env files with optional nesting, updating os.environ
    :param env_file: name of the
    :param search_path: single or list of directories in order of precedence
    :param overwrite: whether to overwrite existing values
    :returns list of .env files processed
    """
    if not env_file:
        env_file = os.environ.get(DEFAULT_ENVKEY, DEFAULT_DOTENV)

    if search_path is None:
        search_path = DEFAULT_ENVPATH
    elif isinstance(search_path, (str, bytes)):
        search_path = [search_path]
    # if overwriting, traverse path in reverse order
    if overwrite:
        search_path.reverse()

    processed = []
    environ = {k: v for k, v in os.environ.items()}

    for directory in search_path:
        env_path = os.path.join(directory, env_file)
        if os.access(env_path, os.R_OK):
            with open(env_path, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line and line[0] != '#':
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            key, val = parts
                            if overwrite or os.environ.get(key) is None:
                                environ[key] = val
                processed.append(env_path)

    # post-process the variables changed for ${substitutions}
    for env_key in list(environ.keys()):
        env_val = environ[env_key]
        if all(v in env_val for v in ('${', '}')):      # looks like template
            val = Template(env_val).safe_substitute(environ)
            if val != env_val:  # prefer not to change
                environ[env_key] = val

    # back-populate changed variables to the environment
    for env_key in list(environ.keys()):
        env_val = environ[env_key]
        if env_val != os.environ.get(env_key):
            os.environ[env_key] = env_val

    return processed
