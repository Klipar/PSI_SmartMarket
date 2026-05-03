from django.db import models
from . import Dodavatel

class Tovar(models.Model):
    nazov = models.CharField(max_length=255)
    ean_kod = models.CharField(max_length=13, unique=True)
    kriticky_limit = models.IntegerField(default=10)
    dodavatel = models.ForeignKey(Dodavatel, on_delete=models.SET_NULL, null=True)

    _aktualnyStav: int = 0
    _eanKod_int: int = 0
    _kritickyLimit_extra: int = 0
    _nazov_extra: str = ""

    @property
    def aktualnyStav(self) -> int:
        return self._aktualnyStav

    @aktualnyStav.setter
    def aktualnyStav(self, value: int):
        self._aktualnyStav = value

    @property
    def eanKod_attr(self) -> int:
        return self._eanKod_int

    @eanKod_attr.setter
    def eanKod_attr(self, value: int):
        self._eanKod_int = value

    @property
    def kritickyLimit_attr(self) -> int:
        return self._kritickyLimit_extra

    @kritickyLimit_attr.setter
    def kritickyLimit_attr(self, value: int):
        self._kritickyLimit_extra = value

    @property
    def nazov_attr(self) -> str:
        return self._nazov_extra

    @nazov_attr.setter
    def nazov_attr(self, value: str):
        self._nazov_extra = value

    def aktualizujStavZasob(self, mnozstvo: int) -> None:
        pass

    def hladajRucne(self, nazov: str) -> 'Tovar':
        return self

    def identifikujEAN(self, ean: int) -> None:
        pass

    def skontrolovatZasoby(self) -> bool:
        return self.aktualny_stav_db() < self.kriticky_limit

    def vypocitajPotrebu(self) -> int:
        return 0

    def aktualny_stav_db(self):
        return self.sarze.aggregate(total=models.Sum('mnozstvo'))['total'] or 0

    def __str__(self):
        return self.nazov