from django.db import models

# Create your models here.


class Meta(models.Model):
    """
    Meta data van cijfers tabel
    """
    sort = models.CharField(max_length=5)
    thema = models.CharField(max_length=30)
    variabele = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=65)
    label_kort = models.CharField(max_length=50, null=True)
    definitie = models.TextField()
    tussenkop_kerncijfertabel =  models.CharField(max_length=65, null=True)
    bron = models.CharField(max_length=50)
    peildatum = models.CharField(max_length=50)
    verschijningsfrequentie = models.CharField(max_length=50)

    # EN
    topic = models.CharField(max_length=30, null=True)
    label_1 = models.CharField(max_length=100, null=True)
    definition = models.TextField()
    reference_date = models.CharField(max_length=50, null=True)
    frequency = models.CharField(max_length=100, null=True)

    eenheid = models.IntegerField(null=True)
    groep = models.CharField(max_length=50, null=True)
    format = models.CharField(max_length=5, null=True)
    thema_kleurentabel = models.CharField(max_length=50, null=True)
    kleurenpalet = models.IntegerField(null=True)
    minimum_aantal_inwoners = models.IntegerField(null=True)
    minimum_aantal_woningen = models.IntegerField(null=True)

    symbool = models.CharField(max_length=30, null=True)
    legendacode = models.CharField(max_length=30, null=True)


class Cijfers(models.Model):
    """
    Alle BBGA cijfers
    """
    jaar = models.IntegerField(db_index=True)
    gebiedcode15 = models.CharField(db_index=True, max_length=4)
    variabele = models.CharField(db_index=True, max_length=30)
    waarde = models.FloatField(null=True)

    class Meta:
        unique_together = (('jaar', 'gebiedcode15', 'variabele'),)
        index_together = (
            ('jaar', 'gebiedcode15'),
            ('gebiedcode15', 'variabele')
        )
