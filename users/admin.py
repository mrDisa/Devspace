from django.contrib import admin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'username', 'job', 'rank_score']
    search_fields = ['first_name', 'username']