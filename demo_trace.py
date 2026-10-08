"""
Interactive Visual Trace Tool for Koor Programming Language.
Shows how Koor processes source code through every stage:
[Source Code] -> [Lexer Tokens] -> [AST Parser Tree] -> [Runtime Execution Output]
"""

import sys
import io

if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from koor.lexer import Lexer
from koor.parser import Parser
from koor.interpreter import Interpreter


def trace_kood(kood: str):
    print("=" * 70)
    print("📜 1. RAW SOURCE CODE:")
    print("=" * 70)
    print(kood.strip())

    print("\n" + "=" * 70)
    print("🔤 2. LEXER TOKENS (How words/symbols are categorized):")
    print("=" * 70)
    lexer = Lexer(kood)
    tokens = lexer.tokens_saar()
    for t in tokens:
        print(f"  {t.nooc:<20} | {repr(t.qiimo):<30} | Sadarka {t.sadar}, Tiirka {t.tiir}")

    print("\n" + "=" * 70)
    print("🌳 3. ABSTRACT SYNTAX TREE (AST - Grammar Structure):")
    print("=" * 70)
    parser = Parser(tokens)
    ast = parser.parse()
    import pprint
    pprint.pprint(ast, indent=2, width=80)

    print("\n" + "=" * 70)
    print("🚀 4. RUNTIME EXECUTION (Virtual Interpreter Output):")
    print("=" * 70)
    vm = Interpreter()
    vm.fuli(ast)
    print("=" * 70)
    print("✅ Completed successfully!")


if __name__ == "__main__":
    tusaale = '''
x waa 12.
haddi x ay la mid tahay 12 waxaad soo saartaa " waad guulaysatay ".
waxaad ku dartaa 8 x.
waxaad soo saartaa "X hadda waa: {x}".
'''
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            tusaale = f.read()

    trace_kood(tusaale)
