from django.db import models
from .tovar import Tovar

class Sarza(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, related_name='sarze')
    mnozstvo = models.IntegerField(default=0)
    datum_exspiracie = models.DateField(null=True, blank=True)
    id_sarze = models.CharField(max_length=100)
    aktualna_cena = models.DecimalField(max_digits=10, decimal_places=2)

    _aktualnaCena: float = 0.0
    _datumExspiracie_int: int = 0
    _idSarze: int = 0
    _mnozstvo_extra: int = 0

    @property
    def aktualnaCena(self) -> float:
        return self._aktualnaCena

    @aktualnaCena.setter
    def aktualnaCena(self, value: float):
        self._aktualnaCena = value

    @property
    def datumExspiracie(self) -> int:
        return self._datumExspiracie_int

    @datumExspiracie.setter
    def datumExspiracie(self, value: int):
        self._datumExspiracie_int = value

    @property
    def idSarze(self) -> int:
        return self._idSarze

    @idSarze.setter
    def idSarze(self, value: int):
        self._idSarze = value

    @property
    def mnozstvo_attr(self) -> int:
        return self._mnozstvo_extra

    @mnozstvo_attr.setter
    def mnozstvo_attr(self, value: int):
        self._mnozstvo_extra = value

    def aktualizujCenu(self, nova_cena: int) -> None:
        self.aktualnaCena = float(nova_cena)

    def nastavitExpiraciu(self, datum: int) -> None:
        self.datumExspiracie = datum

    def vypocitajZlavu(self, percento: int) -> float:
        return self.aktualnaCena * (percento / 100)

    @classmethod
    def vytvoritNovu(cls, nazov: str, mnozstvo: int) -> 'Sarza':
        return cls()

    def aplikovat_zlavu(self, percento):
        """Method for UC03: Price adjustment when expiration is approaching"""
        multiplier = (100 - percento) / 100
        self.aktualna_cena = float(self.aktualna_cena) * multiplier
        self.save()