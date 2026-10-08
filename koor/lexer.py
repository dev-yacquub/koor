"""
Lexer for Koor Programming Language.
Supports natural Somali phrases, multi-word keywords, numbers, strings, and punctuation.
"""

import re
from dataclasses import dataclass
from typing import List, Optional
from koor.errors import KhaladNaxwo

# Token Types
class TokenType:
    # Single-word or multi-word keywords
    HADDII = "HADDII"                   # haddii, haddi
    HADDII_KALE = "HADDII_KALE"         # haddii kale, haddi kale
    KALE = "KALE"                       # kale
    INTA = "INTA"                       # inta
    KU_CELI = "KU_CELI"                 # ku celi
    JEER = "JEER"                       # jeer
    KASTA = "KASTA"                     # kasta
    KU_JIRA = "KU_JIRA"                 # ku jira, ku jirta, oo ku jira, oo ku jirta
    HAWL = "HAWL"                       # hawl, hawsha
    HAWSHU_WAA = "HAWSHU_WAA"           # hawshu waa, hawsha waa
    QABO_HAWSHAN = "QABO_HAWSHAN"       # qabo hawshan, qabo hawsha
    OO_QAADATA = "OO_QAADATA"           # oo qaadata
    CELI = "CELI"                       # celi, soo celi, waxaad soo celisaa
    DAABAC = "DAABAC"                   # daabac, soo saar, waxaad soo saartaa, waxaad daabacdaa, qor
    WAYDIIN = "WAYDIIN"                 # waydiin, waxaad waydiisaa
    WEYDII = "WAYDIIN"                  # alias
    WAA = "WAA"                         # waa
    QEEX = "QEEX"                       # qeex
    INUU_YAHAY = "INUU_YAHAY"           # inuu yahay, inay tahay
    
    # In-place operations (waxaad ku dartaa 1 x)
    KU_DAR = "KU_DAR"                   # ku dar, waxaad ku dartaa
    KA_JAR = "KA_JAR"                   # ka jar, waxaad ka jartaa
    KU_DHUFO = "KU_DHUFO"               # ku dhufo, waxaad ku dhufataa
    U_QAYBI = "U_QAYBI"                 # u qaybi, waxaad u qaybisaa
    
    # Natural comparisons
    LA_MID_YAHAY = "LA_MID_YAHAY"       # == (ay la mid tahay, uu la mid yahay, la mid tahay, la mid yahay)
    AAN_LA_MID_AHAYN = "AAN_LA_MID_AHAYN" # != (aysan la mid ahayn, uusan la mid ahayn, aan la mid ahayn)
    KA_WEYN = "KA_WEYN"                 # > (uu ka weyn yahay, ay ka weyn tahay, ka weyn yahay, ka weyn tahay)
    KA_YAR = "KA_YAR"                   # < (uu ka yar yahay, ay ka yar tahay, ka yar yahay, ka yar tahay)
    KA_WEYN_AMA_LA_MID = "KA_WEYN_AMA_LA_MID" # >= (ka weyn yahay ama la mid yahay, ka weyn tahay ama la mid tahay)
    KA_YAR_AMA_LA_MID = "KA_YAR_AMA_LA_MID"   # <= (ka yar yahay ama la mid yahay, ka yar tahay ama la mid tahay)

    # Boolean logic in Somali
    IYO = "IYO"                         # iyo, and
    AMA = "AMA"                         # ama, or
    MA_AHA = "MA_AHA"                   # ma aha, ma, not
    RUN = "RUN"                         # run (True)
    BEEN = "BEEN"                       # been (False)
    WAXBA = "WAXBA"                     # waxba (None)

    # Mathematical natural operators & zero-sign constructs
    HARAA = "HARAA"                     # haraaga, haraa (%)
    WAC = "WAC"                         # wac (explicit call)
    LIISKA = "LIISKA"                   # liiska (zero-sign list literal)
    QAAMUUSKA = "QAAMUUSKA"             # qaamuuska (zero-sign dict literal)
    MAGAC_WAA = "MAGAC_WAA"             # magaceed waa, magaca waa, magac waa
    TIBXUHU_WAA = "TIBXUHU_WAA"         # tibxuhu waa, tibxaha waa, tibxo waa
    KAYDI_NATIIJADA = "KAYDI_NATIIJADA" # kaydi natiijada, kaydi natiijo
    WAXAAD = "WAXAAD"                   # waxaad

    # Literals
    TIRO = "TIRO"                       # 12, 3.14
    QORAAL = "QORAAL"                   # "waad guulaysatay"
    MAGAC = "MAGAC"                     # x, magac, dhibco

    # Loop controls
    KA_BAX = "KA_BAX"                   # ka bax (break)
    KA_BOOD = "KA_BOOD"                 # ka bood (continue)

    # Operators and Punctuation
    PLUS = "PLUS"                       # +
    MINUS = "MINUS"                     # -
    STAR = "STAR"                       # *
    SLASH = "SLASH"                     # /
    PERCENT = "PERCENT"                 # %
    EQUAL = "EQUAL"                     # =
    DOT = "DOT"                         # . (Sentence terminator or dot access)
    COLON = "COLON"                     # :
    COMMA = "COMMA"                     # ,
    LPAREN = "LPAREN"                   # (
    RPAREN = "RPAREN"                   # )
    LBRACKET = "LBRACKET"               # [
    RBRACKET = "RBRACKET"               # ]
    LBRACE = "LBRACE"                   # {
    RBRACE = "RBRACE"                   # }

    # Whitespace & Control
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"


