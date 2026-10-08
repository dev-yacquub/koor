"""
Interpreter and Runtime Engine for Koor Programming Language.
Executes AST directly with environment scopes and native Somali built-ins.
Supports the 6 Core Foundations:
1. Variables & Data Types
2. Control Flow
3. Functions
4. Data Structures (Lists, Dictionaries, Text Sequences)
5. Operators & Expressions
6. Input and Output
"""

import math
import random
from typing import Dict, Any, List, Optional
from koor.ast_nodes import (
    ASTNode, Barnaamij, TiroExpr, QoraalExpr, RunBeenExpr, WaxbaExpr,
    MagacExpr, HawlgalLabaaleExpr, HawlgalKeliyaExpr, WacHawlExpr,
    LiisExpr, QaamuusExpr, TusmoHelExpr, XubinHelExpr,
    QorStmt, GeliStmt, BeddelStmt, XubinGeliStmt, TusmoGeliStmt,
    HaddiiStmt, IntaStmt, KuCeliStmt, KastaStmt, KaBaxStmt, KaBoodStmt,
    HawlQeexidStmt, CeliStmt, HadalKeliyaStmt
)
from koor.errors import (
    KhaladMagac, KhaladNooc, KhaladEberLooQaybiyay, KhaladSocod
)

# Control Flow Exceptions
class CeliException(Exception):
    def __init__(self, qiimo: Any):
        self.qiimo = qiimo


class KaBaxException(Exception):
    pass


class KaBoodException(Exception):
    pass


class KoorHawl:
    """Hawl la qeexay (Function) ee Koor."""
    def __init__(self, magac: str, barxado: List[str], jirka: List[ASTNode], deegaan: 'Deegaan'):
        self.magac = magac
        self.barxado = barxado
        self.jirka = jirka
        self.deegaan = deegaan

    def __repr__(self):
        return f"<hawl {self.magac}({', '.join(self.barxado)})>"


class Deegaan:
    """Maamulaha xusuusta iyo baaxadda doorsoomayaasha (Scope/Environment)."""
    def __init__(self, waalid: Optional['Deegaan'] = None):
        self.keyd: Dict[str, Any] = {}
        self.waalid = waalid

    def geli(self, magac: str, qiimo: Any):
        self.keyd[magac] = qiimo

    def beddel(self, magac: str, qiimo: Any, sadar: int = 1, tiir: int = 1, kood_sadar: str = ""):
        if magac in self.keyd:
            self.keyd[magac] = qiimo
            return
        if "_" in magac and magac.replace("_", " ") in self.keyd:
            self.keyd[magac.replace("_", " ")] = qiimo
            return
        if " " in magac and magac.replace(" ", "_") in self.keyd:
            self.keyd[magac.replace(" ", "_")] = qiimo
            return
        if self.waalid:
            self.waalid.beddel(magac, qiimo, sadar, tiir, kood_sadar)
            return
        raise KhaladMagac(
            f"Doorsoomaha '{magac}' lama hayo oo lama beddeli karo ka hor intaan la qeexin.",
            sadar=sadar,
            tiir=tiir,
            kood_sadar=kood_sadar,
            talo=self._talo_magac(magac)
        )

    def hel(self, magac: str, sadar: int = 1, tiir: int = 1, kood_sadar: str = "") -> Any:
        if magac in self.keyd:
            return self.keyd[magac]
        if "_" in magac and magac.replace("_", " ") in self.keyd:
            return self.keyd[magac.replace("_", " ")]
        if " " in magac and magac.replace(" ", "_") in self.keyd:
            return self.keyd[magac.replace(" ", "_")]
        if self.waalid:
            return self.waalid.hel(magac, sadar, tiir, kood_sadar)

        raise KhaladMagac(
            f"Magaca '{magac}' lama garanayo mana jiro doorsoome ama hawl sidaas la yiraahdo.",
            sadar=sadar,
            tiir=tiir,
            kood_sadar=kood_sadar,
            talo=self._talo_magac(magac)
        )

    def dhammaan_magacyada(self) -> List[str]:
        magacyo = list(self.keyd.keys())
        if self.waalid:
            magacyo.extend(self.waalid.dhammaan_magacyada())
        return list(set(magacyo))

    def _talo_magac(self, magac: str) -> Optional[str]:
        dhammaan = self.dhammaan_magacyada()
        if not dhammaan:
            return None
        import difflib
        isku_dhow = difflib.get_close_matches(magac, dhammaan, n=1, cutoff=0.6)
        if isku_dhow:
            return f"Miyaad u jeedday '{isku_dhow[0]}'?"
        return None


