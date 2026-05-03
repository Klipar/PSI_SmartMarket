from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PolozkaNavrhu',
            new_name='PolozkaObjednavky',
        ),
        migrations.RenameField(
            model_name='polozkaobjednavky',
            old_name='cena_pri_objednavke',
            new_name='cena_za_kus',
        ),
        migrations.RenameField(
            model_name='polozkaobjednavky',
            old_name='mnozstvo',
            new_name='navrhovane_mnozstvo',
        ),
        migrations.RenameField(
            model_name='polozkaobjednavky',
            old_name='navrh',
            new_name='objednavka',
        ),
    ]