@dataclass
class Token:
    nooc: str
    qiimo: any
    sadar: int
    tiir: int
    kood_sadar: str = ""

    def __repr__(self):
        return f"Token({self.nooc}, {repr(self.qiimo)}, L{self.sadar}:C{self.tiir})"


# Multi-word phrases sorted from longest to shortest to ensure greedy matching
MULTIWORD_PHRASES = [
    # Comparisons (Longest first)
    (r"\b(uu|ay)?\s*ka\s+weyn\s+(yahay|tahay)\s+ama\s+la\s+mid\s+(yahay|tahay)\b", TokenType.KA_WEYN_AMA_LA_MID),
    (r"\b(uu|ay)?\s*ka\s+weyn\s+ama\s+la\s+mid\s*(ah|yahay|tahay)?\b", TokenType.KA_WEYN_AMA_LA_MID),
    (r"\b(uu|ay)?\s*ka\s+yar\s+(yahay|tahay)\s+ama\s+la\s+mid\s+(yahay|tahay)\b", TokenType.KA_YAR_AMA_LA_MID),
    (r"\b(uu|ay)?\s*ka\s+yar\s+ama\s+la\s+mid\s*(ah|yahay|tahay)?\b", TokenType.KA_YAR_AMA_LA_MID),
    (r"\b(uu|ay|wuxuu|waxay)?\s*aysan\s+la\s+mid\s+ahayn\b", TokenType.AAN_LA_MID_AHAYN),
    (r"\b(uu|ay|wuxuu|waxay)?\s*uusan\s+la\s+mid\s+ahayn\b", TokenType.AAN_LA_MID_AHAYN),
    (r"\b(uu|ay|wuxuu|waxay)?\s*aan\s+la\s+mid\s+ahayn\b", TokenType.AAN_LA_MID_AHAYN),
    (r"\b(uu|ay|wuxuu|waxay)?\s*la\s+mid\s+(yahay|tahay)\b", TokenType.LA_MID_YAHAY),
    (r"\b(uu|ay|wuxuu|waxay)?\s*la\s+mid\s+ah\b", TokenType.LA_MID_YAHAY),
    (r"\b(uu|ay)?\s*ka\s+weyn\s*(yahay|tahay)?\b", TokenType.KA_WEYN),
    (r"\b(uu|ay)?\s*ka\s+yar\s*(yahay|tahay)?\b", TokenType.KA_YAR),

    # Actions / Verbs (Waxaad ...)
    (r"\bwaxaad\s+soo\s+saartaa\b", TokenType.DAABAC),
    (r"\bwaxaad\s+daabacdaa\b", TokenType.DAABAC),
    (r"\bwaxaad\s+soo\s+celisaa\b", TokenType.CELI),
    (r"\bwaxaad\s+waydiisaa\b", TokenType.WAYDIIN),
    (r"\bwaxaad\s+weydiisaa\b", TokenType.WAYDIIN),
    # Loop controls
    (r"\bka\s+bax\b", TokenType.KA_BAX),
    (r"\bka\s+bood\b", TokenType.KA_BOOD),

    # Two-word phrases
    (r"\bsidoo\s+kale\b", TokenType.IYO),
    (r"\bmagac(eed|a)\s+waa\b", TokenType.MAGAC_WAA),
    (r"\btibx(uhu|aha|adu|ada|o)?\s+waa\b", TokenType.TIBXUHU_WAA),
    (r"\bhawsh(u|a)\s+waa\b", TokenType.HAWSHU_WAA),
    (r"\bkaydi\s+natiijad(a|ii)\b", TokenType.KAYDI_NATIIJADA),
    (r"\bkaydi\s+natiijo\b", TokenType.KAYDI_NATIIJADA),
    (r"\bqabo\s+hawsh(an|a)\b", TokenType.QABO_HAWSHAN),
    (r"\bsoo\s+saar\b", TokenType.DAABAC),
    (r"\bsoo\s+celi\b", TokenType.CELI),
    (r"\bku\s+celi\b", TokenType.KU_CELI),
    (r"\bku\s+dart(aa|a)\b", TokenType.KU_DAR),
    (r"\bka\s+jart(aa|a)\b", TokenType.KA_JAR),
    (r"\bku\s+dhufat(aa|a)\b", TokenType.KU_DHUFO),
    (r"\bu\s+qaybis(aa|a)\b", TokenType.U_QAYBI),
    (r"\bku\s+dar\b", TokenType.KU_DAR),
    (r"\bka\s+jar\b", TokenType.KA_JAR),
    (r"\bku\s+dhufo\b", TokenType.KU_DHUFO),
    (r"\bu\s+qaybi\b", TokenType.U_QAYBI),
    (r"\bharaag(a|ii)\b", TokenType.HARAA),
    (r"\bharaa\b", TokenType.HARAA),
    # Control flow else-if phrases (greedy matching)
    (r"\b(haddii|haddi|hadii)\s+kale\s+oo\s+(ay|uu)\b", TokenType.HADDII_KALE),
    (r"\b(haddii|haddi|hadii)\s+kale\b", TokenType.HADDII_KALE),
    (r"\bmid\s+kasta\s+oo\b", TokenType.KASTA),
    (r"\bmid\s+kast(oo|o)\b", TokenType.KASTA),
    (r"\bmid\s+kasta\b", TokenType.KASTA),
    (r"\boo\s+ku\s+jir(a|ta)\b", TokenType.KU_JIRA),
    (r"\bku\s+jir(a|ta)\b", TokenType.KU_JIRA),
    (r"\boo\s+qaadat(a|aa)\b", TokenType.OO_QAADATA),
    (r"\boo\s+qaadanays(a|aa)\b", TokenType.OO_QAADATA),
    (r"\boo\s+qaadanay(a|aa)\b", TokenType.OO_QAADATA),
    (r"\bin(uu|ay)\s+tahay\b", TokenType.INUU_YAHAY),
    (r"\bin(uu|ay)\s+yahay\b", TokenType.INUU_YAHAY),
    (r"\bma\s+aha\b", TokenType.MA_AHA),
]

