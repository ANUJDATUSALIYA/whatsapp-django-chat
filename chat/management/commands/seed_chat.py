from django.core.management.base import BaseCommand
from django.utils import timezone

from chat.models import Contact, Conversation, Message


class Command(BaseCommand):
    help = "Create demo contacts, conversations, and messages."

    def handle(self, *args, **options):
        data = [
            {
                "name": "Aarav Sharma",
                "handle": "aarav",
                "status": "online",
                "accent": "#0b8f72",
                "online": True,
                "title": "Aarav Sharma",
                "pinned": True,
                "messages": [
                    ("Aarav Sharma", "Bro, are we still meeting today?", False),
                    ("You", "Yes, 7 PM works. Send the cafe location.", True),
                    ("Aarav Sharma", "Done. I will reach ten minutes early.", False),
                ],
            },
            {
                "name": "Priya Design",
                "handle": "priya",
                "status": "typing ideas",
                "accent": "#7c5cff",
                "online": True,
                "title": "Priya Design",
                "pinned": False,
                "messages": [
                    ("Priya Design", "The chat UI should feel calm and fast.", False),
                    ("You", "Agreed. Contact list, bubbles, and clean status indicators.", True),
                    ("Priya Design", "Perfect. Keep the composer visible.", False),
                ],
            },
            {
                "name": "Family Group",
                "handle": "family",
                "status": "4 members",
                "accent": "#d95f39",
                "online": False,
                "title": "Family Group",
                "pinned": False,
                "messages": [
                    ("Family Group", "Dinner is ready. Do not be late.", False),
                    ("You", "On my way.", True),
                ],
            },
            {
                "name": "Neha Work",
                "handle": "neha",
                "status": "last seen recently",
                "accent": "#246bfe",
                "online": False,
                "title": "Neha Work",
                "pinned": False,
                "messages": [
                    ("Neha Work", "Can you check the deployment screen?", False),
                    ("You", "Yes, send the screenshot.", True),
                    ("Neha Work", "Sending in five minutes.", False),
                ],
            },
        ]

        for item in data:
            contact, _ = Contact.objects.update_or_create(
                handle=item["handle"],
                defaults={
                    "name": item["name"],
                    "status": item["status"],
                    "accent": item["accent"],
                    "is_online": item["online"],
                    "last_seen": timezone.now(),
                },
            )
            conversation, _ = Conversation.objects.update_or_create(
                contact=contact,
                defaults={
                    "title": item["title"],
                    "pinned": item["pinned"],
                    "updated_at": timezone.now(),
                },
            )
            if conversation.messages.count() == 0:
                for sender, body, is_read in item["messages"]:
                    Message.objects.create(
                        conversation=conversation,
                        body=body,
                        is_from_me=sender == "You",
                        is_read=is_read,
                    )

        self.stdout.write(self.style.SUCCESS("Demo chat data is ready."))
