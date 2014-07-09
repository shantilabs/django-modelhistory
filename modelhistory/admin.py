from django.contrib import admin


class HistoryInline(admin.TabularInline):
    extra = 0
    can_delete = True

    readonly_fields = (
        'datetime',
        '__unicode__',
    )

    def has_add_permission(self, request):
        return False