SINGLE_KEYWORDS = {
    "haddii": TokenType.HADDII,
    "haddi": TokenType.HADDII,
    "hadii": TokenType.HADDII,
    "kale": TokenType.KALE,
    "inta": TokenType.INTA,
    "jeer": TokenType.JEER,
    "kasta": TokenType.KASTA,
    "mid_kastoo": TokenType.KASTA,
    "mid_kasto": TokenType.KASTA,
    "hawl": TokenType.HAWL,
    "hawsha": TokenType.HAWL,
    "celi": TokenType.CELI,
    "daabac": TokenType.DAABAC,
    "qor": TokenType.DAABAC,
    "waydiin": TokenType.WAYDIIN,
    "weydiin": TokenType.WAYDIIN,
    "waydii": TokenType.WAYDIIN,
    "weydii": TokenType.WAYDIIN,
    "waa": TokenType.WAA,
    "qeex": TokenType.QEEX,
    "run": TokenType.RUN,
    "been": TokenType.BEEN,
    "waxba": TokenType.WAXBA,
    "iyo": TokenType.IYO,
    "sidoo_kale": TokenType.IYO,
    "ama": TokenType.AMA,
    "ma": TokenType.MA_AHA,
    "ka_bax": TokenType.KA_BAX,
    "ka_bood": TokenType.KA_BOOD,
    "wac": TokenType.WAC,
    "waxaad": TokenType.WAXAAD,
    "haraa": TokenType.HARAA,
    "haraaga": TokenType.HARAA,
    "liiska": TokenType.LIISKA,
    "qaamuuska": TokenType.QAAMUUSKA,
}


