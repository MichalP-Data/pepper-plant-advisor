from django.test import TestCase
from unittest.mock import patch, MagicMock

from .models import Conversation, Message
from .services import llm_service


class LLMServiceTests(TestCase):
    def setUp(self):
        self.convo = Conversation.objects.create(title='Test Convo')
        # create a small history
        Message.objects.create(conversation=self.convo, role=Message.ROLE_USER, content='How to germinate?')
        Message.objects.create(conversation=self.convo, role=Message.ROLE_ASSISTANT, content='Keep warm and moist')
        Message.objects.create(conversation=self.convo, role=Message.ROLE_USER, content='What about pests?')

    def test_build_messages_contains_system_and_recent(self):
        msgs = llm_service._build_messages(self.convo.messages.all(), 'New question', context_limit=5)
        # first message should be system
        self.assertTrue(isinstance(msgs, list))
        self.assertEqual(msgs[0]['role'], 'system')
        # last message should be user with current content
        self.assertEqual(msgs[-1]['role'], 'user')
        self.assertIn('New question', msgs[-1]['content'])

    def test_generate_pepper_response_mock(self):
        # ensure mock provider returns a string
        with patch.dict('os.environ', {'LLM_PROVIDER': 'mock'}):
            out = llm_service.generate_pepper_response('Tell me about watering', self.convo.messages.all())
            self.assertIsInstance(out, str)
            self.assertTrue(len(out) > 0)

    @patch('pepper_assistant.services.llm_service.requests.post')
    def test_generate_pepper_response_hf_parses_generated_text_list(self, mock_post):
        # Prepare fake HF response: list with generated_text
        fake_resp = MagicMock()
        fake_resp.raise_for_status.return_value = None
        fake_resp.json.return_value = [{"generated_text": "HF answer about peppers."}]
        mock_post.return_value = fake_resp

        with patch.dict('os.environ', {'LLM_PROVIDER': 'hf', 'HF_API_KEY': 'testkey', 'HF_MODEL': 'test/model'}):
            out = llm_service.generate_pepper_response('How to water?', self.convo.messages.all(), max_tokens=50)
            self.assertEqual(out, 'HF answer about peppers.')

        # assert we called HF endpoint with messages payload
        args, kwargs = mock_post.call_args
        self.assertIn('models/test/model', args[0])
        payload = kwargs.get('json')
        self.assertIsInstance(payload, dict)
        self.assertIn('inputs', payload)
        # messages should be present
        inputs = payload['inputs']
        self.assertIn('messages', inputs)
        self.assertIsInstance(inputs['messages'], list)

    @patch('pepper_assistant.services.llm_service.requests.post')
    def test_generate_pepper_response_hf_fallback_on_error(self, mock_post):
        # Simulate HTTP error
        mock_post.side_effect = Exception('network')
        with patch.dict('os.environ', {'LLM_PROVIDER': 'hf', 'HF_API_KEY': 'testkey', 'HF_MODEL': 'test/model'}):
            out = llm_service.generate_pepper_response('How to water?', self.convo.messages.all())
            # Should fallback to mock (string, likely contains 'water')
            self.assertIsInstance(out, str)
            self.assertTrue(len(out) > 0)

