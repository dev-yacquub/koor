"""
AST (Abstract Syntax Tree) Nodes for Koor Programming Language.
"""

from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class ASTNode:
    sadar: int = 1
    tiir: int = 1

@dataclass
class Barnaamij(ASTNode):
    hadallo: List[ASTNode] = None

    def __post_init__(self):
        if self.hadallo is None:
            self.hadallo = []

# --- Expressions ---

@dataclass
class TiroExpr(ASTNode):
    qiimo: Any = 0

@dataclass
class QoraalExpr(ASTNode):
    qiimo: str = ""
    f_string: bool = False

@dataclass
class RunBeenExpr(ASTNode):
    qiimo: bool = True

@dataclass
class WaxbaExpr(ASTNode):
    pass

@dataclass
class MagacExpr(ASTNode):
    magac: str = ""

@dataclass
class HawlgalLabaaleExpr(ASTNode):
    bidix: ASTNode = None
    calaanad: str = ""
    midig: ASTNode = None

@dataclass
class HawlgalKeliyaExpr(ASTNode):
    calaanad: str = ""
    shay: ASTNode = None

@dataclass
class WacHawlExpr(ASTNode):
    magac: str = ""
    doodo: List[ASTNode] = None

    def __post_init__(self):
        if self.doodo is None:
            self.doodo = []

@dataclass
class LiisExpr(ASTNode):
    walxo: List[ASTNode] = None

    def __post_init__(self):
        if self.walxo is None:
            self.walxo = []

@dataclass
class QaamuusExpr(ASTNode):
    fureyaal_iyo_qiimayaal: List[tuple] = None

    def __post_init__(self):
        if self.fureyaal_iyo_qiimayaal is None:
            self.fureyaal_iyo_qiimayaal = []

@dataclass
class TusmoHelExpr(ASTNode):
    liis_ama_qaamuus: ASTNode = None
    tusmo: ASTNode = None

# --- Statements ---

@dataclass
class QorStmt(ASTNode):
    """waxaad soo saartaa ... / daabac ..."""
    qoraallo: List[ASTNode] = None

    def __post_init__(self):
        if self.qoraallo is None:
            self.qoraallo = []

@dataclass
class GeliStmt(ASTNode):
    """magac = qiimo / magac waa qiimo / qeex magac inuu yahay qiimo"""
    magac: str = ""
    qiimo: ASTNode = None

@dataclass
class BeddelStmt(ASTNode):
    """waxaad ku dartaa 1 x / waxaad ka jartaa 2 x"""
    magac: str = ""
    hawlgal: str = "+"
    qiimo: ASTNode = None

@dataclass
class HaddiiStmt(ASTNode):
    """haddii shardi: ... haddii_kale: ... kale: ..."""
    shardi: ASTNode = None
    haddii_run_tahay: List[ASTNode] = None
    haddii_kale: List[tuple] = None  # List of (shardi, statements)
    kale: Optional[List[ASTNode]] = None

    def __post_init__(self):
        if self.haddii_run_tahay is None:
            self.haddii_run_tahay = []
        if self.haddii_kale is None:
            self.haddii_kale = []

@dataclass
class IntaStmt(ASTNode):
    """inta shardi: ..."""
    shardi: ASTNode = None
    jirka: List[ASTNode] = None

    def __post_init__(self):
        if self.jirka is None:
            self.jirka = []

@dataclass
class KuCeliStmt(ASTNode):
    """ku celi N jeer: ..."""
    jeer: ASTNode = None
    jirka: List[ASTNode] = None

    def __post_init__(self):
        if self.jirka is None:
            self.jirka = []

@dataclass
class KastaStmt(ASTNode):
    """kasta oo ku jira liiska: ..."""
    doorsoome: str = ""
    liis_expr: ASTNode = None
    jirka: List[ASTNode] = None

    def __post_init__(self):
        if self.jirka is None:
            self.jirka = []

@dataclass
class HawlQeexidStmt(ASTNode):
    """hawl magac(barxado): ..."""
    magac: str = ""
    barxado: List[str] = None
    jirka: List[ASTNode] = None

    def __post_init__(self):
        if self.barxado is None:
            self.barxado = []
        if self.jirka is None:
            self.jirka = []

@dataclass
class XubinHelExpr(ASTNode):
    """shay.sifo ama shay.hawl()"""
    shay: ASTNode = None
    xubin: str = ""

@dataclass
class CeliStmt(ASTNode):
    """waxaad soo celisaa ... / celi ..."""
    qiimo: Optional[ASTNode] = None

@dataclass
class KaBaxStmt(ASTNode):
    """ka bax (break)"""
    pass

@dataclass
class KaBoodStmt(ASTNode):
    """ka bood (continue)"""
    pass

@dataclass
class XubinGeliStmt(ASTNode):
    """shay.sifo = qiimo ama kan.sifo waa qiimo"""
    shay: ASTNode = None
    xubin: str = ""
    qiimo: ASTNode = None

@dataclass
class TusmoGeliStmt(ASTNode):
    """liis[0] = qiimo ama qaamuus["fure"] = qiimo"""
    shay: ASTNode = None
    tusmo: ASTNode = None
    qiimo: ASTNode = None

@dataclass
class HadalKeliyaStmt(ASTNode):
    muujin: ASTNode = None

