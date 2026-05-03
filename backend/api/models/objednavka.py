from django.db import models

class Objednavka(models.Model):
    navrh = models.OneToOneField('NavrhObjednavky', on_delete=models.SET_NULL, null=True, blank=True)
    datum_vytvorenia = models.DateTimeField(auto_now_add=True)
    stav = models.CharField(max_length=50, default="Vytvorená")

    _idObjednavky: int = 0
    _usek: str = ""

    @property
    def idObjednavky(self) -> int:
        return self._idObjednavky

    @idObjednavky.setter
    def idObjednavky(self, value: int):
        self._idObjednavky = value

    @property
    def usek(self) -> str:
        return self._usek

    @usek.setter
    def usek(self, value: str):
        self._usek = value

    def aktualizovatStav(self, novy_stav: str) -> None:
        self.stav = novy_stav

    def overitStav(self) -> None:
        pass

    def __str__(self):
        return f"Order #{self.id} - {self.stav}"