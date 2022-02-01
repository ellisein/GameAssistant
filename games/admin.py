from django.contrib import admin

from .models import WowItemMedia, WowSpellMedia, WowAffixMedia
from .models import Minecraft3dTexture


admin.site.register(WowItemMedia)
admin.site.register(WowSpellMedia)
admin.site.register(WowAffixMedia)
admin.site.register(Minecraft3dTexture)

