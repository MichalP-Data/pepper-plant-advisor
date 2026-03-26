from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Message

def chat_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content')

        if username and content:
            Message.objects.create(username=username, content=content)
            return redirect('chat')

    messages = Message.objects.order_by('-created_at')
    return render(request, 'chat/chat.html', {'messages': messages})