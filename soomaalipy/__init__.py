"""
SoomaaliPy - Luuqadda Barnaamijyada ee Af-Soomaaliga.
Somali Python Programming Language.
"""

from .transpiler import to_python, to_somali, TranspileError
from .runtime import run_code, run_file, get_somali_builtins, inject_somali_builtins
from .repl import start_repl

__version__ = "1.0.0"
__author__ = "SoomaaliPy Contributors"

__all__ = [
    "to_python",
    "to_somali",
    "run_code",
    "run_file",
    "start_repl",
    "get_somali_builtins",
    "inject_somali_builtins",
    "TranspileError",
]
