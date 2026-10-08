"""
SoomaaliPy - Transpiler & Token Translation Engine.
Waxay u turjumtaa koodka Af-Soomaaliga una beddeshaa Python sax ah,
iyadoo ilaalinaysa xariiqyada, faallada, iyo qoraallada (strings).
"""

import io
import tokenize
from typing import Dict, List, Tuple, Optional, Set

from .tokens import (
    SOMALI_TO_PYTHON_KEYWORDS,
    SOMALI_TO_PYTHON_BUILTINS,
    SOMALI_TO_PYTHON_EXCEPTIONS,
    ALL_SOMALI_TO_PYTHON,
    ALL_PYTHON_TO_SOMALI,
    PYTHON_TO_SOMALI_KEYWORDS,
    PYTHON_TO_SOMALI_BUILTINS,
    PYTHON_TO_SOMALI_EXCEPTIONS,
)

# Noocyada xogta (Types) ee magac ahaan loo adeegsan karo doorsoome ahaan (variables)
# Waxaa la beddelaa oo keliya marka ay hawl ahaan u yeeraan e.g. tiro(x), qoraal(x), liis()
SOMALI_TYPE_BUILTINS: Set[str] = {
    "tiro", "tiro_idil", "jajab", "qoraal", "xaqiijin",
    "liis", "qaamuus", "urur", "lamaane", "nooc"
}

PYTHON_TYPE_BUILTINS: Set[str] = {
    "int", "float", "str", "bool", "list", "dict", "set", "tuple", "type"
}


class TranspileError(Exception):
    """Khalad ku yimid turjumidda koodka."""
    def __init__(self, message: str, line: int = 1, col: int = 0):
        super().__init__(f"Khalad Qoraal xariiqda {line}, tiirka {col}: {message}")
        self.line = line
        self.col = col
        self.message = message


def _get_next_significant_token(tokens: List[tokenize.TokenInfo], start_idx: int) -> Optional[tokenize.TokenInfo]:
    """Hel calaamadda (token) xigta ee aan ahayn meel banaan ama faallo."""
    for j in range(start_idx, len(tokens)):
        t = tokens[j]
        if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT):
            return t
    return None


def to_python(source_code: str) -> str:
    """
    U beddel koodka Af-Soomaaliga una beddel koodka caadiga ah ee Python.
    
    Waxay ilaalisaa:
    1. Qoraallada u dhexeeya xigashooyinka (strings & f-strings)
    2. Faallooyinka (# comments)
    3. Kala fogaanshaha (indentation)
    4. Xariiqyada (1-to-1 line correspondence for error traces)
    """
    if not source_code:
        return ""

    try:
        token_stream = tokenize.tokenize(io.BytesIO(source_code.encode("utf-8")).readline)
        tokens = list(token_stream)
    except tokenize.TokenError as exc:
        msg, (sline, scol) = exc.args
        raise TranspileError(f"Naxwaha koodka baa qabyo ah ({msg})", line=sline, col=scol) from exc
    except IndentationError as exc:
        raise TranspileError(f"Kala fogaanshaha xariiqyada baa khaldan: {exc.msg}", line=exc.lineno or 1) from exc

    # Split lines preserving original endings
    lines = source_code.splitlines(keepends=True)
    if not lines:
        return ""

    # Group replacements by line index: {line_idx: [(scol, ecol, replacement)]}
    replacements: Dict[int, List[Tuple[int, int, str]]] = {}

    prev_tok: Optional[tokenize.TokenInfo] = None
    i = 0
    num_tokens = len(tokens)

    while i < num_tokens:
        tok = tokens[i]

        # Ignore non-name tokens
        if tok.type != tokenize.NAME:
            prev_tok = tok
            i += 1
            continue

        # Check if this token is an attribute access (e.g. `obj.shaqo`)
        is_attribute = (prev_tok is not None and prev_tok.type == tokenize.OP and prev_tok.string == ".")
        
        name = tok.string
        line_idx = tok.start[0] - 1
        scol = tok.start[1]
        ecol = tok.end[1]

        # Check for two-word combos like `haddii kale` -> `elif`
        if name == "haddii" and i + 1 < num_tokens:
            next_tok = tokens[i + 1]
            if next_tok.type == tokenize.NAME and next_tok.string == "kale":
                if next_tok.start[0] - 1 == line_idx:
                    replacements.setdefault(line_idx, []).append((scol, next_tok.end[1], "elif"))
                    prev_tok = next_tok
                    i += 2
                    continue

        # Check for two-word combo `ma aha` -> `not`
        if name == "ma" and i + 1 < num_tokens:
            next_tok = tokens[i + 1]
            if next_tok.type == tokenize.NAME and next_tok.string == "aha":
                if next_tok.start[0] - 1 == line_idx:
                    replacements.setdefault(line_idx, []).append((scol, next_tok.end[1], "not"))
                    prev_tok = next_tok
                    i += 2
                    continue

        # Check for two-word combo `ma ku` / `ma ku_jira` -> `not in`
        if name == "ma" and i + 1 < num_tokens:
            next_tok = tokens[i + 1]
            if next_tok.type == tokenize.NAME and next_tok.string in ("ku", "ku_jira"):
                if next_tok.start[0] - 1 == line_idx:
                    replacements.setdefault(line_idx, []).append((scol, next_tok.end[1], "not in"))
                    prev_tok = next_tok
                    i += 2
                    continue

        # Don't translate attribute accesses unless they are illegal in Python
        if is_attribute:
            prev_tok = tok
            i += 1
            continue

        # 1. Keywords (always translate)
        if name in SOMALI_TO_PYTHON_KEYWORDS:
            py_word = SOMALI_TO_PYTHON_KEYWORDS[name]
            replacements.setdefault(line_idx, []).append((scol, ecol, py_word))

        # 2. Builtins & Types
        elif name in SOMALI_TO_PYTHON_BUILTINS:
            next_sig = _get_next_significant_token(tokens, i + 1)
            # If it's a type name (qoraal, tiro, liis, etc.)
            if name in SOMALI_TYPE_BUILTINS:
                # Only translate if followed by '(' like qoraal(x) or tiro("5")
                if next_sig is not None and next_sig.type == tokenize.OP and next_sig.string == "(":
                    py_word = SOMALI_TO_PYTHON_BUILTINS[name]
                    replacements.setdefault(line_idx, []).append((scol, ecol, py_word))
                # Otherwise keep as user variable (e.g. qoraal = "salaan", daabac(qoraal))
            else:
                # Regular built-in functions (daabac, dherer, tirsan, isku_dar, etc.)
                # Check if it's being assigned to as a variable: daabac = ...
                if next_sig is not None and next_sig.type == tokenize.OP and next_sig.string in ("=", "+=", "-="):
                    pass # User variable assignment
                else:
                    py_word = SOMALI_TO_PYTHON_BUILTINS[name]
                    replacements.setdefault(line_idx, []).append((scol, ecol, py_word))

        # 3. Exceptions (always translate)
        elif name in SOMALI_TO_PYTHON_EXCEPTIONS:
            py_word = SOMALI_TO_PYTHON_EXCEPTIONS[name]
            replacements.setdefault(line_idx, []).append((scol, ecol, py_word))

        prev_tok = tok
        i += 1

    # Apply replacements from right to left on each line
    result_lines: List[str] = []
    for idx, line in enumerate(lines):
        if idx in replacements:
            line_repls = sorted(replacements[idx], key=lambda item: item[0], reverse=True)
            new_line = line
            for s_col, e_col, replacement in line_repls:
                new_line = new_line[:s_col] + replacement + new_line[e_col:]
            result_lines.append(new_line)
        else:
            result_lines.append(line)

    return "".join(result_lines)


