"""
Nidaamka Maareynta Khaladaadka ee Koor (Error Diagnostics)
Dhammaan farriimaha khaladka waxay ku qoran yihiin Af-Soomaali saafi ah oo cad.
"""

from typing import Optional

class KoorKhalad(Exception):
    """Fasalka aasaasiga ah ee dhammaan khaladaadka Koor."""
    def __init__(self, farriin: str, sadar: Optional[int] = None, tiir: Optional[int] = None, kood_sadar: Optional[str] = None, talo: Optional[str] = None):
        self.farriin = farriin
        self.sadar = sadar
        self.tiir = tiir
        self.kood_sadar = kood_sadar
        self.talo = talo
        super().__init__(self.habee())

    def habee(self) -> str:
        natiijo = []
        cinwaan = f"❌ [{self.__class__.__name__}]"
        if self.sadar is not None:
            cinwaan += f" Sadarka {self.sadar}"
            if self.tiir is not None:
                cinwaan += f", Tiirka {self.tiir}"
        cinwaan += f": {self.farriin}"
        natiijo.append(cinwaan)

        if self.kood_sadar:
            natiijo.append(f"    │")
            natiijo.append(f"    │  {self.kood_sadar.rstrip()}")
            if self.tiir is not None and self.tiir > 0:
                calaamad = " " * (self.tiir - 1) + "^"
                natiijo.append(f"    │  {calaamad}")

        if self.talo:
            natiijo.append(f"💡 TALO: {self.talo}")

        return "\n".join(natiijo)


class KhaladNaxwo(KoorKhalad):
    """Khalad ku saabsan naxwaha qoraalka koodka."""
    pass

class KhaladMagac(KoorKhalad):
    """Khalad dhacay markii la adeegsaday magac ama doorsoome aan la aqoon."""
    pass

class KhaladNooc(KoorKhalad):
    """Khalad ku saabsan hawlgal noocyo aan is qaadan karin lagu sameeyey."""
    pass

class KhaladQiimo(KoorKhalad):
    """Khalad ku saabsan qiime aan sax ahayn."""
    pass

class KhaladEberLooQaybiyay(KoorKhalad):
    """Khalad dhacay markii tiro eber loo qaybiyey."""
    pass

class KhaladSocod(KoorKhalad):
    """Khalad dhaca xilliga barnaamijku socdo."""
    pass
