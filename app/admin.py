from django.contrib import admin
from .models import Brand, PlacaVideo, Laptop, Procesor, Categorie, Depozit, Stoc, Produs, Adresa, Promotie
# Register your models here.

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('nume','website_url')
    ordering = ('nume',)
    
@admin.register(PlacaVideo)
class PlacaVideoAdmin(admin.ModelAdmin):
    list_display = ('brand','pret','nume')
    ordering = ('brand','-pret','nume',)
    
@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand','pret','nume')
    ordering = ('brand','-pret','nume',)
    
@admin.register(Procesor)
class ProcesorAdmin(admin.ModelAdmin):
    list_display = ('brand','pret','nume')
    ordering = ('brand','-pret','nume',)
   
@admin.register(Promotie)
class PromotieAdmin(admin.ModelAdmin):
    list_display = ('data_inceput','data_sfarsit','nume')
    ordering = ('data_inceput','data_sfarsit','nume',)
    
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume',)
    ordering = ('nume',)
    
@admin.register(Depozit)
class DepozitAdmin(admin.ModelAdmin):
    list_display = ('nume','adresa')
    ordering = ('nume','adresa')
    
@admin.register(Stoc)
class StocAdmin(admin.ModelAdmin):
    list_display = ('produs','depozit','cantitate')
    ordering = ('produs','depozit','cantitate',)

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display = ('tip_produs','brand','pret','nume')
    ordering = ('tip_produs','brand','-pret','nume',)  
    
@admin.register(Adresa)
class AdresaAdmin(admin.ModelAdmin):  
    list_display = ('strada','numar','oras','judet')
    ordering = ('strada','numar','oras','judet')
    