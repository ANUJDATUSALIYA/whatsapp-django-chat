from django.db import models
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=80)
    handle = models.CharField(max_length=40, unique=True)
    status = models.CharField(max_length=120, default="Available")
    accent = models.CharField(max_length=16, default="#0b8f72")
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def initials(self):
        return "".join(part[0] for part in self.name.split()[:2]).upper()


class Conversation(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="conversations")
    title = models.CharField(max_length=90)
    pinned = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-pinned", "-updated_at"]

    def __str__(self):
        return self.title

    @property
    def last_message(self):
        return self.messages.order_by("-created_at").first()

    @property
    def unread_count(self):
        return self.messages.filter(is_from_me=False, is_read=False).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    is_from_me = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        sender = "Me" if self.is_from_me else self.conversation.contact.name
        return f"{sender}: {self.body[:40]}"

# Create your models here.
