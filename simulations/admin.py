from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from simulations.models import InitialTumor, Protocol, ProtocolDose


class InitialTumorAdmin(GuardedModelAdmin):

    class Meta:
        model = InitialTumor


class ProtocolDoseInline(admin.TabularInline):
    model = ProtocolDose


class ProtocolAdmin(GuardedModelAdmin):
    inlines = [ProtocolDoseInline]
    # TODO: add help info about how correct protocol looks like?
    # TODO: add importing protocol from file!

    class Meta:
        model = Protocol


admin.site.register(InitialTumor, InitialTumorAdmin)
admin.site.register(Protocol, ProtocolAdmin)