"""
SoomaaliPy - Error Handler & Traceback Translator.
Waxay u turjumtaa khaladaadka Python luuqadda Af-Soomaaliga,
iyadoo si faahfaahsan oo fudud u caddaynaysa meesha khaladku ka dhacay.
"""

import re
import sys
import traceback
from typing import Optional, List

from .tokens import PYTHON_TO_SOMALI_EXCEPTIONS

# Turjumaadda fariimaha khaladaadka caanka ah ee Python
ERROR_MESSAGE_PATTERNS = [
    # ZeroDivisionError
    (r"division by zero", "Tiro laguma qaybin karo eber (0)."),
    (r"float division by zero", "Jajab laguma qaybin karo eber (0)."),
    (r"integer division or modulo by zero", "Qaybinta tiro ama haraaga laguma samayn karo eber."),
    
    # NameError
    (r"name '([^']+)' is not defined", r"Magaca '\1' lama yaqaan (lama qeexin ka hor intaan la isticmaalin)."),
    
    # IndexError
    (r"list index out of range", "Tusmada liisku waxay ka baxsan tahay xadka liiska."),
    (r"string index out of range", "Tusmada qoraalku waxay ka baxsan tahay dhererka qoraalka."),
    (r"tuple index out of range", "Tusmada lamaanuhu waxay ka baxsan tahay xadka."),
    
    # KeyError
    (r"KeyError: '([^']+)'", r"Furaha '\1' lagama helin qaamuuska gudihiisa."),
    
    # TypeError
    (r"can only concatenate str \(not \"([^\"]+)\"\) to str", r"Qoraalka kuma xiri kartid nooca '\1'. Fadlan marka hore u beddel qoraal adigoo adeegsanaya qoraal()."),
    (r"unsupported operand type\(s\) for ([^:]+): '([^']+)' and '([^']+)'", r"Hawsha \1 laguma samayn karo noocyada kala ah '\2' iyo '\3'."),
    (r"missing (\d+) required positional argument[s]?: (.+)", r"Waxaa dhiman \1 dood (argument) oo qasab ah: \2"),
    (r"'([^']+)' object is not callable", r"Shayga noociisu yahay '\1' maaha hawl (function) la wici karo."),
    (r"'([^']+)' object is not iterable", r"Shayga noociisu yahay '\1' laguma samayn karo wareeg (maaha liis ama taxane)."),
    (r"'([^']+)' object is not subscriptable", r"Shayga noociisu yahay '\1' lagama dhex dooran karo tusmo []"),
    
    # ValueError
    (r"invalid literal for int\(\) with base 10: '([^']*)'", r"Qoraalka '\1' looma beddeli karo tiro buuxda (int)."),
    (r"not enough values to unpack \(expected (\d+), got (\d+)\)", r"Qaybintu way khaldan tahay: waxaa la sugayey \1 qiime, laakiin waxaa la helay \2."),
    (r"too many values to unpack \(expected (\d+)\)", r"Qiimaha la helay ayaa ka badan inta loo baahnaa (\1)."),
    
    # AttributeError
    (r"'([^']+)' object has no attribute '([^']+)'", r"Shayga nooca '\1' ah ma laha sifo ama hawl la yiraahdo '\2'."),
    
    # FileNotFoundError
    (r"\[Errno 2\] No such file or directory: '([^']+)'", r"Faylka ama galka la yiraahdo '\1' lama helin."),
    
    # ModuleNotFoundError / ImportError
    (r"No module named '([^']+)'", r"Qaybta ama xirmada la yiraahdo '\1' lama helin. Hubi magaca ama soo daji adigoo isticmaalaya pip."),
    
    # SyntaxError
    (r"invalid syntax", "Naxwaha koodka baa khaldan (Invalid Syntax)."),
    (r"unexpected EOF while parsing", "Koodku wuu go'ay intaan la dhammaystirin (Unexpected EOF)."),
    (r"expected an indented block after '([^']+)'", r"Waxaa loo baahnaa xariiq hore loo riixay (indentation) ka dib '\1'."),
    (r"unindent does not match any outer indentation level", "Kala fogaanshaha xariiqyada (indentation) ma habboona."),
]


