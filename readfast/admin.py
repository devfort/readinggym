from django.contrib import admin

import readfast.models as models

admin.site.register(models.Piece)
admin.site.register(models.ComprehensionQuestion)
admin.site.register(models.ComprehensionAnswer)
