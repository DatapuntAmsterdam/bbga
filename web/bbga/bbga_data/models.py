from django.db import models

# Create your models here.


class Meta(models.Model):
    """
    """
    sort = models.CharField(max_length=5)
    thema = models.CharField(max_length=30)
    variabele = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=65)
    definitie = models.TextField()
    bron = models.CharField(max_length=50)
    peildatum = models.CharField(max_length=50)
    verschijningsfrequentie = models.CharField(max_length=50)

    eenheid = models.IntegerField(null=True)
    groep = models.CharField(max_length=50, null=True)
    format = models.CharField(max_length=5, null=True)
    thema_kleurentabel = models.CharField(max_length=50, null=True)
    kleurenpalet = models.IntegerField(null=True)
    minimum_aantal_inwoners = models.IntegerField(null=True)
    minimum_aantal_woningen = models.IntegerField(null=True)


#class Gebieden(models.Model):
#    """
#    """
#    pass


class Variabelen(models.Model):
    """
    """
    jaar = models.IntegerField()
    gebiedcode15 = models.CharField(max_length=4)
    variabele = models.CharField(max_length=30)
    waarde = models.FloatField(null=True)

    class Meta:
        unique_together = (('jaar', 'gebiedcode15', 'variabele'),)
        index_together = (
            ('jaar', 'gebiedcode15'),
            ('gebiedcode15', 'variabele')
        )
