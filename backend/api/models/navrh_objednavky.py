from django.db import models
from .dodavatel import Dodavatel

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
    def total_price(self):
        """Calculate total price for the order"""
        return float(sum(
            float(item.cena_za_kus) * item.navrhovane_mnozstvo
            for item in self.polozky.all()
        ))

    @property
    def items_count(self):
        """Get number of items"""
        return self.polozky.count()

    @property
    def supplier_name(self):
        """Get supplier name"""
        return self.dodavatel.meno if self.dodavatel else ""

    def vypocitajCelkovuSumu(self) -> float:
        """Legacy method for compatibility"""
        return self.total_price

    def __str__(self):
        return f"Order #{self.id} ({self.supplier_name})"


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


    def zlucitPodlaDodavatela(self, id_dodavatela: int) -> None:
        pass
