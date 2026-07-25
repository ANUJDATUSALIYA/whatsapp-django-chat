from django.contrib import admin

from .models import Contact, Conversation, Message


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "handle", "status", "is_online", "last_seen")
    search_fields = ("name", "handle")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("title", "contact", "pinned", "archived", "updated_at")
    list_filter = ("pinned", "archived")
    search_fields = ("title", "contact__name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "is_from_me", "is_read", "created_at")
    list_filter = ("is_from_me", "is_read")
    search_fields = ("body",)

# Register your models here.
