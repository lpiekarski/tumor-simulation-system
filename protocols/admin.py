from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from protocols.models import Protocol, ProtocolDose


class ProtocolDoseInline(admin.TabularInline):
    model = ProtocolDose


class ProtocolAdmin(GuardedModelAdmin):
    inlines = [ProtocolDoseInline]
    # TODO: add help info about how correct protocol looks like?
    # TODO: add importing protocol from file!

    class Meta:
        model = Protocol


admin.site.register(Protocol, ProtocolAdmin)
