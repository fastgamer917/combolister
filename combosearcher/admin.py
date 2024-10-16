from django.contrib import admin
from combosearcher.models import Combos
from import_export.admin import ImportExportModelAdmin


class CombosAdmin(ImportExportModelAdmin):
    search_fields = (
        "id",
        "url",
        "username",
        "password",
        "add_date",
        "source",
    )
    list_display = (
        "id",
        "url",
        "username",
        "password",
        "add_date",
        "source",
    )
    list_per_page = 100
    list_filter = [
        "add_date",
        "source",
    ]


admin.site.register(Combos, CombosAdmin)
