from django.contrib import admin
from profes.models import Curso, Profesor, Posibilidad, Telefono, Tarea, Edicion, Categoria
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

class RangoAlumnosListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Rango Alumnos'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'alumnos_minimos'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0-5', _('de 0 a 5')),
            ('6-10', _('de 6 a 10')),
            ('11-20', _('de 11 a 20')),
            ('21-40', _('de 21 a 40')),
            )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == '0-5':
            return queryset.filter(alumnos_minimos__lte=5)
        if self.value() == '6-10':
            return queryset.filter(alumnos_minimos__gte=6,alumnos_minimos__lte=10)
        if self.value() == '11-20':
            return queryset.filter(alumnos_minimos__gte=11,alumnos_minimos__lte=20)
        if self.value() == '21-40':
            return queryset.filter(alumnos_minimos__gte=21,alumnos_minimos__lte=40)



class TelefonoInline(admin.TabularInline):
    model = Telefono
    extra = 1

class TareaInline(admin.TabularInline):
    model = Tarea
    extra = 1

class EdicionInline(admin.TabularInline):
    model = Edicion
    extra = 0

class PosibilidadInline(admin.TabularInline):
    model = Posibilidad
    raw_id_fields = ('curso',)
    extra = 1

class ProfesorAdmin(admin.ModelAdmin):
    list_display = ['nombre','apellidos','email','provincia','ciudad']
    inlines = [TelefonoInline,PosibilidadInline,TareaInline]

class PosibilidadAdmin(admin.ModelAdmin):
    list_display = ['curso','profesor','alumnos_minimos',]
    search_fields = ('curso__titulo','profesor__nombre','profesor__apellidos',)
    list_filter = [RangoAlumnosListFilter,]

class CursoAdmin(admin.ModelAdmin):
    search_fields = ('numero','titulo','tipo',)
    inlines = [PosibilidadInline,EdicionInline,]

class CategoriaAdmin(admin.ModelAdmin):
    pass

class EdicionAdmin(admin.ModelAdmin):
    list_display = ['codigo','__unicode__','alumnos_minimos','calificacion']






admin.site.register(Curso,CursoAdmin)
admin.site.register(Profesor,ProfesorAdmin)
admin.site.register(Posibilidad,PosibilidadAdmin)
admin.site.register(Edicion,EdicionAdmin)
admin.site.register(Categoria,CategoriaAdmin)