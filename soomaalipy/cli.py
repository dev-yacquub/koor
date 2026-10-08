"""
SoomaaliPy - Command Line Interface (CLI).
Aaladda khadka taliska ee SoomaaliPy.
"""

import sys
import os
import argparse
from typing import List, Optional

# Ensure UTF-8 output on Windows consoles
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

from .transpiler import to_python, to_somali, TranspileError
from .runtime import run_file, run_code
from .repl import start_repl, VERSION
from .errors import print_somali_exception


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="somali",
        description="🇸🇴 SoomaaliPy - Luuqadda Barnaamijyada ee Af-Soomaaliga (Somali Python)",
        epilog="Tusaalooyin:\n"
               "  somali run barnaamij.so       # Fuli koodka Soomaaliga\n"
               "  somali repl                   # Bilow REPL-ka tooska ah\n"
               "  somali transpile file.so -o out.py  # U beddel Python caadi ah\n"
               "  somali to-somali app.py -o out.so   # U beddel Python Af-Soomaali\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version", version=f"SoomaaliPy {VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Awaamiirta la heli karo")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Fuli faylka koodka Af-Soomaaliga (.so)")
    run_parser.add_argument("file", help="Faylka koodka (.so ama .sompy)")
    run_parser.add_argument("args", nargs=argparse.REMAINDER, help="Doodaha loo gudbinayo barnaamijka")

    # Command: repl
    subparsers.add_parser("repl", help="Bilow qolka tijaabada tooska ah (REPL)")

    # Command: transpile
    trans_parser = subparsers.add_parser("transpile", help="U beddel koodka Soomaaliga una rog Python")
    trans_parser.add_argument("file", help="Faylka Af-Soomaaliga")
    trans_parser.add_argument("-o", "--output", help="Faylka lagu keydinayo koodka Python")

    # Command: to-somali
    to_so_parser = subparsers.add_parser("to-somali", help="U beddel koodka Python una rog Af-Soomaali")
    to_so_parser.add_argument("file", help="Faylka Python (.py)")
    to_so_parser.add_argument("-o", "--output", help="Faylka lagu keydinayo koodka Soomaaliga")

    # Command: check
    check_parser = subparsers.add_parser("check", help="Hubi naxwaha iyo qoraalka faylka")
    check_parser.add_argument("file", help="Faylka la hubinayo")

    return parser


def main(args: Optional[List[str]] = None) -> int:
    if args is None:
        args = sys.argv[1:]

    parser = build_parser()

    # If no arguments given, or just running a file directly (e.g. `somali script.so`)
    if not args:
        start_repl()
        return 0

    first_arg = args[0]
    if first_arg not in ("run", "repl", "transpile", "to-somali", "check", "-h", "--help", "-v", "--version"):
        # If the first argument is an existing file, default to "run"
        if os.path.exists(first_arg) or first_arg.endswith((".so", ".sompy", ".py")):
            args = ["run"] + args

    parsed = parser.parse_args(args)

    if parsed.command == "repl":
        start_repl()
        return 0

    elif parsed.command == "run":
        target_file = parsed.file
        # Pass remaining args through sys.argv
        sys.argv = [target_file] + (parsed.args or [])
        success = run_file(target_file)
        return 0 if success else 1

    elif parsed.command == "transpile":
        target_file = parsed.file
        if not os.path.exists(target_file):
            print(f"Khalad: Faylka '{target_file}' lama helin.", file=sys.stderr)
            return 1
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            py_code = to_python(content)
        except TranspileError as exc:
            print_somali_exception(exc, filename=target_file, source_code=content)
            return 1

        if parsed.output:
            with open(parsed.output, "w", encoding="utf-8") as f:
                f.write(py_code)
            print(f"✅ Si guul leh ayaa loogu beddelay: {parsed.output}")
        else:
            print(py_code)
        return 0

    elif parsed.command == "to-somali":
        target_file = parsed.file
        if not os.path.exists(target_file):
            print(f"Khalad: Faylka '{target_file}' lama helin.", file=sys.stderr)
            return 1
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        so_code = to_somali(content)
        if parsed.output:
            with open(parsed.output, "w", encoding="utf-8") as f:
                f.write(so_code)
            print(f"✅ Si guul leh ayaa loogu beddelay Af-Soomaali: {parsed.output}")
        else:
            print(so_code)
        return 0

    elif parsed.command == "check":
        target_file = parsed.file
        if not os.path.exists(target_file):
            print(f"Khalad: Faylka '{target_file}' lama helin.", file=sys.stderr)
            return 1
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            py_code = to_python(content)
            compile(py_code, target_file, "exec")
            print(f"✅ Koodka faylka '{target_file}' waa sax, wax khalad ah lagama helin!")
            return 0
        except BaseException as exc:
            print_somali_exception(exc, filename=target_file, source_code=content)
            return 1

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