class Lexer:
    def __init__(self, kood: str, fayl_magac: str = "<xadhig>"):
        self.kood = kood
        self.fayl_magac = fayl_magac
        self.dherer = len(kood)
        self.tilmaame = 0
        self.sadar = 1
        self.tiir = 1
        self.xariiqyada = kood.splitlines()

    def kood_sadarka(self, sadar_lambar: int) -> str:
        if 1 <= sadar_lambar <= len(self.xariiqyada):
            return self.xariiqyada[sadar_lambar - 1]
        return ""

    def fiiri(self, n: int = 0) -> str:
        idx = self.tilmaame + n
        if idx < self.dherer:
            return self.kood[idx]
        return ""

    def soco(self) -> str:
        xaraf = self.fiiri()
        self.tilmaame += 1
        if xaraf == '\n':
            self.sadar += 1
            self.tiir = 1
        else:
            self.tiir += 1
        return xaraf

    def tokens_saar(self) -> List[Token]:
        tokens: List[Token] = []
        indent_stack = [0]
        bracket_depth = 0

        while self.tilmaame < self.dherer:
            # Check for comments (# ...)
            if self.fiiri() == '#':
                while self.tilmaame < self.dherer and self.fiiri() != '\n':
                    self.soco()
                continue

            # Check for line-start indentation after newline (only at top-level outside brackets)
            if self.tiir == 1 and self.tilmaame < self.dherer and bracket_depth == 0:
                # Count leading spaces
                space_count = 0
                temp_idx = self.tilmaame
                while temp_idx < self.dherer and self.kood[temp_idx] in (' ', '\t'):
                    space_count += 4 if self.kood[temp_idx] == '\t' else 1
                    temp_idx += 1
                
                # If entire line is comment or empty, skip indentation processing
                if temp_idx < self.dherer and self.kood[temp_idx] not in ('\n', '#', '\r'):
                    current_indent = indent_stack[-1]
                    if space_count > current_indent:
                        indent_stack.append(space_count)
                        tokens.append(Token(TokenType.INDENT, space_count, self.sadar, 1, self.kood_sadarka(self.sadar)))
                    elif space_count < current_indent:
                        while indent_stack and space_count < indent_stack[-1]:
                            indent_stack.pop()
                            tokens.append(Token(TokenType.DEDENT, space_count, self.sadar, 1, self.kood_sadarka(self.sadar)))
                        if indent_stack and space_count != indent_stack[-1]:
                            raise KhaladNaxwo(
                                f"Balaarinta koodka (indentation) ma habboona.",
                                sadar=self.sadar,
                                tiir=1,
                                kood_sadar=self.kood_sadarka(self.sadar),
                                talo="Hubi in dhammaan meelaha bannaan ee bilowga sadarradu ay siman yihiin (4 boos)."
                            )

            # Whitespace (not newline)
            if self.fiiri() in (' ', '\t', '\r'):
                self.soco()
                continue

            # Newline
            if self.fiiri() == '\n':
                sadar_hadda = self.sadar
                tiir_hadda = self.tiir
                self.soco()
                # Don't emit consecutive newlines
                if tokens and tokens[-1].nooc != TokenType.NEWLINE and tokens[-1].nooc != TokenType.INDENT:
                    tokens.append(Token(TokenType.NEWLINE, "\n", sadar_hadda, tiir_hadda, self.kood_sadarka(sadar_hadda)))
                continue

            # Try multi-word phrases first
            matched_phrase = False
            haray = self.kood[self.tilmaame:]
            for qaab, token_type in MULTIWORD_PHRASES:
                match = re.match(qaab, haray, re.IGNORECASE)
                if match:
                    dhererka_qaybta = match.end()
                    qoraalka = haray[:dhererka_qaybta]
                    start_sadar = self.sadar
                    start_tiir = self.tiir
                    for _ in range(dhererka_qaybta):
                        self.soco()
                    tokens.append(Token(token_type, qoraalka, start_sadar, start_tiir, self.kood_sadarka(start_sadar)))
                    matched_phrase = True
                    break
            
            if matched_phrase:
                continue

            # Numbers
            if self.fiiri().isdigit():
                tokens.append(self._akhri_tiro())
                continue

            # Strings ("..." or '...')
            if self.fiiri() in ('"', "'"):
                tokens.append(self._akhri_qoraal())
                continue

            # Identifiers and single keywords
            if self.fiiri().isalpha() or self.fiiri() == '_':
                tokens.append(self._akhri_eray())
                continue

            # Symbols and Operators
            xaraf = self.fiiri()
            sadar_hadda = self.sadar
            tiir_hadda = self.tiir
            kood_line = self.kood_sadarka(sadar_hadda)

            # Two-character operators
            labo = self.fiiri(0) + self.fiiri(1)
            if labo == "==":
                self.soco(); self.soco()
                tokens.append(Token(TokenType.LA_MID_YAHAY, "==", sadar_hadda, tiir_hadda, kood_line))
                continue
            elif labo == "!=":
                self.soco(); self.soco()
                tokens.append(Token(TokenType.AAN_LA_MID_AHAYN, "!=", sadar_hadda, tiir_hadda, kood_line))
                continue
            elif labo == ">=":
                self.soco(); self.soco()
                tokens.append(Token(TokenType.KA_WEYN_AMA_LA_MID, ">=", sadar_hadda, tiir_hadda, kood_line))
                continue
            elif labo == "<=":
                self.soco(); self.soco()
                tokens.append(Token(TokenType.KA_YAR_AMA_LA_MID, "<=", sadar_hadda, tiir_hadda, kood_line))
                continue

            # Single-character tokens
            if xaraf == '+':
                self.soco()
                tokens.append(Token(TokenType.PLUS, '+', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '-':
                self.soco()
                tokens.append(Token(TokenType.MINUS, '-', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '*':
                self.soco()
                tokens.append(Token(TokenType.STAR, '*', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '/':
                self.soco()
                tokens.append(Token(TokenType.SLASH, '/', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '%':
                self.soco()
                tokens.append(Token(TokenType.PERCENT, '%', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '=':
                self.soco()
                tokens.append(Token(TokenType.EQUAL, '=', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '>':
                self.soco()
                tokens.append(Token(TokenType.KA_WEYN, '>', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '<':
                self.soco()
                tokens.append(Token(TokenType.KA_YAR, '<', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '.':
                self.soco()
                tokens.append(Token(TokenType.DOT, '.', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == ':':
                self.soco()
                tokens.append(Token(TokenType.COLON, ':', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == ',':
                self.soco()
                tokens.append(Token(TokenType.COMMA, ',', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '(':
                self.soco()
                bracket_depth += 1
                tokens.append(Token(TokenType.LPAREN, '(', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == ')':
                self.soco()
                if bracket_depth > 0: bracket_depth -= 1
                tokens.append(Token(TokenType.RPAREN, ')', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '[':
                self.soco()
                bracket_depth += 1
                tokens.append(Token(TokenType.LBRACKET, '[', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == ']':
                self.soco()
                if bracket_depth > 0: bracket_depth -= 1
                tokens.append(Token(TokenType.RBRACKET, ']', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '{':
                self.soco()
                bracket_depth += 1
                tokens.append(Token(TokenType.LBRACE, '{', sadar_hadda, tiir_hadda, kood_line))
            elif xaraf == '}':
                self.soco()
                if bracket_depth > 0: bracket_depth -= 1
                tokens.append(Token(TokenType.RBRACE, '}', sadar_hadda, tiir_hadda, kood_line))
            else:
                xaraf_khaldan = self.soco()
                raise KhaladNaxwo(
                    f"Xaraf ama calaamad aan la garaneyn: '{xaraf_khaldan}'",
                    sadar=sadar_hadda,
                    tiir=tiir_hadda,
                    kood_sadar=kood_line,
                    talo="Hubi inaadan qorin calaamad aan luuqaddu aqoonsaneyn."
                )

        # Clear remaining indents
        while len(indent_stack) > 1:
            indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, 0, self.sadar, self.tiir, ""))

        tokens.append(Token(TokenType.EOF, "", self.sadar, self.tiir, ""))
        return tokens

    def _akhri_tiro(self) -> Token:
        start_sadar = self.sadar
        start_tiir = self.tiir
        buug = []
        ma_jebisay = False

        while self.tilmaame < self.dherer and (self.fiiri().isdigit() or self.fiiri() == '.'):
            if self.fiiri() == '.':
                # Check if it's a decimal or sentence period (e.g. followed by non-digit or end)
                if ma_jebisay or not self.fiiri(1).isdigit():
                    break
                ma_jebisay = True
            buug.append(self.soco())

        qoraalka = "".join(buug)
        qiimo = float(qoraalka) if ma_jebisay else int(qoraalka)
        return Token(TokenType.TIRO, qiimo, start_sadar, start_tiir, self.kood_sadarka(start_sadar))

    def _akhri_qoraal(self) -> Token:
        start_sadar = self.sadar
        start_tiir = self.tiir
        xidhaha = self.soco()  # " or '
        buug = []

        while self.tilmaame < self.dherer and self.fiiri() != xidhaha:
            if self.fiiri() == '\n':
                raise KhaladNaxwo(
                    "Qoraalka (string) lama xirin ka hor dhammaadka sadarka.",
                    sadar=start_sadar,
                    tiir=start_tiir,
                    kood_sadar=self.kood_sadarka(start_sadar),
                    talo=f"Ku dar calaamadda {xidhaha} dhamaadka qoraalka."
                )
            if self.fiiri() == '\\':
                self.soco()
                baxsade = self.soco()
                if baxsade == 'n': buug.append('\n')
                elif baxsade == 't': buug.append('\t')
                elif baxsade == '\\': buug.append('\\')
                elif baxsade == xidhaha: buug.append(xidhaha)
                else: buug.append(baxsade)
            else:
                buug.append(self.soco())

        if self.tilmaame >= self.dherer and (not buug or self.kood[-1] != xidhaha):
            raise KhaladNaxwo(
                "Qoraalka (string) lama xirin.",
                sadar=start_sadar,
                tiir=start_tiir,
                kood_sadar=self.kood_sadarka(start_sadar),
                talo=f"Ku dar calaamadda {xidhaha} dhamaadka qoraalka."
            )

        self.soco()  # Consume closing quote
        qiimo = "".join(buug)
        return Token(TokenType.QORAAL, qiimo, start_sadar, start_tiir, self.kood_sadarka(start_sadar))

    def _akhri_eray(self) -> Token:
        start_sadar = self.sadar
        start_tiir = self.tiir
        buug = []

        while self.tilmaame < self.dherer and (self.fiiri().isalnum() or self.fiiri() in ('_', "'")):
            buug.append(self.soco())

        eray = "".join(buug)
        hoos = eray.lower()

        # Check if single keyword
        if hoos in SINGLE_KEYWORDS:
            nooc = SINGLE_KEYWORDS[hoos]
            return Token(nooc, eray, start_sadar, start_tiir, self.kood_sadarka(start_sadar))

        return Token(TokenType.MAGAC, eray, start_sadar, start_tiir, self.kood_sadarka(start_sadar))
