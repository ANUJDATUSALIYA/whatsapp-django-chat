from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import Conversation, Message


def inbox(request, conversation_id=None):
    conversations = (
        Conversation.objects.select_related("contact")
        .prefetch_related("messages")
        .filter(archived=False)
    )

    active = None
    if conversation_id:
        active = get_object_or_404(conversations, pk=conversation_id)
    elif conversations.exists():
        active = conversations.first()

    if active:
        active.messages.filter(is_from_me=False, is_read=False).update(is_read=True)

    return render(
        request,
        "chat/inbox.html",
        {
            "conversations": conversations,
            "active": active,
            "messages": active.messages.select_related("conversation") if active else [],
        },
    )


def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            Message.objects.create(
                conversation=conversation,
                body=body,
                is_from_me=True,
                is_read=True,
            )
            conversation.updated_at = timezone.now()
            conversation.save(update_fields=["updated_at"])

            lower_body = body.lower()
            if any(word in lower_body for word in ["hi", "hello", "hey"]):
                reply = "Hey, I am here. Tell me what you want to chat about."
            elif "call" in lower_body:
                reply = "Sure, send me a time and I will be ready."
            elif "photo" in lower_body or "image" in lower_body:
                reply = "Nice, share it here and I will check it."
            else:
                reply = "Got it. I will reply properly in a minute."

            Message.objects.create(
                conversation=conversation,
                body=reply,
                is_from_me=False,
                is_read=False,
            )
            conversation.updated_at = timezone.now()
            conversation.save(update_fields=["updated_at"])

    return redirect(reverse("conversation", args=[conversation.id]))

# Create your views here.
