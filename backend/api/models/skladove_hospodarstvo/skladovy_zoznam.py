from django.db import models

class SkladovyZoznam(models.Model):
    _idZaznamu: int = 0
    _poznamka: str = ""

    @property
    def idZaznamu(self) -> int:
        return self._idZaznamu

    @idZaznamu.setter
    def idZaznamu(self, value: int):
        self._idZaznamu = value

    @property
    def poznamka(self) -> str:
        return self._poznamka

    @poznamka.setter
    def poznamka(self, value: str):
        self._poznamka = value

    def zaznamenatPrijem(self) -> bool:
        return True