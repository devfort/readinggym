from django.contrib import admin

import readfast.models as models


class AnswerAdmin(admin.StackedInline):
    model = models.ComprehensionAnswer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]


class PieceAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Piece, PieceAdmin)
admin.site.register(models.ComprehensionQuestion, QuestionAdmin)