class Interpreter:
    def __init__(self, wax_soo_saar_qabte=None):
        self.deegaan_guud = Deegaan()
        self.wax_soo_saar = wax_soo_saar_qabte  # callback or None for print
        self._rakib_hawlaha_aasaasiga_ah()

    def _rakib_hawlaha_aasaasiga_ah(self):
        # Type inspection
        def nooc_magac(x):
            if isinstance(x, bool): return "run_been"
            if isinstance(x, (int, float)): return "tiro"
            if isinstance(x, str): return "qoraal"
            if isinstance(x, list): return "liis"
            if isinstance(x, dict): return "qaamuus"
            if isinstance(x, KoorHawl) or callable(x): return "hawl"
            if x is None: return "waxba"
            return type(x).__name__

        self.deegaan_guud.geli("nooc", nooc_magac)

        # Conversions
        self.deegaan_guud.geli("tiro", lambda x: int(x) if isinstance(x, (int, float, str)) and str(x).isdigit() else float(x))
        self.deegaan_guud.geli("qoraal", lambda x: self._u_rog_qoraal(x))
        self.deegaan_guud.geli("run_been", lambda x: self._waa_run(x))
        self.deegaan_guud.geli("liis", lambda x: list(x))
        self.deegaan_guud.geli("qaamuus", lambda x: dict(x))

        # Array & String methods
        self.deegaan_guud.geli("dherer", lambda x: len(x))
        self.deegaan_guud.geli("weyneey", lambda x: str(x).upper())
        self.deegaan_guud.geli("yaree", lambda x: str(x).lower())
        self.deegaan_guud.geli("jar", lambda x: str(x).strip())
        self.deegaan_guud.geli("kala_bax", lambda x, cal=" ": str(x).split(cal))
        self.deegaan_guud.geli("beddel_qoraal", lambda x, hore, dambe: str(x).replace(hore, dambe))
        self.deegaan_guud.geli("ku_dar_liiska", lambda l, item: l.append(item) or l)
        self.deegaan_guud.geli("ka_saar_liiska", lambda l, i=-1: l.pop(i))

        # IO & Math
        self.deegaan_guud.geli("waydiin", lambda f="": input(str(f)))
        self.deegaan_guud.geli("weydiin", lambda f="": input(str(f)))
        self.deegaan_guud.geli("weydii", lambda f="": input(str(f)))
        self.deegaan_guud.geli("xidid", lambda x: math.sqrt(x))
        self.deegaan_guud.geli("qaanso", lambda *args: list(range(*args)))
        self.deegaan_guud.geli("nasiib", lambda bilow=1, dhamaad=100: random.randint(int(bilow), int(dhamaad)))

    def _u_rog_qoraal(self, qiimo: Any) -> str:
        if qiimo is True:
            return "run"
        elif qiimo is False:
            return "been"
        elif qiimo is None:
            return "waxba"
        elif isinstance(qiimo, list):
            return "[" + ", ".join(self._u_rog_qoraal(item) for item in qiimo) + "]"
        elif isinstance(qiimo, dict):
            qaybo = [f'"{k}": {self._u_rog_qoraal(v)}' for k, v in qiimo.items()]
            return "{" + ", ".join(qaybo) + "}"
        return str(qiimo)

    def fuli(self, geed: Barnaamij, deegaan: Optional[Deegaan] = None):
        if deegaan is None:
            deegaan = self.deegaan_guud

        for hadal in geed.hadallo:
            self._fuli_hadal(hadal, deegaan)

    def _fuli_hadal(self, hadal: ASTNode, deegaan: Deegaan):
        if isinstance(hadal, QorStmt):
            qiimayaal = [self._qiimee(q, deegaan) for q in hadal.qoraallo]
            if len(qiimayaal) == 1 and qiimayaal[0] is None and len(hadal.qoraallo) == 1 and isinstance(hadal.qoraallo[0], WacHawlExpr):
                return
            qoraallo = [self._u_rog_qoraal(val) for val in qiimayaal]
            qoraal_buuxa = " ".join(qoraallo)
            if self.wax_soo_saar:
                self.wax_soo_saar(qoraal_buuxa)
            else:
                print(qoraal_buuxa)

        elif isinstance(hadal, GeliStmt):
            qiimo = self._qiimee(hadal.qiimo, deegaan)
            deegaan.geli(hadal.magac, qiimo)

        elif isinstance(hadal, XubinGeliStmt):
            shay = self._qiimee(hadal.shay, deegaan)
            qiimo = self._qiimee(hadal.qiimo, deegaan)
            if isinstance(shay, dict):
                shay[hadal.xubin] = qiimo
            else:
                raise KhaladNooc(f"Ma lagu dari karo sifo '{hadal.xubin}' noocan {type(shay).__name__}.", sadar=hadal.sadar, tiir=hadal.tiir)

        elif isinstance(hadal, TusmoGeliStmt):
            shay = self._qiimee(hadal.shay, deegaan)
            tusmo = self._qiimee(hadal.tusmo, deegaan)
            qiimo = self._qiimee(hadal.qiimo, deegaan)
            try:
                shay[tusmo] = qiimo
            except Exception as e:
                raise KhaladSocod(f"Lama gelin karo qiimaha tusmada {tusmo}: {e}", sadar=hadal.sadar, tiir=hadal.tiir)

        elif isinstance(hadal, BeddelStmt):
            kordhin = self._qiimee(hadal.qiimo, deegaan)
            if isinstance(hadal.magac, XubinHelExpr):
                shay = self._qiimee(hadal.magac.shay, deegaan)
                xubin = hadal.magac.xubin
                if isinstance(shay, dict):
                    hadda = shay[xubin]
                else:
                    hadda = getattr(shay, xubin)

                if hadal.hawlgal == "+": natiijo = hadda + kordhin
                elif hadal.hawlgal == "-": natiijo = hadda - kordhin
                elif hadal.hawlgal == "*": natiijo = hadda * kordhin
                elif hadal.hawlgal == "/":
                    if kordhin == 0: raise KhaladEberLooQaybiyay("Tiro laguma qaybin karo eber.", sadar=hadal.sadar, tiir=hadal.tiir)
                    natiijo = hadda / kordhin

                if isinstance(shay, dict): shay[xubin] = natiijo
                else: setattr(shay, xubin, natiijo)
            elif isinstance(hadal.magac, TusmoHelExpr):
                shay = self._qiimee(hadal.magac.liis_ama_qaamuus, deegaan)
                tusmo = self._qiimee(hadal.magac.tusmo, deegaan)
                try:
                    hadda = shay[tusmo]
                except Exception as e:
                    raise KhaladSocod(f"Lama heli karo tusmada '{tusmo}': {e}", sadar=hadal.sadar, tiir=hadal.tiir)

                if hadal.hawlgal == "+": natiijo = hadda + kordhin
                elif hadal.hawlgal == "-": natiijo = hadda - kordhin
                elif hadal.hawlgal == "*": natiijo = hadda * kordhin
                elif hadal.hawlgal == "/":
                    if kordhin == 0: raise KhaladEberLooQaybiyay("Tiro laguma qaybin karo eber.", sadar=hadal.sadar, tiir=hadal.tiir)
                    natiijo = hadda / kordhin

                shay[tusmo] = natiijo
            else:
                hadda = deegaan.hel(hadal.magac, sadar=hadal.sadar, tiir=hadal.tiir)
                if hadal.hawlgal == "+":
                    natiijo = hadda + kordhin
                elif hadal.hawlgal == "-":
                    natiijo = hadda - kordhin
                elif hadal.hawlgal == "*":
                    natiijo = hadda * kordhin
                elif hadal.hawlgal == "/":
                    if kordhin == 0:
                        raise KhaladEberLooQaybiyay("Tiro laguma qaybin karo eber.", sadar=hadal.sadar, tiir=hadal.tiir)
                    natiijo = hadda / kordhin
                deegaan.beddel(hadal.magac, natiijo, sadar=hadal.sadar, tiir=hadal.tiir)

        elif isinstance(hadal, HaddiiStmt):
            shardi_run = self._waa_run(self._qiimee(hadal.shardi, deegaan))
            if shardi_run:
                for h in hadal.haddii_run_tahay:
                    self._fuli_hadal(h, deegaan)
            else:
                fulay = False
                for elif_shardi, elif_jirka in hadal.haddii_kale:
                    if self._waa_run(self._qiimee(elif_shardi, deegaan)):
                        for h in elif_jirka:
                            self._fuli_hadal(h, deegaan)
                        fulay = True
                        break
                if not fulay and hadal.kale:
                    for h in hadal.kale:
                        self._fuli_hadal(h, deegaan)

        elif isinstance(hadal, IntaStmt):
            while self._waa_run(self._qiimee(hadal.shardi, deegaan)):
                try:
                    for h in hadal.jirka:
                        self._fuli_hadal(h, deegaan)
                except KaBoodException:
                    continue
                except KaBaxException:
                    break

        elif isinstance(hadal, KuCeliStmt):
            jeer_tirada = self._qiimee(hadal.jeer, deegaan)
            if not isinstance(jeer_tirada, int):
                raise KhaladNooc(f"Tirada 'ku celi' waa inay noqotaa tiro idil (integer).", sadar=hadal.sadar, tiir=hadal.tiir)
            for _ in range(jeer_tirada):
                try:
                    for h in hadal.jirka:
                        self._fuli_hadal(h, deegaan)
                except KaBoodException:
                    continue
                except KaBaxException:
                    break

        elif isinstance(hadal, KastaStmt):
            liis_qiimo = self._qiimee(hadal.liis_expr, deegaan)
            if not hasattr(liis_qiimo, '__iter__'):
                raise KhaladNooc(f"Wareegga 'kasta' wuxuu u baahan yahay liis ama xog la dhex mari karo.", sadar=hadal.sadar, tiir=hadal.tiir)
            for item in liis_qiimo:
                deegaan.geli(hadal.doorsoome, item)
                try:
                    for h in hadal.jirka:
                        self._fuli_hadal(h, deegaan)
                except KaBoodException:
                    continue
                except KaBaxException:
                    break

        elif isinstance(hadal, KaBaxStmt):
            raise KaBaxException()

        elif isinstance(hadal, KaBoodStmt):
            raise KaBoodException()

        elif isinstance(hadal, HawlQeexidStmt):
            hawl = KoorHawl(hadal.magac, hadal.barxado, hadal.jirka, deegaan)
            deegaan.geli(hadal.magac, hawl)
            if "_" in hadal.magac:
                deegaan.geli(hadal.magac.replace("_", " "), hawl)
            if " " in hadal.magac:
                deegaan.geli(hadal.magac.replace(" ", "_"), hawl)

        elif isinstance(hadal, CeliStmt):
            qiimo = self._qiimee(hadal.qiimo, deegaan) if hadal.qiimo else None
            raise CeliException(qiimo)

        elif isinstance(hadal, HadalKeliyaStmt):
            self._qiimee(hadal.muujin, deegaan)

    def _waa_run(self, qiimo: Any) -> bool:
        if qiimo is False or qiimo is None or qiimo == 0 or qiimo == "":
            return False
        return True

    def _qiimee(self, node: ASTNode, deegaan: Deegaan) -> Any:
        if isinstance(node, TiroExpr):
            return node.qiimo

        elif isinstance(node, QoraalExpr):
            qoraal = node.qiimo
            if "{" in qoraal and "}" in qoraal:
                import re
                def badal(match):
                    expr_text = match.group(1).strip()
                    try:
                        if "." in expr_text:
                            qaybo = expr_text.split(".")
                            curr = deegaan.hel(qaybo[0])
                            for q in qaybo[1:]:
                                if isinstance(curr, dict) and q in curr:
                                    curr = curr[q]
                                else:
                                    curr = getattr(curr, q)
                            return self._u_rog_qoraal(curr)
                        return self._u_rog_qoraal(deegaan.hel(expr_text))
                    except Exception:
                        return match.group(0)
                return re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_'.]*)\}", badal, qoraal)
            elif node.f_string:
                import re
                words = qoraal.split()
                SOMALI_STOP_WORDS = {
                    "waa", "iyo", "ama", "ah", "ku", "ka", "ee", "oo", "ma", "mid",
                    "waxaad", "soo", "celi", "saar", "daabac", "qor", "kaliya", "haddii",
                    "kale", "inta", "jeer"
                }
                natiijo_parts = []
                for w in words:
                    clean_w = re.sub(r"[^\w]", "", w)
                    if clean_w and clean_w not in SOMALI_STOP_WORDS:
                        try:
                            val = deegaan.hel(clean_w)
                            natiijo_parts.append(w.replace(clean_w, self._u_rog_qoraal(val)))
                            continue
                        except Exception:
                            pass
                    natiijo_parts.append(w)
                return " ".join(natiijo_parts)
            return qoraal

        elif isinstance(node, RunBeenExpr):
            return node.qiimo

        elif isinstance(node, WaxbaExpr):
            return None

        elif isinstance(node, MagacExpr):
            return deegaan.hel(node.magac, sadar=node.sadar, tiir=node.tiir)

        elif isinstance(node, LiisExpr):
            return [self._qiimee(w, deegaan) for w in node.walxo]

        elif isinstance(node, QaamuusExpr):
            natiijo = {}
            for fure_node, qiimo_node in node.fureyaal_iyo_qiimayaal:
                fure = self._qiimee(fure_node, deegaan)
                qiimo = self._qiimee(qiimo_node, deegaan)
                natiijo[fure] = qiimo
            return natiijo

        elif isinstance(node, TusmoHelExpr):
            shey = self._qiimee(node.liis_ama_qaamuus, deegaan)
            tus = self._qiimee(node.tusmo, deegaan)
            try:
                return shey[tus]
            except Exception as e:
                raise KhaladSocod(f"Lama heli karo tusmada '{tus}': {e}", sadar=node.sadar, tiir=node.tiir)

        elif isinstance(node, XubinHelExpr):
            shay = self._qiimee(node.shay, deegaan)
            xubin = node.xubin

            if isinstance(shay, dict):
                if xubin in shay:
                    return shay[xubin]
                if xubin == "fureyaal": return lambda: list(shay.keys())
                if xubin == "qiimayaal": return lambda: list(shay.values())
                if xubin == "walxo": return lambda: list(shay.items())
                if xubin == "dherer": return lambda: len(shay)
                raise KhaladMagac(f"Furaha '{xubin}' lagama helin qaamuuska.", sadar=node.sadar, tiir=node.tiir)
            elif isinstance(shay, list):
                if xubin == "ku_dar": return lambda item: shay.append(item) or shay
                if xubin == "ka_saar": return lambda i=-1: shay.pop(i)
                if xubin == "dherer": return lambda: len(shay)
                if xubin == "kala_sooc": return lambda: shay.sort() or shay
                if xubin == "rog": return lambda: shay.reverse() or shay
                raise KhaladMagac(f"Liisku ma laha hawl la yiraahdo '{xubin}'.", sadar=node.sadar, tiir=node.tiir)
            elif isinstance(shay, str):
                if xubin == "weyneey": return lambda: shay.upper()
                if xubin == "yaree": return lambda: shay.lower()
                if xubin == "jar": return lambda: shay.strip()
                if xubin == "kala_bax": return lambda cal=" ": shay.split(cal)
                if xubin == "beddel": return lambda old, new: shay.replace(old, new)
                if xubin == "dherer": return lambda: len(shay)
                raise KhaladMagac(f"Qoraalku ma laha hawl la yiraahdo '{xubin}'.", sadar=node.sadar, tiir=node.tiir)
            else:
                raise KhaladNooc(f"Xubinta '{xubin}' lagama heli karo noocan {type(shay).__name__}.", sadar=node.sadar, tiir=node.tiir)

        elif isinstance(node, HawlgalKeliyaExpr):
            shay = self._qiimee(node.shay, deegaan)
            if node.calaanad == "-":
                return -shay
            elif node.calaanad == "ma":
                return not self._waa_run(shay)

        elif isinstance(node, HawlgalLabaaleExpr):
            bidix = self._qiimee(node.bidix, deegaan)
            midig = self._qiimee(node.midig, deegaan)
            cal = node.calaanad

            if cal == "+":
                if isinstance(bidix, str) or isinstance(midig, str):
                    return self._u_rog_qoraal(bidix) + self._u_rog_qoraal(midig)
                return bidix + midig
            elif cal == "-": return bidix - midig
            elif cal == "*": return bidix * midig
            elif cal == "/":
                if midig == 0:
                    raise KhaladEberLooQaybiyay("Tiro laguma qaybin karo eber.", sadar=node.sadar, tiir=node.tiir)
                return bidix / midig
            elif cal == "%": return bidix % midig
            elif cal == "==": return bidix == midig
            elif cal == "!=": return bidix != midig
            elif cal == ">": return bidix > midig
            elif cal == "<": return bidix < midig
            elif cal == ">=": return bidix >= midig
            elif cal == "<=": return bidix <= midig
            elif cal in ("iyo", "sidoo kale", "and"): return self._waa_run(bidix) and self._waa_run(midig)
            elif cal == "ama": return self._waa_run(bidix) or self._waa_run(midig)

        elif isinstance(node, WacHawlExpr):
            if isinstance(node.magac, str):
                hawl = deegaan.hel(node.magac, sadar=node.sadar, tiir=node.tiir)
            else:
                hawl = self._qiimee(node.magac, deegaan)

            qiimayaal = [self._qiimee(d, deegaan) for d in node.doodo]

            if callable(hawl):
                try:
                    return hawl(*qiimayaal)
                except Exception as e:
                    raise KhaladSocod(f"Khalad ayaa ka dhashay hawsha: {e}", sadar=node.sadar, tiir=node.tiir)

            elif isinstance(hawl, KoorHawl):
                return self._wac_hawl_gudaha(hawl, qiimayaal, sadar=node.sadar, tiir=node.tiir)

            else:
                raise KhaladNooc(f"'{hawl}' ma aha hawl la wici karo.", sadar=node.sadar, tiir=node.tiir)

        return None

    def _wac_hawl_gudaha(self, hawl: KoorHawl, qiimayaal: List[Any], sadar: int = 1, tiir: int = 1) -> Any:
        barxado = list(hawl.barxado)
        deegaan_cusub = Deegaan(waalid=hawl.deegaan)

        if len(qiimayaal) != len(barxado):
            raise KhaladNooc(
                f"Hawsha '{hawl.magac}' waxay qaadataa {len(barxado)} doodood, laakiin waxaad bixisay {len(qiimayaal)}.",
                sadar=sadar,
                tiir=tiir
            )

        for b_magac, b_qiimo in zip(barxado, qiimayaal):
            deegaan_cusub.geli(b_magac, b_qiimo)

        try:
            for h in hawl.jirka:
                self._fuli_hadal(h, deegaan_cusub)
            return None
        except CeliException as c:
            return c.qiimo