def translate_error_message(eng_msg: str) -> str:
    """U beddel fariinta khaladaadka luuqadda Af-Soomaaliga."""
    if not eng_msg:
        return ""
    
    clean_msg = eng_msg.strip()
    for pattern, somali_template in ERROR_MESSAGE_PATTERNS:
        match = re.search(pattern, clean_msg)
        if match:
            try:
                return re.sub(pattern, somali_template, clean_msg)
            except Exception:
                return somali_template
                
    return clean_msg


def translate_exception_name(exc_type_name: str) -> str:
    """U beddel magaca nooca khaladka magac Soomaali ah."""
    return PYTHON_TO_SOMALI_EXCEPTIONS.get(exc_type_name, exc_type_name)


def format_somali_traceback(
    exc: BaseException,
    filename: str = "<kood>",
    source_code: Optional[str] = None
) -> str:
    """
    Habee fariinta khaladka si qurux badan oo Af-Soomaali ah.
    """
    exc_type = type(exc).__name__
    somali_exc_name = translate_exception_name(exc_type)
    raw_msg = str(exc)
    somali_msg = translate_error_message(raw_msg)
    
    lines_output: List[str] = []
    lines_output.append("=" * 60)
    lines_output.append("⚠️  KHALAD BAA DHACAY (SOOMAALIPY)")
    lines_output.append("=" * 60)
    
    # Get traceback info
    tb = exc.__traceback__
    extracted = traceback.extract_tb(tb) if tb else []
    
    # SyntaxError has line info directly on the exception
    if isinstance(exc, SyntaxError):
        lineno = exc.lineno or 1
        offset = exc.offset or 1
        lines_output.append(f"📄 Faylka: {filename}")
        lines_output.append(f"📍 Xariiqda: {lineno}, Tiirka: {offset}")
        if exc.text:
            lines_output.append("")
            lines_output.append(f"   {lineno} | {exc.text.rstrip()}")
            pointer_spaces = " " * (offset - 1 if offset > 0 else 0)
            lines_output.append(f"     | {pointer_spaces}^--- khaladku halkan buu ka bilowday")
    else:
        # Normal runtime exception: find relevant frame in user code
        relevant_frame = None
        for frame in reversed(extracted):
            if frame.filename in (filename, "<string>", "<kood>", "<input>"):
                relevant_frame = frame
                break
        if not relevant_frame and extracted:
            relevant_frame = extracted[-1]
            
        if relevant_frame:
            lineno = relevant_frame.lineno
            lines_output.append(f"📄 Faylka: {filename}")
            lines_output.append(f"📍 Xariiqda: {lineno}")
            
            if source_code:
                code_lines = source_code.splitlines()
                if 1 <= lineno <= len(code_lines):
                    lines_output.append("")
                    # Show previous line if available
                    if lineno > 1:
                        lines_output.append(f"   {lineno - 1:3d} | {code_lines[lineno - 2]}")
                    # Error line
                    lines_output.append(f" > {lineno:3d} | {code_lines[lineno - 1]}")
                    lines_output.append(f"       | ^--- Khaladku xariiqdan buu ku jiraa")
                    # Show next line if available
                    if lineno < len(code_lines):
                        lines_output.append(f"   {lineno + 1:3d} | {code_lines[lineno]}")
    
    lines_output.append("")
    lines_output.append(f"🛑 Nooca Khaladka: {somali_exc_name} ({exc_type})")
    lines_output.append(f"💬 Faahfaahin:     {somali_msg}")
    lines_output.append("=" * 60)
    
    return "\n".join(lines_output)


def print_somali_exception(
    exc: BaseException,
    filename: str = "<kood>",
    source_code: Optional[str] = None
) -> None:
    """Daabac khaladka Af-Soomaaliga."""
    formatted = format_somali_traceback(exc, filename, source_code)
    sys.stderr.write(formatted + "\n")
    sys.stderr.flush()
