"""
Parser for Koor Programming Language.
Parses natural Somali sentences and structured blocks into an AST.
"""

from typing import List, Optional
from koor.lexer import Token, TokenType
from koor.ast_nodes import (
    ASTNode, Barnaamij, TiroExpr, QoraalExpr, RunBeenExpr, WaxbaExpr,
    MagacExpr, HawlgalLabaaleExpr, HawlgalKeliyaExpr, WacHawlExpr,
    LiisExpr, QaamuusExpr, TusmoHelExpr, XubinHelExpr,
    QorStmt, GeliStmt, BeddelStmt, XubinGeliStmt, TusmoGeliStmt,
    HaddiiStmt, IntaStmt, KuCeliStmt, KastaStmt, KaBaxStmt, KaBoodStmt,
    HawlQeexidStmt, CeliStmt, HadalKeliyaStmt
)
from koor.errors import KhaladNaxwo


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.tilmaame = 0
        self.hawlo_la_yaqaan = {
            "tiro", "qoraal", "waydiin", "weydiin", "waydii",
            "dherer", "xidid", "nooc", "qaanso", "nasiib",
            "weyneey", "yaree", "jar", "run_been"
        }
        for i, tok in enumerate(self.tokens):
            if tok.nooc == TokenType.HAWL and i + 1 < len(self.tokens) and self.tokens[i+1].nooc == TokenType.MAGAC:
                self.hawlo_la_yaqaan.add(self.tokens[i+1].qiimo)
            elif tok.nooc == TokenType.MAGAC_WAA:
                j = i + 1
                while j < len(self.tokens) and self.tokens[j].nooc == TokenType.COLON:
                    j += 1
                name_parts = []
                while j < len(self.tokens) and self.tokens[j].nooc not in (TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.COLON):
                    name_parts.append(str(self.tokens[j].qiimo))
                    j += 1
                if name_parts:
                    fn_name = "_".join(name_parts)
                    self.hawlo_la_yaqaan.add(fn_name)
                    self.hawlo_la_yaqaan.add(" ".join(name_parts))

        self.liis_dambe: Optional[str] = None
        for i, tok in enumerate(self.tokens):
            if tok.nooc in (TokenType.WAA, TokenType.EQUAL) and i > 0 and self.tokens[i-1].nooc == TokenType.MAGAC:
                if i + 1 < len(self.tokens) and self.tokens[i+1].nooc in (TokenType.LIISKA, TokenType.LBRACKET):
                    self.liis_dambe = self.tokens[i-1].qiimo

    def fiiri(self, n: int = 0) -> Token:
        idx = self.tilmaame + n
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def hubi(self, *noocyo: str) -> bool:
        return self.fiiri().nooc in noocyo

    def qaado(self, *noocyo: str) -> bool:
        if self.hubi(*noocyo):
            self.soco()
            return True
        return False

    def soco(self) -> Token:
        t = self.fiiri()
        if self.tilmaame < len(self.tokens) - 1:
            self.tilmaame += 1
        return t

    def qasab(self, nooc: str, fariin: str, talo: str = "") -> Token:
        if self.fiiri().nooc == nooc:
            return self.soco()
        t = self.fiiri()
        raise KhaladNaxwo(
            fariin,
            sadar=t.sadar,
            tiir=t.tiir,
            kood_sadar=t.kood_sadar,
            talo=talo
        )

    def parse(self) -> Barnaamij:
        hadallo: List[ASTNode] = []
        while self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.INDENT):
            self.soco()

        while not self.hubi(TokenType.EOF):
            stmt = self._hadal()
            if stmt:
                hadallo.append(stmt)
            while self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.DEDENT):
                self.soco()

        return Barnaamij(hadallo=hadallo)

    def _dhimo_meelaha_madhan(self):
        while self.hubi(TokenType.NEWLINE, TokenType.DOT):
            self.soco()

    # --- Statements ---

    def _hadal(self) -> Optional[ASTNode]:
        self._dhimo_meelaha_madhan()
        if self.hubi(TokenType.EOF):
            return None

        # 1. Conditionals: haddii / haddi
        if self.hubi(TokenType.HADDII):
            return self._haddii_hadal()

        # 2. Print / Output: waxaad soo saartaa / daabac
        if self.hubi(TokenType.DAABAC):
            return self._qor_hadal()

        # 3. Return: waxaad soo celisaa / celi / kaydi natiijada
        if self.hubi(TokenType.CELI, TokenType.KAYDI_NATIIJADA):
            return self._celi_hadal()

        # 4. Break / Continue
        if self.hubi(TokenType.KA_BAX):
            t = self.soco()
            self.qaado(TokenType.DOT)
            self.qaado(TokenType.NEWLINE)
            return KaBaxStmt(sadar=t.sadar, tiir=t.tiir)
        if self.hubi(TokenType.KA_BOOD):
            t = self.soco()
            self.qaado(TokenType.DOT)
            self.qaado(TokenType.NEWLINE)
            return KaBoodStmt(sadar=t.sadar, tiir=t.tiir)

        # 5. In-place modification starting with 'waxaad':
        #    waxaad 1 ku dartaa tirsade / waxaad ku dartaa 1 tirsade
        if self.hubi(TokenType.WAXAAD):
            t_wax = self.soco()  # consume 'waxaad'
            if self.hubi(TokenType.KU_DAR, TokenType.KA_JAR, TokenType.KU_DHUFO, TokenType.U_QAYBI):
                op_tok = self.soco()
                hawlgal = "+"
                if op_tok.nooc == TokenType.KA_JAR: hawlgal = "-"
                elif op_tok.nooc == TokenType.KU_DHUFO: hawlgal = "*"
                elif op_tok.nooc == TokenType.U_QAYBI: hawlgal = "/"

                arg1 = self._muujin()
                arg2 = self._muujin()
                self.qaado(TokenType.DOT)
                self.qaado(TokenType.NEWLINE)

                if isinstance(arg1, MagacExpr) and not isinstance(arg2, MagacExpr):
                    target = arg1.magac
                    qiimo = arg2
                elif isinstance(arg2, MagacExpr):
                    target = arg2.magac
                    qiimo = arg1
                elif isinstance(arg2, (XubinHelExpr, TusmoHelExpr)):
                    target = arg2
                    qiimo = arg1
                elif isinstance(arg1, (XubinHelExpr, TusmoHelExpr)):
                    target = arg1
                    qiimo = arg2
                else:
                    target = arg2
                    qiimo = arg1

                return BeddelStmt(magac=target, hawlgal=hawlgal, qiimo=qiimo, sadar=t_wax.sadar, tiir=t_wax.tiir)
            else:
                # waxaad <qiimo> ku dartaa <target>
                qiimo = self._muujin()
                if not self.hubi(TokenType.KU_DAR, TokenType.KA_JAR, TokenType.KU_DHUFO, TokenType.U_QAYBI):
                    raise KhaladNaxwo(
                        "Waxaad iyo qiimaha ka dib waxaad u baahan tahay hawlgal sida 'ku dartaa', 'ka jartaa', 'ku dhufataa', ama 'u qaybisaa'.",
                        sadar=t_wax.sadar, tiir=t_wax.tiir,
                        kood_sadar=t_wax.kood_sadar,
                        talo="Tusaale: waxaad 1 ku dartaa tirsade"
                    )
                op_tok = self.soco()
                hawlgal = "+"
                if op_tok.nooc == TokenType.KA_JAR: hawlgal = "-"
                elif op_tok.nooc == TokenType.KU_DHUFO: hawlgal = "*"
                elif op_tok.nooc == TokenType.U_QAYBI: hawlgal = "/"

                target_expr = self._muujin()
                self.qaado(TokenType.DOT)
                self.qaado(TokenType.NEWLINE)

                if isinstance(target_expr, MagacExpr):
                    target = target_expr.magac
                elif isinstance(target_expr, (XubinHelExpr, TusmoHelExpr)):
                    target = target_expr
                else:
                    raise KhaladNaxwo("Waa inaad sheegtaa magaca doorsoomaha wax lagu kordhinayo/laga jarayo.", sadar=t_wax.sadar, tiir=t_wax.tiir)

                return BeddelStmt(magac=target, hawlgal=hawlgal, qiimo=qiimo, sadar=t_wax.sadar, tiir=t_wax.tiir)

        # 5b. In-place modification without 'waxaad': ku dar / ka jar
        if self.hubi(TokenType.KU_DAR, TokenType.KA_JAR, TokenType.KU_DHUFO, TokenType.U_QAYBI):
            return self._beddel_hadal()

        # 6. Variable declaration: qeex x inuu yahay ...
        if self.hubi(TokenType.QEEX):
            return self._qeex_hadal()

        # 7. Loops: inta, ku celi, kasta
        if self.hubi(TokenType.INTA):
            return self._inta_hadal()
        if self.hubi(TokenType.KU_CELI):
            return self._ku_celi_hadal()
        if self.hubi(TokenType.KASTA):
            return self._kasta_hadal()

        # 8. Function definition: hawl / hawsha / magaceed waa
        if self.hubi(TokenType.HAWL):
            return self._hawl_hadal()
        if self.hubi(TokenType.MAGAC_WAA):
            return self._qaab_dhismeed_hawl(self.fiiri())

        # 9. Natural function definition: hawshu waa ("iskudhufasho") \n (x * y)
        if self.hubi(TokenType.HAWSHU_WAA):
            return self._hawshu_waa_hadal()

        # 10. Natural function call statement: qabo hawshan ("iskudhufasho") (12, 3)
        if self.hubi(TokenType.QABO_HAWSHAN):
            call_expr = self._qabo_hawshan_expr()
            self.qaado(TokenType.DOT)
            self.qaado(TokenType.NEWLINE)
            return QorStmt(qoraallo=[call_expr], sadar=call_expr.sadar, tiir=call_expr.tiir)

        # 11. Assignments, In-place mutation, or Expression statement
        expr = self._muujin()

        # In-place mutation: da' waxaad ku dartaa 5 / da' ku dartaa 5
        if self.qaado(TokenType.WAXAAD) or (isinstance(expr, (MagacExpr, XubinHelExpr, TusmoHelExpr)) and self.hubi(TokenType.KU_DAR, TokenType.KA_JAR, TokenType.KU_DHUFO, TokenType.U_QAYBI)):
            if not self.hubi(TokenType.KU_DAR, TokenType.KA_JAR, TokenType.KU_DHUFO, TokenType.U_QAYBI):
                raise KhaladNaxwo(
                    "Waxaad ka dib waxaad u baahan tahay hawlgal sida 'ku dartaa', 'ka jartaa', 'ku dhufataa', ama 'u qaybisaa'.",
                    sadar=expr.sadar, tiir=expr.tiir
                )
            op_tok = self.soco()
            hawlgal = "+"
            if op_tok.nooc == TokenType.KA_JAR: hawlgal = "-"
            elif op_tok.nooc == TokenType.KU_DHUFO: hawlgal = "*"
            elif op_tok.nooc == TokenType.U_QAYBI: hawlgal = "/"

            qiimo = self._muujin()
            self.qaado(TokenType.DOT)
            self.qaado(TokenType.NEWLINE)

            if isinstance(expr, MagacExpr):
                target = expr.magac
            elif isinstance(expr, (XubinHelExpr, TusmoHelExpr)):
                target = expr
            else:
                raise KhaladNaxwo("Waa inaad sheegtaa magaca doorsoomaha wax lagu kordhinayo/laga jarayo.", sadar=expr.sadar, tiir=expr.tiir)

            return BeddelStmt(magac=target, hawlgal=hawlgal, qiimo=qiimo, sadar=expr.sadar, tiir=expr.tiir)

        if self.hubi(TokenType.EQUAL, TokenType.WAA):
            self.soco()  # consume '=' or 'waa'
            qiimo = self._muujin()
            self.qaado(TokenType.DOT)
            self.qaado(TokenType.NEWLINE)
            if isinstance(expr, MagacExpr):
                if isinstance(qiimo, (LiisExpr, QaamuusExpr)) or (isinstance(qiimo, WacHawlExpr) and qiimo.magac == "qaanso") or "arday" in expr.magac or "liis" in expr.magac:
                    self.liis_dambe = expr.magac
                return GeliStmt(magac=expr.magac, qiimo=qiimo, sadar=expr.sadar, tiir=expr.tiir)
            elif isinstance(expr, XubinHelExpr):
                return XubinGeliStmt(shay=expr.shay, xubin=expr.xubin, qiimo=qiimo, sadar=expr.sadar, tiir=expr.tiir)
            elif isinstance(expr, TusmoHelExpr):
                return TusmoGeliStmt(shay=expr.liis_ama_qaamuus, tusmo=expr.tusmo, qiimo=qiimo, sadar=expr.sadar, tiir=expr.tiir)
            else:
                raise KhaladNaxwo("Qiimaha laguma shubi karo meeshan.", sadar=expr.sadar, tiir=expr.tiir)

        self.qaado(TokenType.DOT)
        self.qaado(TokenType.NEWLINE)
        return HadalKeliyaStmt(muujin=expr, sadar=expr.sadar, tiir=expr.tiir)

    def _qor_hadal(self) -> QorStmt:
        t_daabac = self.soco()
        qoraallo = []

        if self.hubi(TokenType.DOT, TokenType.NEWLINE, TokenType.EOF):
            return QorStmt(qoraallo=[QoraalExpr("", f_string=False, sadar=t_daabac.sadar, tiir=t_daabac.tiir)], sadar=t_daabac.sadar, tiir=t_daabac.tiir)

        saved_idx = self.tilmaame
        is_unquoted_text = False

        try:
            first_expr = self._muujin()
            if self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.COMMA, TokenType.DEDENT):
                qoraallo.append(first_expr)
                while self.qaado(TokenType.COMMA):
                    qoraallo.append(self._muujin())
            else:
                is_unquoted_text = True
        except Exception:
            is_unquoted_text = True

        if is_unquoted_text:
            self.tilmaame = saved_idx
            line_tokens = []
            cur_line = t_daabac.sadar
            while not self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.EOF) and self.fiiri().sadar == cur_line:
                line_tokens.append(self.soco())

            kood_sadar = t_daabac.kood_sadar
            if line_tokens and kood_sadar:
                start_char = line_tokens[0].tiir - 1
                end_char = line_tokens[-1].tiir - 1 + len(str(line_tokens[-1].qiimo))
                raw_text = kood_sadar[start_char:end_char].strip().rstrip(".")
            else:
                raw_text = " ".join(str(tk.qiimo) for tk in line_tokens).rstrip(".")

            qoraallo = [QoraalExpr(qiimo=raw_text, f_string=True, sadar=t_daabac.sadar, tiir=t_daabac.tiir)]

        # Optional sentence terminator
        self.qaado(TokenType.DOT)
        self.qaado(TokenType.NEWLINE)
        return QorStmt(qoraallo=qoraallo, sadar=t_daabac.sadar, tiir=t_daabac.tiir)

    def _celi_hadal(self) -> CeliStmt:
        t_celi = self.soco()
        qiimo = None
        if not self.hubi(TokenType.DOT, TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT):
            qiimo = self._muujin()
        self.qaado(TokenType.DOT)
        self.qaado(TokenType.NEWLINE)
        return CeliStmt(qiimo=qiimo, sadar=t_celi.sadar, tiir=t_celi.tiir)

    def _qeex_hadal(self) -> GeliStmt:
        t_qeex = self.soco()
        magac_tok = self.qasab(TokenType.MAGAC, "Waxaad ilowday magaca doorsoomaha la qeexayo.", "Tusaale: qeex x inuu yahay 10.")
        self.qasab(TokenType.INUU_YAHAY, f"Qeexitaanka ka dib waxaad u baahan tahay 'inuu yahay' ama 'inay tahay'.", "Tusaale: qeex x inuu yahay 12.")
        qiimo = self._muujin()
        self.qaado(TokenType.DOT)
        self.qaado(TokenType.NEWLINE)
        return GeliStmt(magac=magac_tok.qiimo, qiimo=qiimo, sadar=t_qeex.sadar, tiir=t_qeex.tiir)

    def _geli_hadal(self) -> GeliStmt:
        magac_tok = self.soco()
        self.soco()  # Consume '=' or 'waa'
        qiimo = self._muujin()
        self.qaado(TokenType.DOT)
        self.qaado(TokenType.NEWLINE)
        return GeliStmt(magac=magac_tok.qiimo, qiimo=qiimo, sadar=magac_tok.sadar, tiir=magac_tok.tiir)

    def _beddel_hadal(self) -> BeddelStmt:
        # ku dar 1 x / ku dar x 1
        t_op = self.soco()
        hawlgal = "+"
        if t_op.nooc == TokenType.KA_JAR: hawlgal = "-"
        elif t_op.nooc == TokenType.KU_DHUFO: hawlgal = "*"
        elif t_op.nooc == TokenType.U_QAYBI: hawlgal = "/"

        arg1 = self._muujin()
        arg2 = self._muujin()
        self.qaado(TokenType.DOT)
        self.qaado(TokenType.NEWLINE)

        if isinstance(arg1, MagacExpr) and not isinstance(arg2, MagacExpr):
            target = arg1.magac
            qiimo = arg2
        elif isinstance(arg2, MagacExpr):
            target = arg2.magac
            qiimo = arg1
        elif isinstance(arg2, (XubinHelExpr, TusmoHelExpr)):
            target = arg2
            qiimo = arg1
        elif isinstance(arg1, (XubinHelExpr, TusmoHelExpr)):
            target = arg1
            qiimo = arg2
        else:
            target = arg2
            qiimo = arg1

        return BeddelStmt(magac=target, hawlgal=hawlgal, qiimo=qiimo, sadar=t_op.sadar, tiir=t_op.tiir)

    def _haddii_hadal(self) -> HaddiiStmt:
        t_haddii = self.soco()
        shardi = self._shardi_muujin()

        haddii_run_tahay = []
        haddii_kale = []
        kale = None

        # Check if single natural sentence (like: haddi x ay la mid tahay 12 waxaad soo saartaa "guul".)
        if not self.hubi(TokenType.COLON, TokenType.NEWLINE):
            # Inline single statement!
            stmt = self._hadal()
            if stmt:
                haddii_run_tahay.append(stmt)
            return HaddiiStmt(
                shardi=shardi,
                haddii_run_tahay=haddii_run_tahay,
                haddii_kale=[],
                kale=None,
                sadar=t_haddii.sadar,
                tiir=t_haddii.tiir
            )

        # Block style
        self.qaado(TokenType.COLON)
        haddii_run_tahay = self._hadallo_xirmo()

        # Check for haddii_kale / haddi kale / hadii kale oo ay / hadii kale oo uu
        while self.hubi(TokenType.HADDII_KALE):
            if self.fiiri(1).nooc == TokenType.COLON:
                # Direct else branch (e.g. 'haddii kale:' with no condition)
                self.soco()
                self.qaado(TokenType.COLON)
                kale = self._hadallo_xirmo()
                break
            self.soco()
            elif_shardi = self._shardi_muujin()
            self.qaado(TokenType.COLON)
            elif_jirka = self._hadallo_xirmo()
            haddii_kale.append((elif_shardi, elif_jirka))

        # Check for kale
        if kale is None and self.hubi(TokenType.KALE):
            self.soco()
            self.qaado(TokenType.COLON)
            kale = self._hadallo_xirmo()

        return HaddiiStmt(
            shardi=shardi,
            haddii_run_tahay=haddii_run_tahay,
            haddii_kale=haddii_kale,
            kale=kale,
            sadar=t_haddii.sadar,
            tiir=t_haddii.tiir
        )

    def _inta_hadal(self) -> IntaStmt:
        t_inta = self.soco()
        shardi = self._shardi_muujin()
        self.qaado(TokenType.COLON)
        jirka = self._hadallo_xirmo()
        return IntaStmt(shardi=shardi, jirka=jirka, sadar=t_inta.sadar, tiir=t_inta.tiir)

    def _ku_celi_hadal(self) -> KuCeliStmt:
        t_celi = self.soco()
        jeer = self._muujin()
        self.qaado(TokenType.JEER)
        self.qaado(TokenType.COLON)
        jirka = self._hadallo_xirmo()
        return KuCeliStmt(jeer=jeer, jirka=jirka, sadar=t_celi.sadar, tiir=t_celi.tiir)

    def _kasta_hadal(self) -> KastaStmt:
        t_kasta = self.soco()

        # Check if old-style: kasta <var> ku jira <collection>:
        if self.hubi(TokenType.MAGAC) and self.fiiri(1).nooc == TokenType.KU_JIRA:
            doorsoome = self.soco().qiimo
            self.qaado(TokenType.KU_JIRA)
            liis_expr = self._muujin()
            self.qaado(TokenType.COLON)
            jirka = self._hadallo_xirmo()
            return KastaStmt(doorsoome=doorsoome, liis_expr=liis_expr, jirka=jirka, sadar=t_kasta.sadar, tiir=t_kasta.tiir)

        # New natural style: mid kastoo ku jira magaalooyinka ( mag ): or zero-signs: mid kastoo ku jira magaalooyinka mag
        self.qaado(TokenType.KU_JIRA)

        end_idx = -1
        idx = self.tilmaame
        while idx < len(self.tokens):
            if self.tokens[idx].nooc == TokenType.COLON:
                end_idx = idx
                break
            if self.tokens[idx].nooc in (TokenType.NEWLINE, TokenType.EOF):
                end_idx = idx
                break
            idx += 1

        if end_idx == -1:
            end_idx = idx

        # Loop variable at the end: ( mag ) or bare mag
        if (end_idx - self.tilmaame >= 3 and 
            self.tokens[end_idx - 3].nooc == TokenType.LPAREN and 
            self.tokens[end_idx - 2].nooc == TokenType.MAGAC and 
            self.tokens[end_idx - 1].nooc == TokenType.RPAREN):
            doorsoome = self.tokens[end_idx - 2].qiimo
            expr_tokens = self.tokens[self.tilmaame : end_idx - 3]
        elif (end_idx - self.tilmaame >= 1 and 
              self.tokens[end_idx - 1].nooc == TokenType.MAGAC):
            if end_idx - self.tilmaame == 1 and self.liis_dambe:
                doorsoome = self.tokens[end_idx - 1].qiimo
                expr_tokens = []
            else:
                doorsoome = self.tokens[end_idx - 1].qiimo
                expr_tokens = self.tokens[self.tilmaame : end_idx - 1]
        else:
            raise KhaladNaxwo(
                "Waa inaad doorsoomaha wareegga gelisaa dhamaadka, tusaale: mid kastoo ku jira ardayda (qof)",
                sadar=t_kasta.sadar,
                tiir=t_kasta.tiir,
                talo="Tusaale sax ah: mid kastoo ku jira ardayda (qof) ama mid kastoo ku jira (qof)"
            )

        if not expr_tokens:
            if self.liis_dambe:
                liis_expr = MagacExpr(magac=self.liis_dambe, sadar=t_kasta.sadar, tiir=t_kasta.tiir)
            else:
                raise KhaladNaxwo(
                    "Waa inaad sheegtaa liiska ama taxanaha lagu dul wareegayo.",
                    sadar=t_kasta.sadar,
                    tiir=t_kasta.tiir
                )
        else:
            sub_parser = Parser(expr_tokens + [Token(TokenType.EOF, "", t_kasta.sadar, t_kasta.tiir)])
            liis_expr = sub_parser._muujin()
            if isinstance(liis_expr, MagacExpr):
                self.liis_dambe = liis_expr.magac

        self.tilmaame = end_idx
        self.qaado(TokenType.COLON)
        jirka = self._hadallo_xirmo()
        return KastaStmt(doorsoome=doorsoome, liis_expr=liis_expr, jirka=jirka, sadar=t_kasta.sadar, tiir=t_kasta.tiir)

    def _hawl_hadal(self) -> HawlQeexidStmt:
        t_hawl = self.soco()
        self.qaado(TokenType.COLON)

        # Check if structured declarative function follows:
        # hawl
        # magaceed waa : isku dhufasho
        # tibxuhu waa : x , y
        # hawshu waa : x ku dhufo y
        # kaydi natiijada
        if self.hubi(TokenType.NEWLINE, TokenType.INDENT, TokenType.DOT):
            self._dhimo_meelaha_madhan()
            if self.hubi(TokenType.MAGAC_WAA, TokenType.TIBXUHU_WAA, TokenType.HAWSHU_WAA) or (
                self.hubi(TokenType.INDENT) and self.fiiri(1).nooc in (TokenType.MAGAC_WAA, TokenType.TIBXUHU_WAA, TokenType.HAWSHU_WAA)
            ):
                return self._qaab_dhismeed_hawl(t_hawl)
        elif self.hubi(TokenType.MAGAC_WAA, TokenType.TIBXUHU_WAA, TokenType.HAWSHU_WAA):
            return self._qaab_dhismeed_hawl(t_hawl)

        magac_tok = self.qasab(TokenType.MAGAC, "Waa inaad magac u bixisaa hawsha.", "Tusaale: hawl salaan(qof):")
        self.hawlo_la_yaqaan.add(magac_tok.qiimo)
        barxado = []

        if self.qaado(TokenType.LPAREN):
            if not self.hubi(TokenType.RPAREN):
                if self.hubi(TokenType.MAGAC):
                    barxado.append(self.soco().qiimo)
                else:
                    raise KhaladNaxwo("Magaca barxadda (parameter) waa khaldan yahay.", sadar=self.fiiri().sadar, tiir=self.fiiri().tiir)
                while self.qaado(TokenType.COMMA):
                    if self.hubi(TokenType.MAGAC):
                        barxado.append(self.soco().qiimo)
                    else:
                        raise KhaladNaxwo("Magaca barxadda (parameter) waa khaldan yahay.", sadar=self.fiiri().sadar, tiir=self.fiiri().tiir)
            self.qasab(TokenType.RPAREN, "Waxaad ilowday ')' dhamaadka barxadaha.")
        else:
            # Zero-signs parameter parsing:
            # e.g.: hawl kala_goo oo qaadata x iyo y
            #       hawl kala_goo x y
            #       hawl kala_goo x iyo y
            self.qaado(TokenType.OO_QAADATA)
            while not self.hubi(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF, TokenType.DOT):
                if self.hubi(TokenType.MAGAC):
                    barxado.append(self.soco().qiimo)
                    self.qaado(TokenType.COMMA, TokenType.IYO)
                else:
                    break

        self.qaado(TokenType.COLON)
        jirka = self._hadallo_xirmo()
        return HawlQeexidStmt(magac=magac_tok.qiimo, barxado=barxado, jirka=jirka, sadar=t_hawl.sadar, tiir=t_hawl.tiir)

    def _qaab_dhismeed_hawl(self, t_hawl: Token) -> HawlQeexidStmt:
        magac = ""
        barxado = []
        body_expr = None
        body_stmts = []
        kaydi = False

        has_indent = self.qaado(TokenType.INDENT)
        self._dhimo_meelaha_madhan()

        while not self.hubi(TokenType.EOF):
            if self.hubi(TokenType.DEDENT):
                self.soco()
                break

            self._dhimo_meelaha_madhan()

            if self.hubi(TokenType.MAGAC_WAA):
                self.soco()
                self.qaado(TokenType.COLON)
                name_parts = []
                cur_line = self.fiiri().sadar
                while not self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.COLON) and self.fiiri().sadar == cur_line:
                    name_parts.append(str(self.soco().qiimo))
                if name_parts:
                    magac = "_".join(name_parts)
                    self.hawlo_la_yaqaan.add(magac)
                    self.hawlo_la_yaqaan.add(" ".join(name_parts))
                self.qaado(TokenType.DOT)
                self.qaado(TokenType.NEWLINE)
                self._dhimo_meelaha_madhan()
                continue

            elif self.hubi(TokenType.TIBXUHU_WAA):
                self.soco()
                self.qaado(TokenType.COLON)
                cur_line = self.fiiri().sadar
                while not self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.COLON) and self.fiiri().sadar == cur_line:
                    if self.hubi(TokenType.MAGAC) and self.fiiri().qiimo not in ("waxba",):
                        barxado.append(self.soco().qiimo)
                        self.qaado(TokenType.COMMA, TokenType.IYO)
                    elif self.hubi(TokenType.WAXBA):
                        self.soco()
                    else:
                        self.soco()
                self.qaado(TokenType.DOT)
                self.qaado(TokenType.NEWLINE)
                self._dhimo_meelaha_madhan()
                continue

            elif self.hubi(TokenType.HAWSHU_WAA):
                self.soco()
                self.qaado(TokenType.COLON)
                if self.hubi(TokenType.NEWLINE):
                    self.soco()
                    body_stmts = self._hadallo_xirmo()
                else:
                    if self.hubi(TokenType.DAABAC, TokenType.CELI):
                        body_stmts = [self._hadal()]
                    else:
                        body_expr = self._muujin()
                        self.qaado(TokenType.DOT)
                        self.qaado(TokenType.NEWLINE)
                self._dhimo_meelaha_madhan()
                continue

            elif self.hubi(TokenType.KAYDI_NATIIJADA):
                self.soco()
                kaydi = True
                self.qaado(TokenType.DOT)
                self.qaado(TokenType.NEWLINE)
                self._dhimo_meelaha_madhan()
                break

            else:
                break

        if not magac:
            raise KhaladNaxwo(
                "Hawsha cusub waa inay leedahay magac. Tusaale: magaceed waa : isku_dhufasho",
                sadar=t_hawl.sadar,
                tiir=t_hawl.tiir
            )

        if kaydi:
            if body_expr is not None:
                jirka = [CeliStmt(qiimo=body_expr, sadar=body_expr.sadar, tiir=body_expr.tiir)]
            elif body_stmts:
                if isinstance(body_stmts[-1], HadalKeliyaStmt):
                    body_stmts[-1] = CeliStmt(qiimo=body_stmts[-1].muujin, sadar=body_stmts[-1].sadar, tiir=body_stmts[-1].tiir)
                jirka = body_stmts
            else:
                jirka = []
        else:
            if body_expr is not None:
                jirka = [HadalKeliyaStmt(muujin=body_expr, sadar=body_expr.sadar, tiir=body_expr.tiir)]
            else:
                jirka = body_stmts

        return HawlQeexidStmt(magac=magac, barxado=barxado, jirka=jirka, sadar=t_hawl.sadar, tiir=t_hawl.tiir)

    def _hawshu_waa_hadal(self) -> HawlQeexidStmt:
        t = self.soco()  # consume HAWSHU_WAA
        magac = ""
        if self.qaado(TokenType.LPAREN):
            m_tok = self._muujin()
            self.qasab(TokenType.RPAREN, "Waxaad ilowday ')' magaca hawsha ka dib.")
            if isinstance(m_tok, QoraalExpr):
                magac = m_tok.qiimo.strip()
            elif isinstance(m_tok, MagacExpr):
                magac = m_tok.magac
        elif self.hubi(TokenType.QORAAL):
            magac = self.soco().qiimo.strip()
        elif self.hubi(TokenType.MAGAC):
            magac = self.soco().qiimo
        else:
            raise KhaladNaxwo("Sheeg magaca hawsha.", sadar=t.sadar, tiir=t.tiir)

        self._dhimo_meelaha_madhan()

        if self.qaado(TokenType.COLON):
            jirka = self._hadallo_xirmo()
            barxado = []
        else:
            expr = self._muujin()
            self.qaado(TokenType.DOT)
            self.qaado(TokenType.NEWLINE)
            barxado = self._soo_saar_magacyada(expr)
            jirka = [CeliStmt(qiimo=expr, sadar=expr.sadar, tiir=expr.tiir)]

        return HawlQeexidStmt(magac=magac, barxado=barxado, jirka=jirka, sadar=t.sadar, tiir=t.tiir)

    def _qabo_hawshan_expr(self) -> WacHawlExpr:
        t = self.soco()  # consume QABO_HAWSHAN
        magac = ""
        if self.qaado(TokenType.LPAREN):
            name_parts = []
            while not self.hubi(TokenType.RPAREN, TokenType.EOF, TokenType.NEWLINE):
                name_parts.append(self.soco())
            self.qasab(TokenType.RPAREN, "Waxaad ilowday ')' magaca hawsha ka dib.")
            if len(name_parts) == 1 and name_parts[0].nooc == TokenType.QORAAL:
                magac = str(name_parts[0].qiimo).strip()
            else:
                magac = "_".join(str(tk.qiimo).strip() for tk in name_parts)
        elif self.hubi(TokenType.QORAAL):
            magac = self.soco().qiimo.strip()
        elif self.hubi(TokenType.MAGAC):
            magac = self.soco().qiimo
        else:
            raise KhaladNaxwo("Sheeg magaca hawsha la qabanayo.", sadar=t.sadar, tiir=t.tiir)

        doodo = []
        if self.hubi(TokenType.LPAREN) and self.fiiri().sadar == t.sadar:
            self.soco()  # consume LPAREN
            if not self.hubi(TokenType.RPAREN):
                doodo.append(self._muujin())
                while self.qaado(TokenType.COMMA, TokenType.IYO):
                    if self.hubi(TokenType.RPAREN):
                        break
                    doodo.append(self._muujin())
                while not self.hubi(TokenType.RPAREN, TokenType.EOF, TokenType.NEWLINE):
                    self.qaado(TokenType.COMMA, TokenType.IYO)
                    if self.hubi(TokenType.RPAREN):
                        break
                    doodo.append(self._muujin())
            self.qasab(TokenType.RPAREN, "Waxaad ilowday ')' dhamaadka doodaha.")
        return WacHawlExpr(magac=magac, doodo=doodo, sadar=t.sadar, tiir=t.tiir)

    def _soo_saar_magacyada(self, expr: ASTNode) -> List[str]:
        magacyo = []
        def booqo(n):
            if n is None: return
            if isinstance(n, MagacExpr):
                if n.magac not in magacyo:
                    magacyo.append(n.magac)
            elif isinstance(n, HawlgalLabaaleExpr):
                booqo(n.bidix)
                booqo(n.midig)
            elif isinstance(n, HawlgalKeliyaExpr):
                booqo(n.shay)
            elif isinstance(n, WacHawlExpr):
                for d in n.doodo:
                    booqo(d)
            elif isinstance(n, LiisExpr):
                for w in n.walxo:
                    booqo(w)
            elif isinstance(n, TusmoHelExpr):
                booqo(n.liis_ama_qaamuus)
                booqo(n.tusmo)
            elif isinstance(n, XubinHelExpr):
                booqo(n.shay)
        booqo(expr)
        return magacyo

    def _hadallo_xirmo(self) -> List[ASTNode]:
        hadallo = []
        self._dhimo_meelaha_madhan()

        if self.qaado(TokenType.INDENT):
            while not self.hubi(TokenType.DEDENT, TokenType.EOF):
                h = self._hadal()
                if h:
                    hadallo.append(h)
                self._dhimo_meelaha_madhan()
            self.qaado(TokenType.DEDENT)
        else:
            # Single statement block
            h = self._hadal()
            if h:
                hadallo.append(h)

        return hadallo

    # --- Expressions ---

    def _shardi_muujin(self) -> ASTNode:
        return self._ama_muujin()

    def _muujin(self) -> ASTNode:
        return self._ama_muujin()

    def _ama_muujin(self) -> ASTNode:
        bidix = self._iyo_muujin()
        while self.qaado(TokenType.AMA):
            midig = self._iyo_muujin()
            bidix = HawlgalLabaaleExpr(bidix=bidix, calaanad="ama", midig=midig, sadar=bidix.sadar, tiir=bidix.tiir)
        return bidix

    def _iyo_muujin(self) -> ASTNode:
        bidix = self._sinnaan_muujin()
        while self.qaado(TokenType.IYO):
            midig = self._sinnaan_muujin()
            bidix = HawlgalLabaaleExpr(bidix=bidix, calaanad="sidoo kale", midig=midig, sadar=bidix.sadar, tiir=bidix.tiir)
        return bidix

    def _sinnaan_muujin(self) -> ASTNode:
        bidix = self._kala_sarreyn_muujin()
        while self.hubi(
            TokenType.LA_MID_YAHAY, TokenType.AAN_LA_MID_AHAYN,
            TokenType.KA_WEYN, TokenType.KA_YAR,
            TokenType.KA_WEYN_AMA_LA_MID, TokenType.KA_YAR_AMA_LA_MID
        ):
            op_tok = self.soco()
            cal = "=="
            if op_tok.nooc == TokenType.AAN_LA_MID_AHAYN: cal = "!="
            elif op_tok.nooc == TokenType.KA_WEYN: cal = ">"
            elif op_tok.nooc == TokenType.KA_YAR: cal = "<"
            elif op_tok.nooc == TokenType.KA_WEYN_AMA_LA_MID: cal = ">="
            elif op_tok.nooc == TokenType.KA_YAR_AMA_LA_MID: cal = "<="
            midig = self._kala_sarreyn_muujin()
            bidix = HawlgalLabaaleExpr(bidix=bidix, calaanad=cal, midig=midig, sadar=bidix.sadar, tiir=bidix.tiir)
        return bidix

    def _kala_sarreyn_muujin(self) -> ASTNode:
        bidix = self._kordhin_muujin()
        return bidix

    def _kordhin_muujin(self) -> ASTNode:
        bidix = self._dhufo_muujin()
        while self.hubi(TokenType.PLUS, TokenType.MINUS, TokenType.KU_DAR, TokenType.KA_JAR):
            tok = self.fiiri()
            if tok.qiimo in ("ku dartaa", "ku darta", "ka jartaa", "ka jarta"):
                break
            op_tok = self.soco()
            cal = "+" if op_tok.nooc in (TokenType.PLUS, TokenType.KU_DAR) else "-"
            midig = self._dhufo_muujin()
            bidix = HawlgalLabaaleExpr(bidix=bidix, calaanad=cal, midig=midig, sadar=bidix.sadar, tiir=bidix.tiir)
        return bidix

    def _dhufo_muujin(self) -> ASTNode:
        bidix = self._keliya_muujin()
        while self.hubi(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT, TokenType.KU_DHUFO, TokenType.U_QAYBI, TokenType.HARAA):
            tok = self.fiiri()
            if tok.qiimo in ("ku dhufataa", "ku dhufata", "u qaybisaa", "u qaybisa"):
                break
            op_tok = self.soco()
            if op_tok.nooc in (TokenType.STAR, TokenType.KU_DHUFO):
                cal = "*"
            elif op_tok.nooc in (TokenType.SLASH, TokenType.U_QAYBI):
                cal = "/"
            else:
                cal = "%"
            midig = self._keliya_muujin()
            bidix = HawlgalLabaaleExpr(bidix=bidix, calaanad=cal, midig=midig, sadar=bidix.sadar, tiir=bidix.tiir)
        return bidix

    def _keliya_muujin(self) -> ASTNode:
        if self.hubi(TokenType.MINUS, TokenType.MA_AHA):
            op_tok = self.soco()
            cal = "-" if op_tok.nooc == TokenType.MINUS else "ma"
            shay = self._keliya_muujin()
            return HawlgalKeliyaExpr(calaanad=cal, shay=shay, sadar=op_tok.sadar, tiir=op_tok.tiir)
        return self._tusmo_ama_wac_muujin()

    def _tusmo_ama_wac_muujin(self) -> ASTNode:
        shay = self._aasaasi_muujin()

        while True:
            # Dot property/method access: shay.xubin
            if self.hubi(TokenType.DOT) and self.fiiri(1).nooc == TokenType.MAGAC:
                self.soco()  # consume dot
                xubin_tok = self.soco()
                shay = XubinHelExpr(shay=shay, xubin=xubin_tok.qiimo, sadar=xubin_tok.sadar, tiir=xubin_tok.tiir)
            # Function/Method call with ()
            elif self.qaado(TokenType.LPAREN):
                doodo = []
                if not self.hubi(TokenType.RPAREN):
                    doodo.append(self._muujin())
                    while self.qaado(TokenType.COMMA):
                        doodo.append(self._muujin())
                self.qasab(TokenType.RPAREN, "Waxaad ilowday ')' dhamaadka wicitaanka hawsha.")
                shay = WacHawlExpr(magac=shay, doodo=doodo, sadar=shay.sadar, tiir=shay.tiir)
            # Indexing with []
            elif self.qaado(TokenType.LBRACKET):
                tusmo = self._muujin()
                self.qasab(TokenType.RBRACKET, "Waxaad ilowday ']' dhamaadka tusmada.")
                shay = TusmoHelExpr(liis_ama_qaamuus=shay, tusmo=tusmo, sadar=shay.sadar, tiir=shay.tiir)
            # Zero-signs function call without parentheses:
            elif isinstance(shay, MagacExpr) and shay.magac in self.hawlo_la_yaqaan:
                doodo = []
                STOP_TOKENS = (
                    TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.COLON, TokenType.DEDENT,
                    TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE,
                    TokenType.WAA, TokenType.EQUAL,
                    TokenType.KU_DAR, TokenType.KA_JAR, TokenType.KU_DHUFO, TokenType.U_QAYBI, TokenType.HARAA,
                    TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
                    TokenType.LA_MID_YAHAY, TokenType.AAN_LA_MID_AHAYN, TokenType.KA_WEYN, TokenType.KA_YAR,
                    TokenType.KA_WEYN_AMA_LA_MID, TokenType.KA_YAR_AMA_LA_MID,
                    TokenType.AMA
                )
                cur_line = shay.sadar
                while not self.hubi(*STOP_TOKENS) and self.fiiri().sadar == cur_line:
                    arg = self._keliya_muujin()
                    doodo.append(arg)
                    self.qaado(TokenType.COMMA, TokenType.IYO)
                    if shay.magac in ("tiro", "qoraal", "dherer", "xidid", "nooc", "run_been"):
                        # Unary built-in function takes 1 argument
                        break
                shay = WacHawlExpr(magac=shay.magac, doodo=doodo, sadar=shay.sadar, tiir=shay.tiir)
            else:
                break

        return shay

    def _aasaasi_muujin(self) -> ASTNode:
        t = self.fiiri()

        if t.nooc == TokenType.TIRO:
            self.soco()
            return TiroExpr(qiimo=t.qiimo, sadar=t.sadar, tiir=t.tiir)

        if t.nooc == TokenType.QORAAL:
            self.soco()
            return QoraalExpr(qiimo=t.qiimo, sadar=t.sadar, tiir=t.tiir)

        if t.nooc == TokenType.RUN:
            self.soco()
            return RunBeenExpr(qiimo=True, sadar=t.sadar, tiir=t.tiir)

        if t.nooc == TokenType.BEEN:
            self.soco()
            return RunBeenExpr(qiimo=False, sadar=t.sadar, tiir=t.tiir)

        if t.nooc == TokenType.WAXBA:
            self.soco()
            return WaxbaExpr(sadar=t.sadar, tiir=t.tiir)

        if t.nooc == TokenType.MAGAC:
            self.soco()
            return MagacExpr(magac=t.qiimo, sadar=t.sadar, tiir=t.tiir)

        # Parenthesized expression: ( expr )
        if self.qaado(TokenType.LPAREN):
            expr = self._muujin()
            self.qasab(TokenType.RPAREN, "Waxaad ilowday xiritaanka qawska ')'.")
            return expr

        # List literal: [1, 2, 3]
        if self.qaado(TokenType.LBRACKET):
            walxo = []
            self._dhimo_meelaha_madhan()
            if not self.hubi(TokenType.RBRACKET):
                walxo.append(self._muujin())
                while self.qaado(TokenType.COMMA):
                    self._dhimo_meelaha_madhan()
                    if self.hubi(TokenType.RBRACKET):
                        break
                    walxo.append(self._muujin())
            self._dhimo_meelaha_madhan()
            self.qasab(TokenType.RBRACKET, "Waxaad ilowday ']' dhamaadka liiska.")
            return LiisExpr(walxo=walxo, sadar=t.sadar, tiir=t.tiir)

        # Zero-sign list literal: liiska 10 iyo 20 iyo 30
        if self.qaado(TokenType.LIISKA):
            walxo = []
            while not self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.COLON, TokenType.DEDENT):
                if self.hubi(TokenType.WAA, TokenType.EQUAL):
                    break
                walxo.append(self._keliya_muujin())
                self.qaado(TokenType.COMMA, TokenType.IYO)
            return LiisExpr(walxo=walxo, sadar=t.sadar, tiir=t.tiir)

        # Dictionary / Object literal: {"magac": "Cali", "da'": 20}
        if self.qaado(TokenType.LBRACE):
            fureyaal_iyo_qiimayaal = []
            self._dhimo_meelaha_madhan()
            if not self.hubi(TokenType.RBRACE):
                fure = self._muujin()
                self.qasab(TokenType.COLON, "Waxaad ilowday ':' inta u dhaxeysa furaha iyo qiimaha qaamuuska.")
                qiimo = self._muujin()
                fureyaal_iyo_qiimayaal.append((fure, qiimo))
                while self.qaado(TokenType.COMMA):
                    self._dhimo_meelaha_madhan()
                    if self.hubi(TokenType.RBRACE):
                        break
                    fure = self._muujin()
                    self.qasab(TokenType.COLON, "Waxaad ilowday ':' inta u dhaxeysa furaha iyo qiimaha qaamuuska.")
                    qiimo = self._muujin()
                    fureyaal_iyo_qiimayaal.append((fure, qiimo))
            self._dhimo_meelaha_madhan()
            self.qasab(TokenType.RBRACE, "Waxaad ilowday '}' dhamaadka qaamuuska ama shayga.")
            return QaamuusExpr(fureyaal_iyo_qiimayaal=fureyaal_iyo_qiimayaal, sadar=t.sadar, tiir=t.tiir)

        # Explicit call: wac magac arg1 arg2 ...
        if self.qaado(TokenType.WAC):
            magac_tok = self.qasab(TokenType.MAGAC, "Sheeg magaca hawsha la wacayo.")
            doodo = []
            while not self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.COLON, TokenType.DEDENT):
                if self.hubi(TokenType.KU_DAR, TokenType.KA_JAR, TokenType.KU_DHUFO, TokenType.U_QAYBI, TokenType.HARAA, TokenType.WAA, TokenType.EQUAL):
                    break
                doodo.append(self._keliya_muujin())
                self.qaado(TokenType.COMMA, TokenType.IYO)
            return WacHawlExpr(magac=magac_tok.qiimo, doodo=doodo, sadar=t.sadar, tiir=t.tiir)

        # Natural function call: qabo hawshan ("iskudhufasho") (12, 3)
        if self.hubi(TokenType.QABO_HAWSHAN):
            return self._qabo_hawshan_expr()

        # Natural input: waydiin("Magacaa? ") or zero-signs waydiin gali lambarka
        if self.hubi(TokenType.WAYDIIN):
            self.soco()
            doodo = []
            if self.qaado(TokenType.LPAREN):
                if not self.hubi(TokenType.RPAREN):
                    doodo.append(self._muujin())
                self.qasab(TokenType.RPAREN, "Waxaad ilowday ')' ka dib waydiin.")
            elif self.hubi(TokenType.QORAAL):
                doodo.append(self._muujin())
            else:
                line_tokens = []
                cur_line = t.sadar
                while not self.hubi(TokenType.NEWLINE, TokenType.DOT, TokenType.EOF, TokenType.RPAREN) and self.fiiri().sadar == cur_line:
                    line_tokens.append(self.soco())
                kood_sadar = t.kood_sadar
                if line_tokens and kood_sadar:
                    start_char = line_tokens[0].tiir - 1
                    end_char = line_tokens[-1].tiir - 1 + len(str(line_tokens[-1].qiimo))
                    prompt_text = kood_sadar[start_char:end_char].strip().rstrip(".")
                else:
                    prompt_text = " ".join(str(tk.qiimo) for tk in line_tokens).rstrip(".")
                if prompt_text and not prompt_text.endswith(":") and not prompt_text.endswith(" "):
                    prompt_text += ": "
                doodo.append(QoraalExpr(qiimo=prompt_text, f_string=False, sadar=t.sadar, tiir=t.tiir))
            return WacHawlExpr(magac="waydiin", doodo=doodo, sadar=t.sadar, tiir=t.tiir)

        raise KhaladNaxwo(
            f"Kood aan la fahmin ama calaamad khaldan: '{t.qiimo}'",
            sadar=t.sadar,
            tiir=t.tiir,
            kood_sadar=t.kood_sadar,
            talo="Hubi qoraalka koodka meeshan ku yaalla."
        )
