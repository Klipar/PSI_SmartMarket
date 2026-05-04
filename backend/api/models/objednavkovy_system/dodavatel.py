from django.db import models

class Dodavatel(models.Model):
    meno = models.CharField(max_length=255)
    email = models.EmailField()

    _idDodavatela: int = 0

    @property
    def idDodavatela(self) -> int:
        return self._idDodavatela

    @idDodavatela.setter
    def idDodavatela(self, value: int):
        self._idDodavatela = value

    @property
    def email_attr(self) -> str:
        return self.email

    @email_attr.setter
    def email_attr(self, value: str):
        self.email = value

    @property
    def meno_attr(self) -> str:
        return self.meno

    @meno_attr.setter
    def meno_attr(self, value: str):
        self.meno = value

    def prijmiDopyt(self, navrh_objednavky) -> None:
        pass

    def __str__(self):
        return self.meno
