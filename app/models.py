from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Brand(models.Model):
    class Meta:
        verbose_name_plural = "Branduri"
        ordering = ['nume']
        get_latest_by = ['-data_adaugare']
    
    nume = models.CharField(max_length=100, unique=True, error_messages={'unique': 'Acest brand exista deja.'})
    logo = models.ImageField(upload_to='logouri_branduri/', blank=True, null=True, default=None)
    website_url = models.URLField(null=True, default=None, blank=True)
    data_adaugare = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return self.nume
    
    
class Produs(models.Model):
    class Meta:
        verbose_name_plural = "Produse"
        get_latest_by = ['-data_lansare']
        ordering = ['-data_lansare']
        indexes = [
            models.Index(fields=['nume'], name='idx_produs_nume'),
            models.Index(
                fields=['brand', 'tip_produs'],
                name='idx_produs_brand_tip'
            ),
            models.Index(
                fields=['pret'],
                name='idx_produs_pret'
            ),
            models.Index(
                fields=['-data_lansare'],
                name='idx_produs_lansare'
            ),
        ]
        
    class TipProdus(models.TextChoices):
        LAPTOP = 'Laptop'
        PROCESOR = 'Procesor'
        PLACA_VIDEO = 'Placa Video'

    nume = models.CharField(max_length=100)
    # Django creaza automat un index pentru campul ForeignKey.
    # Brandul unui produs se poate schimba.
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='produse')
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    descriere = models.TextField(null=True, default=None, blank=True)
    tip_produs = models.CharField(max_length=20, choices=TipProdus.choices)
    data_adaugare = models.DateTimeField(auto_now_add=True, blank=True)
    durata_garantie = models.DurationField(help_text="Durata grantie in formatul '[DD] [HH:[MM:]]ss'. E.g. '30 00:00:00' pentru 30 de zile.")
    imagine = models.ImageField(upload_to='imagini_produse/', blank=True,null=True, default=None) 
    slug = models.SlugField(unique=True, error_messages={'unique': 'Acest slug exista deja. Alege altul.'})
    cod_producator = models.CharField(max_length=100)   
    data_lansare = models.DateField()
    
    def __str__(self):
        return f"{self.tip_produs} {self.brand} ({self.nume}) - {self.pret} RON"


