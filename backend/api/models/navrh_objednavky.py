from django.db import models
from . import Dodavatel

class NavrhObjednavky(models.Model):
    class Status(models.TextChoices):
        NA_SCHVALENIE = 'NS', 'Pending Approval'
        ODOSLANE = 'OD', 'Sent'
        ZAMIETNUTE = 'ZA', 'Rejected'

    stav = models.CharField(max_length=2, choices=Status.choices, default=Status.NA_SCHVALENIE)
    dodavatel = models.ForeignKey(Dodavatel, on_delete=models.CASCADE)
    datum_vytvorenia = models.DateTimeField(auto_now_add=True)

    _celkovaSuma: float = 0.0
    _idNavrhu: int = 0
    _stav_string: str = ""

    @property
    def celkovaSuma(self) -> float:
        return self._celkovaSuma

    @celkovaSuma.setter
    def celkovaSuma(self, value: float):
        self._celkovaSuma = value

    @property
    def idNavrhu(self) -> int:
        return self._idNavrhu

    @idNavrhu.setter
    def idNavrhu(self, value: int):
        self._idNavrhu = value

    @property
    def stav_string(self) -> str:
        return self._stav_string

    @stav_string.setter
    def stav_string(self, value: str):
        self._stav_string = value

    def vypocitajCelkovuSumu(self) -> float:
        return float(sum(p.cena_za_kus * p.navrhovane_mnozstvo for p in self.polozky.all()))

    def zlucitPodlaDodavatela(self, id_dodavatela: int) -> None:
        pass

    def __str__(self):
        return f"Order #{self.id} ({self.dodavatel.meno})"