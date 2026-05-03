from django.db import models
from datetime import date
from typing import List
from . import Sarza

class SpravaOExspiracii(models.Model):
    _datumGenerovania: date = date.today()
    _pocetPoloziek: int = 0

    @property
    def datumGenerovania(self) -> date:
        return self._datumGenerovania

    @datumGenerovania.setter
    def datumGenerovania(self, value: date):
        self._datumGenerovania = value

    @property
    def pocetPoloziek(self) -> int:
        return self._pocetPoloziek

    @pocetPoloziek.setter
    def pocetPoloziek(self, value: int):
        self._pocetPoloziek = value

    def getZoznamKritickychSarzi(self, limit: int) -> List[Sarza]:
        return []