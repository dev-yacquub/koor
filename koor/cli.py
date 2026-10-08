"""
Command Line Interface (CLI) and REPL for Koor Programming Language.
"""

import sys
import os
import io
import argparse

if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from koor import __version__
from koor.lexer import Lexer
from koor.parser import Parser
from koor.interpreter import Interpreter
from koor.errors import KoorKhalad


def fuli_fayl(fayl_jid: str, muuji_tokens: bool = False, muuji_ast: bool = False):
    if not os.path.exists(fayl_jid):
        print(f"❌ Khalad: Faylka '{fayl_jid}' lama helin.")
        sys.exit(1)

    with open(fayl_jid, 'r', encoding='utf-8-sig') as f:
        kood = f.read()

    try:
        lexer = Lexer(kood, fayl_magac=fayl_jid)
        tokens = lexer.tokens_saar()

        if muuji_tokens:
            print("--- TOKENS ---")
            for t in tokens:
                print(f"  {t}")
            return

        parser = Parser(tokens)
        ast = parser.parse()

        if muuji_ast:
            print("--- AST ---")
            print(ast)
            return

        vm = Interpreter()
        vm.fuli(ast)

    except KoorKhalad as e:
        print(e.habee())
        sys.exit(1)
    except Exception as e:
        print(f"❌ Khalad lama filaan ah: {e}")
        sys.exit(1)


def fur_repl():
    print(f"🇸🇴 Koor {__version__} - Luuqadda Barnaamijyada ee Af-Soomaaliga")
    print("Qor koodkaaga tooska ah. Si aad uga baxdo qor 'ka_bax' ama riix Ctrl+C.\n")

    if sys.platform == "win32":
        try:
            from koor.installer_utils import is_in_user_path
            current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            if not is_in_user_path(current_dir):
                print("💡 Talo: Koor kuma jiro PATH-kaaga. Qor 'koor install' si uu terminal kasta uga shaqeeyo toos.\n")
        except Exception:
            pass

    vm = Interpreter()

    while True:
        try:
            sadar = input("koor> ")
            if not sadar.strip():
                continue
            if sadar.strip() in ("ka_bax", "ka bax", "exit", "quit"):
                print("Nabad gelyo!")
                break

            lexer = Lexer(sadar, fayl_magac="<repl>")
            tokens = lexer.tokens_saar()
            parser = Parser(tokens)
            ast = parser.parse()
            vm.fuli(ast)

        except KoorKhalad as e:
            print(e.habee())
        except (KeyboardInterrupt, EOFError):
            print("\nNabad gelyo!")
            break
        except Exception as e:
            print(f"❌ Khalad: {e}")


def qabso_install(fayl_dir: str = None):
    """Integrates Koor into Windows User PATH and file associations."""
    if sys.platform != "win32":
        print("Amarka 'install' waxa loogu talagalay nidaamka Windows.")
        return

    from koor.installer_utils import (
        add_to_user_path,
        register_file_association,
        create_shortcuts,
        register_windows_uninstall,
        get_default_install_dir,
    )

    exe_path = os.path.abspath(sys.argv[0])
    target_dir = os.path.abspath(fayl_dir) if fayl_dir else os.path.dirname(exe_path)

    print("==================================================")
    print("   RAKIBAADDA KOOR (INSTALLING KOOR TO PATH)    ")
    print("==================================================")

    # 1. Add to PATH
    added = add_to_user_path(target_dir)
    if added:
        print(f"✅ Galka '{target_dir}' waxaa lagu daray User PATH.")
    else:
        print(f"ℹ️ Galka '{target_dir}' horey ayuu ugu jiray User PATH.")

    # 2. Register file association if .exe or bat exists
    reg_assoc = register_file_association(exe_path)
    if reg_assoc:
        print("✅ Faylasha .koor waxaa lagu xiriiriyay Koor (Double-click to run).")
        print("✅ Menu-ga Midig (Right-Click) waxa lagu daray 'Ku wad Koor'.")

    # 3. Create shortcuts
    shortcuts = create_shortcuts(exe_path, desktop=True)
    if shortcuts:
        print(f"✅ Waxaa la sameeyay toobiyaha Start Menu & Desktop ({len(shortcuts)} shortcuts).")

    # 4. Register in Windows Settings / Installed Apps
    register_windows_uninstall(target_dir, exe_path, __version__)

    print("\n==================================================")
    print("   HAMBALYO! KOOR WAA DIYAAR IN TOOS LOO ISTICMAALO!   ")
    print("==================================================")
    print("Hadda waxaad terminal kasta (PowerShell ama CMD) ka qori kartaa:")
    print("   koor run fayl.koor")
    print("   koor repl")
    print("   koor check fayl.koor\n")


