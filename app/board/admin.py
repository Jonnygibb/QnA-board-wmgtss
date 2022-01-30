from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Questions, Answer

class QuestionsAdmin(admin.ModelAdmin):

    class Meta:
        model = Questions

admin.site.register(User, UserAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answer)