class Laptop(Produs):
    class Meta: # type: ignore
        verbose_name_plural = "Laptopuri"
    
    class SistemOperare(models.TextChoices):
        WINDOWS = 'WIN','Windows'
        LINUX = 'LIN','Linux'
        MACOS = 'MAC','macOS'
        FARA_SISTEM = 'FSO','Fara sistem de operare'
    
    class RezolutieEcran(models.TextChoices):
        HD = 'HD','HD (1366x768)'
        FULL_HD = 'FHD','Full HD (1920x1080)'
        QHD = 'QHD','QHD (2560x1440)'
        UHD = 'UHD','UHD (3840x2160)'
        
    class TipStocare(models.TextChoices):
        HDD = 'HDD','HDD'
        SSD = 'SSD','SSD'
    
    class Culori(models.TextChoices):
        NEGRU = 'Negru','Negru'
        ARGINTIU = 'Argintiu','Argintiu'
        GRI = 'Gri','Gri'
        ALB = 'Alb','Alb'

    culori = ArrayField(models.CharField(max_length=20, choices=Culori.choices),help_text="Culorile disponibile pentru acest laptop separate prin virgula (Negru, Argintiu, Gri sau Alb).") 
    nume_procesor = models.CharField(max_length=100)
    placa_video = models.CharField(max_length=100)
    capacitate_ram = models.PositiveIntegerField(help_text="Capacitatea RAM in GB.", validators=[MinValueValidator(1)])
    capacitate_stocare = models.PositiveIntegerField(help_text="Capacitatea stocare in GB.", validators=[MinValueValidator(1)])
    tip_stocare = models.CharField(max_length=3, choices=TipStocare.choices, default=TipStocare.SSD)
    sistem_de_operare = models.CharField(max_length=3, choices=SistemOperare.choices, default=SistemOperare.FARA_SISTEM)
    greutate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Greutatea laptopului in kg.") 
    dimensiune_ecran = models.DecimalField(max_digits=4, decimal_places=2, help_text="Dimensiunea ecranului in inch.", default=Decimal('16.00'))
    rezolutie_ecran = models.CharField(max_length=3, choices=RezolutieEcran.choices)
    rata_refresh = models.PositiveIntegerField(help_text="Rata de refresh a ecranului in Hz.", validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Laptop {self.brand} ({self.nume}) - {self.pret} RON"
    

class Procesor(Produs):
    class Meta: # type: ignore
        verbose_name_plural = "Procesoare"
        
    nucleu = models.CharField(max_length=100)
    numar_nuclee = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Numarul de nuclee al procesorului.")
    numar_threaduri = models.PositiveIntegerField(null=True, default=None, blank=True, validators=[MinValueValidator(1)], help_text="Numarul de threaduri al procesorului. Daca procesorul nu suporta Hyper-Threading, acest camp este egal cu numarul de nuclee.")
    memorie_cache_l1 = models.DecimalField(max_digits=10, decimal_places=2, help_text="Memorie cache L1 in KB.", null=True, default=None, blank=True)
    memorie_cache_l2 = models.DecimalField(max_digits=10, decimal_places=2,help_text="Memorie cache L2 in KB.", null=True, default=None, blank=True)
    memorie_cache_l3 = models.DecimalField(max_digits=10, decimal_places=2,help_text="Memorie cache L3 in KB.", null=True, default=None, blank=True)
    frecventa = models.PositiveIntegerField(help_text="Frecventa in Mhz.", validators=[MinValueValidator(1)])
    putere_totala_disipata = models.PositiveIntegerField(help_text="Puterea totala disipata in Wati.", validators=[MinValueValidator(1)])
    serie = models.CharField(max_length=50)
    socket = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Procesor {self.brand} ({self.nume}) - {self.pret} RON"
        
    

class PlacaVideo(Produs):
    class Meta: # type: ignore
        verbose_name = "Placa Video"
        verbose_name_plural = "Placi Video"
    
    memorie = models.PositiveIntegerField(help_text="Capacitate VRAM in GB.", validators=[MinValueValidator(1)])
    tip_memorie = models.CharField(max_length=50)
    frecventa = models.PositiveIntegerField(help_text="Frecventa in MHz.", validators=[MinValueValidator(1)])
    model = models.CharField(max_length=50)
    interfata = models.CharField(max_length=50, help_text="Interfata de conectare (ex: PCIe 4.0 x16).")
    
    def __str__(self):
        return f"Placa Video {self.brand} ({self.nume}) - {self.pret} RON"
        
    
    
class Categorie(models.Model):
    class Meta:
        ordering = ['nume']
        get_latest_by = ['-data_adaugare']
        verbose_name_plural = "Categorii"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(culoare__regex=r'^#[0-9A-Fa-f]{6}$'),
                name='categorie_culoare_format_valid',
                violation_error_message='Culoarea trebuie sa fie in format hexazecimal (ex: #FFFFFF).'
                )
        ]
    
    nume = models.CharField(max_length=100, unique=True, error_messages={'unique': 'Aceasta categorie exista deja.'})
    descriere = models.TextField()
    culoare = models.CharField(max_length=7, help_text="Culoarea trebuie sa fie in format hexazecimal (ex: #FFFFFF).")
    sigla = models.ImageField(upload_to='sigle_categorii/', blank=True, null=True, default=None)
    data_adaugare = models.DateTimeField(auto_now_add=True, blank=True) 
    produse = models.ManyToManyField(Produs, related_name='categorii', blank=True)
    
    def __str__(self):
        return self.nume
    
    
