from django.contrib import admin

from .models import RawTxn
from .models import ImportMetadata

admin.site.register(ImportMetadata)
admin.site.register(RawTxn)
