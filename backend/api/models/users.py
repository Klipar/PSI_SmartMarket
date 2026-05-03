from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SKLADNIK = 'SK', 'Warehouse Worker'
        MANAGER = 'MN', 'Purchasing Manager'
        SPRAVCA = 'SP', 'Store Manager'

    role = models.CharField(max_length=2, choices=Role.choices, default=Role.SKLADNIK)
    usek = models.CharField(max_length=100, blank=True, null=True)

    _meno: str = ""
    _schvalovaciLimit: float = 0.0

    @property
    def employee_id(self) -> int:
        return self.id

    @property
    def meno(self) -> str:
        return self._meno

    @meno.setter
    def meno(self, value: str):
        self._meno = value

    @property
    def schvalovaciLimit(self) -> float:
        return self._schvalovaciLimit

    @schvalovaciLimit.setter
    def schvalovaciLimit(self, value: float):
        self._schvalovaciLimit = value

    def prihlasitSa(self, login: str, heslo: str) -> bool:
        return True

    def naskenovatDodaciList(self, id_listu: int) -> int:
        return 0

    def naskenovatNaRegali(self, id_regalu: int) -> None:
        pass

    def potvrditPrijem(self) -> int:
        return 0

    def zadajSkutocneMnozstvo(self, mnozstvo: int) -> int:
        return mnozstvo

    def aktivovatRezim(self, rezim: str) -> bool:
        return True

    def aplikovatZlavu(self, id_polozky: int, percento: int) -> bool:
        return True

    def potvrditUkoncenie(self, id_operacie: int) -> bool:
        return True

    def vybratPolozkyNaZlavu(self, sprava_exspiracii) -> None:
        pass

    def potvrditAOdoslat(self, id_objednavky: int, id_dodavatela: int = None) -> bool:
        return True

    def skontrolovatNavrh(self, id_navrhu: int):
        return None