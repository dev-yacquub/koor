"""
SoomaaliPy - Interactive Somali REPL (Read-Eval-Print Loop).
Waxay suurtagelinaysaa in koodka Af-Soomaaliga lagu tijaabiyo khadka tooska ah.
"""

import sys
from typing import Dict, Any

from .runtime import inject_somali_builtins, get_somali_builtins
from .transpiler import to_python, TranspileError
from .errors import print_somali_exception

VERSION = "1.0.0"

BANNER = f"""
🇸🇴 SoomaaliPy {VERSION} (Af-Soomaali Python)
Qor koodkaaga Af-Soomaali toos ah.
Ku qor 'caawin()' si aad u hesho caawin, ama 'ka_bax()' si aad uga baxdo.
------------------------------------------------------------
"""


def start_repl() -> None:
    """Bilow REPL-ka isdhexgalka ah ee SoomaaliPy."""
    inject_somali_builtins()
    print(BANNER)

    namespace: Dict[str, Any] = {
        "__name__": "__repl__",
        "__doc__": None,
    }
    namespace.update(get_somali_builtins())

    buffer = []
    in_multiline = False

    while True:
        try:
            prompt = "...   " if in_multiline else "soom> "
            try:
                line = input(prompt)
            except EOFError:
                print("\nNabad gelyo!")
                break

            # Handle blank line in multiline mode (execute buffer)
            if in_multiline:
                if line.strip() == "":
                    # Empty line submits multiline block
                    full_code = "\n".join(buffer)
                    buffer = []
                    in_multiline = False
                    _execute_block(full_code, namespace)
                    continue
                else:
                    buffer.append(line)
                    continue

            stripped = line.strip()

            if not stripped:
                continue

            if stripped in ("ka_bax()", "ka_bax", "exit()", "quit()", "bax"):
                print("Nabad gelyo!")
                break

            # Check if block starts a multiline construct (ends with ':')
            if stripped.endswith(":") or stripped.startswith(("@", "hawl ", "shaqo ", "fasal ", "haddii ", "inta ", "kasta ", "ee ", "isku_day:")):
                buffer.append(line)
                in_multiline = True
                continue

            # Check for unmatched parentheses/brackets
            open_count = line.count("(") + line.count("[") + line.count("{")
            close_count = line.count(")") + line.count("]") + line.count("}")
            if open_count > close_count:
                buffer.append(line)
                in_multiline = True
                continue

            # Execute single line
            _execute_line_or_expr(line, namespace)

        except KeyboardInterrupt:
            print("\nJoojin (Ctrl+C). Qor 'ka_bax()' si aad u baxdo.")
            buffer = []
            in_multiline = False


def _execute_line_or_expr(line: str, namespace: Dict[str, Any]) -> None:
    """Isku day inaad marka hore u qiimeyso sidii expression, haddii kalena statement."""
    try:
        py_code = to_python(line).strip()
    except TranspileError as exc:
        print_somali_exception(exc, filename="<repl>", source_code=line)
        return

    # First attempt: evaluate as expression (print result like Python REPL)
    try:
        compiled = compile(py_code, "<repl>", "eval")
        result = eval(compiled, namespace)
        if result is not None:
            # Print Somali representation of booleans/None if desired
            if result is True:
                print("Run")
            elif result is False:
                print("Been")
            elif result is None:
                pass
            else:
                print(repr(result))
        return
    except SyntaxError:
        # Not an expression, try as statement
        pass
    except BaseException as exc:
        if isinstance(exc, SystemExit):
            raise
        print_somali_exception(exc, filename="<repl>", source_code=line)
        return

    # Second attempt: execute as statement
    try:
        compiled = compile(py_code, "<repl>", "exec")
        exec(compiled, namespace)
    except BaseException as exc:
        if isinstance(exc, SystemExit):
            raise
        print_somali_exception(exc, filename="<repl>", source_code=line)


def _execute_block(code: str, namespace: Dict[str, Any]) -> None:
    """Fuli kood dhowr xariiq ah."""
    try:
        py_code = to_python(code)
        compiled = compile(py_code, "<repl>", "exec")
        exec(compiled, namespace)
    except BaseException as exc:
        if isinstance(exc, SystemExit):
            raise
        print_somali_exception(exc, filename="<repl>", source_code=code)
