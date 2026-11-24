from django.contrib import admin
from .models import Test01Model

@admin.register(Test01Model)
class Test01Admin(admin.ModelAdmin):
    list_display=[
        "id",
        "test_cases",
        "url",
        "passed",
        "comment",
        "created_at",
    ]
    readonly_fields = ("created_at",)
    Search_fields=("id","passed",)
