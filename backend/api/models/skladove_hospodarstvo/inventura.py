from django.db import models
from ..pouzivatelia.users import User

class Inventura(models.Model):
    datum_zahajenia = models.DateTimeField(auto_now_add=True)
    kategoria = models.CharField(max_length=100)
    vykonal = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    _datum_zahajenia: int = 0
    _id_inventory: int = 0
    _kategoria: str = ""

    @property
    def datum_zahajenia(self) -> int:
        """Returns the start date."""
        return self._datum_zahajenia

    @datum_zahajenia.setter
    def datum_zahajenia(self, value: int):
        """Sets the start date."""
        self._datum_zahajenia = value

    @property
    def id_inventory(self) -> int:
        """Returns the inventory ID."""
        return self._id_inventory

    @id_inventory.setter
    def id_inventory(self, value: int):
        """Sets the inventory ID."""
        self._id_inventory = value

    @property
    def kategoria(self) -> str:
        """Returns the category."""
        return self._kategoria

    @kategoria.setter
    def kategoria(self, value: str):
        """Sets the category."""
        self._kategoria = value

    def porovnat_mnozstvo(self, mnozstvo1: int, mnozstvo2: int) -> int:
        """
        Compares two quantities and returns the difference.
        """
        return mnozstvo1 - mnozstvo2

    def zaregistrovat_rozdiel(self, rozdiel: int) -> None:
        """
        Registers the calculated difference.
        """
        print(f"Difference {rozdiel} registered for inventory ID: {self._id_inventory}")
