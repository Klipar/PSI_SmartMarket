from django.db import models
from typing import List
from . import SpravaOExspiracii, Tovar

class SystemovyMonitor(models.Model):
    _interval: int = 0

    @property
    def interval(self) -> int:
        return self._interval

    @interval.setter
    def interval(self, value: int):
        self._interval = value

    def analyzujDatumiSpotreby(self, limit: int) -> SpravaOExspiracii:
        # Returns an instance of SpravaOExspiracii based on limit
        return SpravaOExspiracii()

    def identifikujPodlimity(self) -> List[Tovar]:
        # Returns a list of Tovar items below critical limit
        return []

    def spustitKontrolu(self) -> None:
        # Triggers system check logic
        pass

    def synchronizovatSPokladnou(self, id_pokladne: int, suma: float) -> bool:
        # Syncs data with the cash register system
        return True