def to_somali(python_code: str) -> str:
    """
    U beddel koodka caadiga ah ee Python una beddel koodka Af-Soomaaliga.
    Waxaa loo adeegsadaa barashada iyo u rogida koodkii hore mid Soomaali ah.
    """
    if not python_code:
        return ""

    try:
        token_stream = tokenize.tokenize(io.BytesIO(python_code.encode("utf-8")).readline)
        tokens = list(token_stream)
    except Exception:
        return _fallback_to_somali(python_code)

    lines = python_code.splitlines(keepends=True)
    if not lines:
        return ""

    replacements: Dict[int, List[Tuple[int, int, str]]] = {}
    prev_tok: Optional[tokenize.TokenInfo] = None
    num_tokens = len(tokens)

    for i, tok in enumerate(tokens):
        if tok.type != tokenize.NAME:
            prev_tok = tok
            continue

        is_attribute = (prev_tok is not None and prev_tok.type == tokenize.OP and prev_tok.string == ".")
        name = tok.string
        line_idx = tok.start[0] - 1
        scol = tok.start[1]
        ecol = tok.end[1]

        if not is_attribute:
            if name in PYTHON_TO_SOMALI_KEYWORDS:
                so_word = PYTHON_TO_SOMALI_KEYWORDS[name]
                replacements.setdefault(line_idx, []).append((scol, ecol, so_word))
            elif name in PYTHON_TO_SOMALI_BUILTINS:
                next_sig = _get_next_significant_token(tokens, i + 1)
                if name in PYTHON_TYPE_BUILTINS:
                    if next_sig is not None and next_sig.type == tokenize.OP and next_sig.string == "(":
                        so_word = PYTHON_TO_SOMALI_BUILTINS[name]
                        replacements.setdefault(line_idx, []).append((scol, ecol, so_word))
                else:
                    so_word = PYTHON_TO_SOMALI_BUILTINS[name]
                    replacements.setdefault(line_idx, []).append((scol, ecol, so_word))
            elif name in PYTHON_TO_SOMALI_EXCEPTIONS:
                so_word = PYTHON_TO_SOMALI_EXCEPTIONS[name]
                replacements.setdefault(line_idx, []).append((scol, ecol, so_word))

        prev_tok = tok

    result_lines: List[str] = []
    for idx, line in enumerate(lines):
        if idx in replacements:
            line_repls = sorted(replacements[idx], key=lambda item: item[0], reverse=True)
            new_line = line
            for s_col, e_col, replacement in line_repls:
                new_line = new_line[:s_col] + replacement + new_line[e_col:]
            result_lines.append(new_line)
        else:
            result_lines.append(line)

    return "".join(result_lines)


def _fallback_to_somali(code: str) -> str:
    """Beddel fudud haddii naxwuhu qabyo yahay."""
    res = code
    for py_w, so_w in ALL_PYTHON_TO_SOMALI.items():
        res = res.replace(py_w, so_w)
    return res