class Promotie(models.Model):
    class Meta:
        verbose_name_plural = "Promotii"
        indexes = [
          models.Index(
                fields=['data_inceput','data_sfarsit'],
                name='idx_promotie_data_in_sf'
            ),
        ]
        constraints = [
                    models.CheckConstraint(
                        condition=(models.Q(tip_discount='PROC') & models.Q(discount__lte=100) & models.Q(discount__gte=1)) | (models.Q(tip_discount='SUMA') & models.Q(discount__gte=0)),
                        name='promotie_discount_valid',
                        violation_error_message="Discountul procentual trebuie sa fie intre 1 si 100."
                    ),
                    models.CheckConstraint(
                        condition=models.Q(data_inceput__lt=models.F('data_sfarsit')),
                        name='promotie_data_inceput_inainte_data_sfarsit',
                        violation_error_message="Data de inceput a promotiei trebuie sa fie inainte de data de sfarsit."
                    )
                ]  
    
    class TIP_DISCOUNT(models.TextChoices):
        PROCENT = 'PROC','Procentual'
        SUMA = 'SUMA','Suma fixa'
    
    nume = models.CharField(max_length=100)
    descriere = models.TextField()
    data_inceput = models.DateTimeField()
    data_sfarsit = models.DateTimeField()
    tip_discount = models.CharField(max_length=4, choices=TIP_DISCOUNT.choices, default=TIP_DISCOUNT.PROCENT)
    discount = models.PositiveIntegerField(help_text="Daca tipul de discount este procentual, valoarea trebuie sa fie intre 1 si 100. Altfel, valoarea trebuie sa fie mai mare sau egala cu 0.")
    produse = models.ManyToManyField(Produs, related_name='promotii', blank=True)
    
    def __str__(self):
        return self.nume


class Adresa(models.Model):
    class Meta:
        verbose_name_plural = "Adrese"
        constraints =[
            models.CheckConstraint(
                condition=models.Q(cod_postal__regex=r'^\d{6}$'),
                name='adresa_cod_postal_format_valid',
                violation_error_message='Codul postal trebuie sa fie format din 6 cifre.'
            ),
            models.CheckConstraint(
                condition=models.Q(scara__isnull=True) | models.Q(scara__regex=r'^[A-Z]$'),
                name='adresa_scara_format_valid',
                violation_error_message='Scara trebuie sa fie o litera din intervalul A-Z.'
            )
        ]
    
    def __str__(self):
        return f"Strada {self.strada}, nr. {self.numar}, {self.oras}, {self.judet}, {self.cod_postal}"

    #linie_adresa_1 = models.CharField(max_length=200, help_text="Strada, numar.") 
    #linie_adresa_2 = models.CharField(max_length=200, blank=True, null=True, help_text="Bloc, scara, etaj, apartament.") 
    bloc = models.CharField(max_length=20, blank=True, null=True)
    scara = models.CharField(max_length=1, blank=True, null=True, default=None, help_text="Scara trebuie sa fie o litera din intervalul A-Z.")
    etaj = models.CharField(max_length=10, blank=True, null=True)
    apartament = models.CharField(max_length=20, blank=True, null=True)
    strada = models.CharField(max_length=100)
    numar = models.PositiveIntegerField()
    oras = models.CharField(max_length=50)
    cod_postal = models.CharField(max_length=6, error_messages={'max_length': 'Codul postal trebuie sa fie format din 6 cifre.'})
    judet = models.CharField(max_length=50)


class Depozit(models.Model):
    class Meta:
        verbose_name_plural = "Depozite"
    
    def __str__(self):
        return self.nume

    nume = models.CharField(max_length=100, unique=True)
    adresa = models.OneToOneField(Adresa, on_delete=models.PROTECT, related_name='depozit')
    data_adaugare = models.DateTimeField(auto_now_add=True, blank=True)
    stocuri = models.ManyToManyField(Produs, through='Stoc', related_name='depozite', blank=True)
    

class Stoc(models.Model):
    class Meta:
        verbose_name_plural = "Stocuri"
        constraints = [
            models.UniqueConstraint(fields=['produs', 'depozit'], name='produs_depozit_unic')
        ]
    
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name='stocuri')
    depozit = models.ForeignKey(Depozit, on_delete=models.CASCADE, related_name='inregistrari_stoc')
    cantitate = models.PositiveIntegerField(default=0, error_messages={'min_value': 'Cantitatea nu poate fi negativa.'})

    def __str__(self):
      return f"{self.produs} - {self.depozit}: {self.cantitate}"