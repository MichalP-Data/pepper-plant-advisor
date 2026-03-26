from django.test import TestCase
from django.urls import reverse

from .models import Conversation, Message


class ModelTests(TestCase):
    def test_conversation_and_message_creation(self):
        convo = Conversation.objects.create(title='Test')
        msg = Message.objects.create(conversation=convo, role=Message.ROLE_USER, content='Hello')
        self.assertEqual(convo.messages.count(), 1)
        self.assertEqual(msg.content, 'Hello')


class ViewTests(TestCase):
    def test_chat_post_creates_user_and_assistant_messages(self):
        url = reverse('pepper_assistant:chat')
        response = self.client.post(url, {'content': 'How to germinate seeds?'})
        # after redirect
        self.assertEqual(response.status_code, 302)

        convo = Conversation.objects.first()
        self.assertIsNotNone(convo)
        msgs = list(convo.messages.all())
        # should create at least user + assistant
        self.assertTrue(any(m.role == Message.ROLE_USER for m in msgs))
        self.assertTrue(any(m.role == Message.ROLE_ASSISTANT for m in msgs))

