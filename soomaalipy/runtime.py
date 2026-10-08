"""
SoomaaliPy - Runtime Environment & Execution Engine.
Waxay bixisaa jawiga shaqada iyo fulinta koodka Af-Soomaaliga.
"""

import os
import sys
import builtins
from typing import Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .tokens import (
    SOMALI_TO_PYTHON_BUILTINS,
    SOMALI_TO_PYTHON_EXCEPTIONS,
)
from .transpiler import to_python, TranspileError
from .errors import print_somali_exception


def somali_help(obj: Any = None) -> None:
    """Caawin Af-Soomaali ah oo ku saabsan SoomaaliPy ama shay gaar ah."""
    if obj is None:
        print("""
🌟 Soo Dhawoow SoomaaliPy (Af-Soomaali Python) 🌟
=====================================================
SoomaaliPy waa luuqad barnaamij oo ku dhisan Python,
adigoo adeegsanaya erayo iyo naxwe Af-Soomaali ah.

Erayada Furaha ah (Keywords):
  haddii (if), haddii_kale (elif), kale (else)
  inta (while), kasta / ee (for), ku / ku_jira (in)
  hawl / shaqo (def), celi (return)
  fasal (class), isku_day (try), qabo (except)
  Run (True), Been (False), Waxba (None)
  iyo (and), ama (or), ma (not), waa (is)

Hawlaha Diyaar-ka-ah (Built-in Functions):
  daabac(...)       -> print()
  geli(...)         -> input()
  dherer(...)       -> len()
  tirsan(...)       -> range()
  isku_dar(...)     -> sum()
  tiro(...)         -> int()
  qoraal(...)       -> str()
  liis(...)         -> list()
  qaamuus(...)      -> dict()
  ka_bax()          -> exit()

Si aad u hesho caawin shay gaar ah: caawin(shayga)
=====================================================
""")
    else:
        builtins.help(obj)


def get_somali_builtins() -> Dict[str, Any]:
    """Abuur qaamuuska hawlaha iyo khaladaadka diyaar-ka-ah ee Af-Soomaaliga."""
    env: Dict[str, Any] = {}

    # Map Somali names to Python built-in functions
    for so_name, py_name in SOMALI_TO_PYTHON_BUILTINS.items():
        if hasattr(builtins, py_name):
            env[so_name] = getattr(builtins, py_name)

    # Map Somali exception names to Python exception classes
    for so_name, py_name in SOMALI_TO_PYTHON_EXCEPTIONS.items():
        if hasattr(builtins, py_name):
            env[so_name] = getattr(builtins, py_name)

    # Custom/Somali specialized builtins
    env["caawin"] = somali_help
    env["ka_bax"] = sys.exit
    env["bax"] = sys.exit
    env["Run"] = True
    env["run"] = True
    env["Been"] = False
    env["been"] = False
    env["Waxba"] = None
    env["waxba"] = None
    env["Eber"] = None
    env["eber"] = None

    return env


def inject_somali_builtins() -> None:
    """Ku dar hawlaha Soomaaliga qaybta guud ee builtins ee Python."""
    somali_env = get_somali_builtins()
    for name, func in somali_env.items():
        setattr(builtins, name, func)


def run_code(
    source: str,
    filename: str = "<kood>",
    global_vars: Optional[Dict[str, Any]] = None,
    raise_exceptions: bool = False,
) -> bool:
    """
    U turjun oo fuli koodka Af-Soomaaliga.
    
    Soo celi True haddii si guul leh u socday, False haddii khalad dhacay.
    """
    inject_somali_builtins()

    try:
        py_code = to_python(source)
    except TranspileError as exc:
        if raise_exceptions:
            raise
        print_somali_exception(exc, filename=filename, source_code=source)
        return False
    except Exception as exc:
        if raise_exceptions:
            raise
        print_somali_exception(exc, filename=filename, source_code=source)
        return False

    if global_vars is None:
        global_vars = {
            "__name__": "__main__",
            "__file__": os.path.abspath(filename) if os.path.exists(filename) else filename,
            "__doc__": None,
        }
        global_vars.update(get_somali_builtins())

    try:
        compiled = compile(py_code, filename, "exec")
        exec(compiled, global_vars)
        return True
    except BaseException as exc:
        if isinstance(exc, SystemExit):
            raise
        if raise_exceptions:
            raise
        print_somali_exception(exc, filename=filename, source_code=source)
        return False


def run_file(filepath: str, raise_exceptions: bool = False) -> bool:
    """Akhri oo fuli faylka koodka Af-Soomaaliga (.so / .sompy / .spy)."""
    if not os.path.exists(filepath):
        from .errors import format_somali_traceback
        exc = FileNotFoundError(f"Faylka la furayey lama helin: {filepath}")
        print_somali_exception(exc, filename=filepath)
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    # Add directory of the file to sys.path so local imports work
    file_dir = os.path.dirname(os.path.abspath(filepath))
    if file_dir not in sys.path:
        sys.path.insert(0, file_dir)

    return run_code(source, filename=filepath, raise_exceptions=raise_exceptions)
