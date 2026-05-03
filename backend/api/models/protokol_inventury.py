from django.db import models
from .inventura import Inventura

class ProtokolInventury(models.Model):
    inventura = models.OneToOneField(Inventura, on_delete=models.CASCADE)
    zisteny_rozdiel = models.IntegerField()
    poznamka = models.TextField(blank=True)

    _idProtokolu: int = 0
    _zistenyRozdiel_extra: int = 0

    @property
    def idProtokolu_attr(self) -> int:
        return self._idProtokolu

    @idProtokolu_attr.setter
    def idProtokolu_attr(self, value: int):
        self._idProtokolu = value

    @property
    def zistenyRozdiel_extra(self) -> int:
        return self._zistenyRozdiel_extra

    @zistenyRozdiel_extra.setter
    def zistenyRozdiel_extra(self, value: int):
        self._zistenyRozdiel_extra = value

    def idProtokolu(self) -> None:
        pass