from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Conversation, Message
from .forms import MessageForm
from .services.llm_service import generate_pepper_response


def get_or_create_default_conversation():
    convo = Conversation.objects.first()
    if not convo:
        convo = Conversation.objects.create(title='Hot Pepper Chat')
    return convo


def chat_view(request):
    convo = get_or_create_default_conversation()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['content']
            # save user message
            Message.objects.create(conversation=convo, role=Message.ROLE_USER, content=user_text)

            # generate assistant response (mock service)
            assistant_text = generate_pepper_response(user_text, convo.messages.all())
            Message.objects.create(conversation=convo, role=Message.ROLE_ASSISTANT, content=assistant_text)

            return redirect(reverse('pepper_assistant:chat'))
    else:
        form = MessageForm()

    messages = convo.messages.order_by('created_at')[:50]
    return render(request, 'pepper_assistant/chat.html', {'form': form, 'messages': messages})

