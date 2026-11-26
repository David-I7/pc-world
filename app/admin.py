import csv
from datetime import datetime, timezone
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.utils.html import format_html
from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .utils.date import formateaza_data
from .models import Brand, PlacaVideo, Laptop, Procesor, Categorie, Depozit, Stoc, Produs, Adresa, Promotie
# Register your models here.


admin.site.site_header = "PC World - Panou de administrare"
admin.site.site_title = "PC World | Administrare"
admin.site.index_title = "Administrarea magazinului online"
admin.site.site_url = "/app"
      
fieldset_produs:list[tuple[str, dict[str, tuple[str, ...]]]] = [
  ('Informatii produs',{
    'fields':('nume','brand','pret','descriere','tip_produs','durata_garantie','imagine','slug','cod_producator','data_lansare','taguri')
  })
]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('nume','website_url')
    ordering = ('nume',)
    search_fields = ('^nume','website_url',)
    search_help_text = 'Cauta dupa nume sau URL website brand.'

@admin.register(PlacaVideo)
class PlacaVideoAdmin(admin.ModelAdmin):
    list_display = ('brand','pret','nume')
    ordering = ('brand','-pret','nume',)
    search_fields = ('nume','^brand__nume',)
    search_help_text = 'Cauta dupa nume sau brand placa video.'
    
    fieldsets = (
      fieldset_produs[0], # type: ignore
      ('Informatii Placa Video',{
        'fields':('memorie','tip_memorie','frecventa','interfata','model')
      },)
    )

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand','pret','nume')
    ordering = ('brand','-pret','nume',)
    search_fields = ('nume','^brand__nume',)
    search_help_text = 'Cauta dupa nume sau brand laptop.'
    
    fieldsets = (
      fieldset_produs[0], # type: ignore
      ('Informatii Laptop',{
        'fields':('culori','nume_procesor','placa_video','capacitate_ram','capacitate_stocare','tip_stocare','sistem_de_operare','greutate','dimensiune_ecran','rezolutie_ecran','rata_refresh')
      },)
    )

@admin.register(Procesor)
class ProcesorAdmin(admin.ModelAdmin):
    list_display = ('brand','pret','nume')
    ordering = ('brand','-pret','nume',)
    search_fields = ('nume','^brand__nume',)
    search_help_text = 'Cauta dupa nume sau brand procesor.'

    fieldsets = (
      fieldset_produs[0], # type: ignore
      ('Informatii Procesor',{
        'fields':('nucleu','numar_nuclee','numar_threaduri','memorie_cache_l1','memorie_cache_l2','memorie_cache_l3','frecventa','putere_totala_disipata','serie','socket')
      },)
    )
   
@admin.register(Promotie)
class PromotieAdmin(admin.ModelAdmin):
    list_display = ('data_inceput_formatata','data_sfarsit_formatata','nume','discount_formatat','este_activa',)
    ordering = ('-data_inceput','data_sfarsit','nume',)
    search_fields = ('^nume','tip_discount',)
    search_help_text = 'Cauta dupa nume promotie sau tip discount.'
    list_filter = ('data_inceput','data_sfarsit',)
    
    @admin.display(description='Este activa?', boolean=True, ordering='data_inceput')
    def este_activa(self, obj):
        today = datetime.now(tz=timezone.utc)
        return obj.data_inceput <= today <= obj.data_sfarsit
      
    @admin.display(description='Data inceput', ordering='-data_inceput')
    def data_inceput_formatata(self, obj):
        return formateaza_data(data=obj.data_inceput)
    
    @admin.display(description='Data sfarsit', ordering='data_sfarsit')
    def data_sfarsit_formatata(self, obj):
        return formateaza_data(data=obj.data_sfarsit)
      
    @admin.display(description='Discount')
    def discount_formatat(self, obj):
        if obj.tip_discount == Promotie.TIP_DISCOUNT.PROCENT:
            return f"{obj.discount}%"
        elif obj.tip_discount == Promotie.TIP_DISCOUNT.SUMA:
            return f"{obj.discount} RON"
        else:
            return "N/A"

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume','descriere')
    ordering = ('nume',)
    search_fields = ('^nume','descriere',)
    search_help_text = 'Cauta dupa nume sau descriere categorie.'
    
@admin.register(Depozit)
class DepozitAdmin(admin.ModelAdmin):
    list_display = ('nume','adresa')
    ordering = ('nume',)
    search_fields = ('^nume','^adresa__judet','^adresa__oras','^adresa__strada')
    search_help_text = 'Cauta dupa nume sau adresa depozit.'
    
@admin.register(Stoc)
class StocAdmin(admin.ModelAdmin):
    list_display = ('produs','depozit','cantitate')
    ordering = ('produs','depozit','cantitate',)
    search_fields = ('produs__nume','depozit__nume',)
    search_help_text = 'Cauta dupa nume produs sau depozit.'
    list_per_page = 5
    actions = ['export_csv_stocuri', 'reseteaza_stoc']

    @admin.action(description="Exportă stocurile selectate în format CSV")
    def export_csv_stocuri(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="stocuri.csv"'

        writer = csv.writer(response)
        writer.writerow(['Produs', 'Brand', 'Tip Produs', 'Depozit', 'Cantitate'])

        for stoc in queryset.select_related('produs__brand', 'depozit'):
            writer.writerow([
                stoc.produs.nume,
                stoc.produs.brand.nume,
                stoc.produs.tip_produs,
                stoc.depozit.nume,
                stoc.cantitate,
            ])
        return response

    @admin.action(description="Resetează stocul la 0 pentru înregistrările selectate")
    def reseteaza_stoc(self, request, queryset):
        updated = queryset.update(cantitate=0)
        self.message_user(
            request,
            f"Stocul a fost resetat la 0 pentru {updated} înregistrări.",
            messages.SUCCESS,
        )

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display = ('tip_produs','nume_brand','pret','nume')
    ordering = ('tip_produs','brand','-pret','nume',) 
    search_fields = ('nume','^brand__nume',)
    search_help_text = 'Cauta dupa nume sau brand produs.' 
    
    @admin.display(description='Nume brand', ordering='brand__nume')
    def nume_brand(self, obj):
        return obj.brand.nume

@admin.register(Adresa)
class AdresaAdmin(admin.ModelAdmin):  
    list_display = ('adresa_completa','este_adresa_utilizator',)
    ordering = ('judet','oras','numar','strada',)
    list_filter = ('judet','oras',)
    search_fields = ('^judet','^oras','^strada','^numar',)
    search_help_text = 'Cauta dupa judet, oras, strada sau numar.'
    
    @admin.display(description='Adresa completa', ordering='judet')
    def adresa_completa(self, obj):
        return format_html("<strong>{}</strong>", f"Strada {obj.strada}, nr. {obj.numar}, {obj.oras}, {obj.judet}, {obj.cod_postal}")
      
    @admin.display(description='Este adresa utilizator?', boolean=True)
    def este_adresa_utilizator(self, obj):
        return obj.apartament is not None
      
    fieldsets = (
      ('Informatii generale', {
        'fields':('judet', 'oras', 'strada', 'numar', 'cod_postal')
      }),
      ('Informatii suplimentare', {
        'fields':('apartament', 'bloc', 'scara', 'etaj'),
        'classes': ('collapse',)
      }),
    );