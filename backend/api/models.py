from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SKLADNIK = 'SK', 'Skladník'
        MANAGER = 'MN', 'Manažér nákupu'
        SPRAVCA = 'SP', 'Správca obchodu'

    role = models.CharField(max_length=2, choices=Role.choices, default=Role.SKLADNIK)
    usek = models.CharField(max_length=100, blank=True, null=True)

class Dodavatel(models.Model):
    meno = models.CharField(max_length=255)
    email = models.EmailField()

class Tovar(models.Model):
    nazov = models.CharField(max_length=255)
    ean_kod = models.CharField(max_length=13, unique=True)
    kriticky_limit = models.IntegerField(default=10)
    dodavatel = models.ForeignKey(Dodavatel, on_delete=models.SET_NULL, null=True)

    def skontrolovat_zasoby(self):
        """Реалізація методу skontrolovatZasoby() з UML"""
        return self.aktualny_stav() < self.kriticky_limit

    def aktualny_stav(self):
        """Розрахунок поточного залишку по всіх партіях"""
        return self.sarze.aggregate(total=models.Sum('mnozstvo'))['total'] or 0

class Sarza(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, related_name='sarze')
    id_sarze = models.CharField(max_length=100) # Номер партії
    mnozstvo = models.IntegerField()
    datum_exspiracie = models.DateField()
    aktualna_cena = models.DecimalField(max_digits=10, decimal_places=2)

    def aplikovat_zlavu(self, percento):
        """Метод для UC03: Зміна ціни при наближенні експірації"""
        multiplier = (100 - percento) / 100
        self.aktualna_cena = float(self.aktualna_cena) * multiplier
        self.save()

class NavrhObjednavky(models.Model):
    class Status(models.TextChoices):
        NA_SCHVALENIE = 'NS', 'Na schválenie'
        ODOSLANE = 'OD', 'Odoslané'
        ZAMIETNUTE = 'ZA', 'Zamietnuté'

    stav = models.CharField(max_length=2, choices=Status.choices, default=Status.NA_SCHVALENIE)
    dodavatel = models.ForeignKey(Dodavatel, on_delete=models.CASCADE)
    datum_vytvorenia = models.DateTimeField(auto_now_add=True)

    def vypocitaj_celkovu_sumu(self):
        """Метод з UML для розрахунку суми пропозиції"""
        total = sum(p.cena_pri_objednavke * p.mnozstvo for p in self.polozky.all())
        return total

class PolozkaNavrhu(models.Model):
    navrh = models.ForeignKey(NavrhObjednavky, related_name='polozky', on_delete=models.CASCADE)
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    mnozstvo = models.IntegerField()
    cena_pri_objednavke = models.DecimalField(max_digits=10, decimal_places=2)


class Inventura(models.Model):
    datum_zahajenia = models.DateTimeField(auto_now_add=True)
    kategoria = models.CharField(max_length=100)
    vykonal = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class ProtokolInventury(models.Model):
    inventura = models.OneToOneField(Inventura, on_delete=models.CASCADE)
    zisteny_rozdiel = models.IntegerField() # Різниця в кількості одиниць
    poznamka = models.TextField(blank=True)