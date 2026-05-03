from django.db import models
from .navrh_objednavky import NavrhObjednavky
from .tovar import Tovar

class PolozkaObjednavky(models.Model):
    objednavka = models.ForeignKey(NavrhObjednavky, related_name='polozky', on_delete=models.CASCADE)
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    navrhovane_mnozstvo = models.IntegerField()
    cena_za_kus = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tovar.nazov} - {self.navrhovane_mnozstvo} pcs"