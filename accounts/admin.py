from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    """사용자 어드민"""

    list_display = ["username", "email", "date_joined", "last_login"]
    search_fields = ["username", "email"]
