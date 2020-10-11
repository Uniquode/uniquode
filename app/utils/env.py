# -*- coding: utf-8 -*-
import os
from string import Template
from typing import Union, List, Dict

__all__ = (
    'load',
)

DEFAULT_ENVKEY = 'ENV'
DEFAULT_DOTENV = '.env'
DEFAULT_ENVPATH = ('.', '..', '../..')


def _env_files(env_file, search_path):
    """ expand env_file with full search path """
    processed = []
    for directory in search_path:
        env_path = os.path.join(directory, env_file)
        if os.access(env_path, os.R_OK):
            processed.append(env_path)
    return processed


def _process_env(env_file: str, search_path: List[str], environ: dict, overwrite: bool) -> None:
    """ search for any env_files in given dir list and populate environ dict """

    def process_line(string):
        """ process a single line """
        parts = string.split('=', 1)
        if len(parts) == 2:
            key, val = parts
            if overwrite or environ.get(key) is None:
                environ[key] = val

    for env_path in _env_files(env_file, search_path):
        with open(env_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and line[0] != '#':
                    process_line(line)


def _post_process(environ):
    """ post-process the variables using ${substitutions} """
    for env_key, env_val in environ.items():
        if all(v in env_val for v in ('${', '}')):  # looks like template
            # ignore anything that does not resolve, don't throw an exception!
            val = Template(env_val).safe_substitute(environ)
            if val != env_val:      # don't update unless we need to
                environ[env_key] = val


def _update_os_env(environ: Dict) -> None:
    """ back-populate changed variables to the environment """
    for env_key, env_val in environ.items():
        if env_val != os.environ.get(env_key):
            os.environ[env_key] = env_val


def load(env_file: str = None, search_path: Union[None, List[str], str] = None, overwrite: bool = False) -> None:
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

    # initially populate from os.environ
    environ = {k: v for k, v in os.environ.items()}
    _process_env(env_file, search_path, environ, overwrite)
    _post_process(environ)
    _update_os_env(environ)
