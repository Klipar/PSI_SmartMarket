from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SKLADNIK = 'SK', 'Warehouse Worker'
        MANAGER = 'MN', 'Purchasing Manager'
        SPRAVCA = 'SP', 'Store Manager'

    role = models.CharField(max_length=2, choices=Role.choices, default=Role.SKLADNIK)
    usek = models.CharField(max_length=100, blank=True, null=True)

class Dodavatel(models.Model):
    meno = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.meno

class Tovar(models.Model):
    nazov = models.CharField(max_length=255)
    ean_kod = models.CharField(max_length=13, unique=True)
    kriticky_limit = models.IntegerField(default=10)
    dodavatel = models.ForeignKey(Dodavatel, on_delete=models.SET_NULL, null=True)

    def skontrolovat_zasoby(self):
        """Implementation of the skontrolovatZasoby() method from UML"""
        return self.aktualny_stav() < self.kriticky_limit

    def aktualny_stav(self):
        """Calculation of the current stock across all batches"""
        return self.sarze.aggregate(total=models.Sum('mnozstvo'))['total'] or 0

    def __str__(self):
        return self.nazov

class Sarza(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, related_name='sarze')
    id_sarze = models.CharField(max_length=100)
    mnozstvo = models.IntegerField()
    datum_exspiracie = models.DateField()
    aktualna_cena = models.DecimalField(max_digits=10, decimal_places=2)

    def aplikovat_zlavu(self, percento):
        """Method for UC03: Price adjustment when expiration is approaching"""
        multiplier = (100 - percento) / 100
        self.aktualna_cena = float(self.aktualna_cena) * multiplier
        self.save()

class NavrhObjednavky(models.Model):
    class Status(models.TextChoices):
        NA_SCHVALENIE = 'NS', 'Pending Approval'
        ODOSLANE = 'OD', 'Sent'
        ZAMIETNUTE = 'ZA', 'Rejected'

    stav = models.CharField(max_length=2, choices=Status.choices, default=Status.NA_SCHVALENIE)
    dodavatel = models.ForeignKey(Dodavatel, on_delete=models.CASCADE)
    datum_vytvorenia = models.DateTimeField(auto_now_add=True)

    def vypocitaj_celkovu_sumu(self):
        """Method for calculating the proposal total (uses current fields)"""
        return sum(p.cena_za_kus * p.navrhovane_mnozstvo for p in self.polozky.all())

    def __str__(self):
        return f"Order #{self.id} ({self.dodavatel.meno})"

class PolozkaObjednavky(models.Model):
    """This class replaces PolozkaNavrhu for UC02 compliance"""
    objednavka = models.ForeignKey(NavrhObjednavky, related_name='polozky', on_delete=models.CASCADE)
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    navrhovane_mnozstvo = models.IntegerField()
    cena_za_kus = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tovar.nazov} - {self.navrhovane_mnozstvo} pcs"

class Inventura(models.Model):
    datum_zahajenia = models.DateTimeField(auto_now_add=True)
    kategoria = models.CharField(max_length=100)
    vykonal = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class ProtokolInventury(models.Model):
    inventura = models.OneToOneField(Inventura, on_delete=models.CASCADE)
    zisteny_rozdiel = models.IntegerField()
    poznamka = models.TextField(blank=True)