def qabso_uninstall():
    """Unregisters Koor from PATH, associations, and shortcuts."""
    if sys.platform != "win32":
        print("Amarka 'uninstall' waxa loogu talagalay nidaamka Windows.")
        return

    from koor.installer_utils import (
        remove_from_user_path,
        unregister_file_association,
        remove_shortcuts,
        unregister_windows_uninstall,
    )

    exe_path = os.path.abspath(sys.argv[0])
    target_dir = os.path.dirname(exe_path)

    print("Ka saaraya Koor nidaamka Windows...")
    remove_from_user_path(target_dir)
    unregister_file_association()
    remove_shortcuts()
    unregister_windows_uninstall()
    print("✅ Koor si guul leh ayaa looga saaray PATH iyo nidaamka.")


def main():
    parser = argparse.ArgumentParser(
        prog="koor",
        description="🇸🇴 Koor - Luuqadda Barnaamijyada ee Af-Soomaaliga Dabiiciga ah"
    )
    subparsers = parser.add_subparsers(dest="command", help="Amarrada Koor")

    # run command
    run_parser = subparsers.add_parser("run", help="Fuli fayl koodka Koor ah (.koor)")
    run_parser.add_argument("fayl", help="Jidka faylka (.koor)")
    run_parser.add_argument("--tokens", action="store_true", help="Muuji liiska tokens-ka")
    run_parser.add_argument("--ast", action="store_true", help="Muuji geedka naxwaha (AST)")

    # repl command
    subparsers.add_parser("repl", help="Fur qolka tijaabada tooska ah (REPL)")

    # check command
    check_parser = subparsers.add_parser("check", help="Hubi naxwaha koodka adigoon fulin")
    check_parser.add_argument("fayl", help="Jidka faylka (.koor)")

    # install command
    install_parser = subparsers.add_parser("install", help="Ku dar Koor PATH-ka nidaamka oo xiriiri faylasha .koor")
    install_parser.add_argument("--dir", default=None, help="Galka lagu darayo PATH (default: galka Koor)")

    # uninstall command
    subparsers.add_parser("uninstall", help="Ka saar Koor PATH-ka iyo nidaamka")

    args = parser.parse_args()

    if args.command == "run":
        fuli_fayl(args.fayl, muuji_tokens=args.tokens, muuji_ast=args.ast)
    elif args.command == "repl":
        fur_repl()
    elif args.command == "check":
        try:
            with open(args.fayl, 'r', encoding='utf-8-sig') as f:
                kood = f.read()
            tokens = Lexer(kood, fayl_magac=args.fayl).tokens_saar()
            Parser(tokens).parse()
            print("✅ Naxwaha koodku waa sax! Wax khalad ah lama helin.")
        except KoorKhalad as e:
            print(e.habee())
            sys.exit(1)
    elif args.command == "install":
        qabso_install(args.dir)
    elif args.command == "uninstall":
        qabso_uninstall()
    else:
        if len(sys.argv) > 1 and sys.argv[1].endswith(".koor"):
            fuli_fayl(sys.argv[1])
        else:
            fur_repl()


if __name__ == "__main__":
    main()
