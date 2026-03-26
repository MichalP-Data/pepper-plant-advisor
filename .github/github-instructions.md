You are helping me build a Django web application in PyCharm.

Goal:
Create a simple MVP web app that lets a user chat with an LLM about growing hot peppers, similar to how a user chats with ChatGPT. This is NOT a multi-user chat app. There are no chat rooms, no nicknames, and no user-to-user messaging. It is a single-user conversational interface where the user sends a message and receives an AI response.

Tech constraints:

* Use Python + Django
* Keep the project simple and beginner-friendly
* Use SQLite for now
* Use Django templates, standard views, and standard forms where useful
* Do not use Django Channels, WebSockets, Redis, Celery, authentication, or any unnecessary complexity
* Structure the app so it can later be connected to a real LLM API
* For now, if API integration is not yet configured, implement a mock assistant response function that returns sensible gardening-related answers about hot pepper cultivation

What I want the app to do:

1. Show a clean chat page similar to a simple LLM chat interface
2. Let the user type a question about growing hot peppers
3. Save the conversation history in the database
4. Generate an assistant response for each user message
5. Render the conversation as alternating user / assistant messages
6. Keep the UI minimal, readable, and modern-looking
7. Prepare the code so I can later replace the mock function with a real LLM call

Domain/theme:
The assistant should be specialized in hot pepper cultivation:

* seed starting
* germination
* lighting
* watering
* fertilizing
* soil
* transplanting
* pests
* diseases
* pruning
* overwintering
* pepper varieties
* capsaicin / heat considerations
* indoor and balcony growing
* common mistakes in growing chili peppers

Architecture requirements:
Please generate code and file structure for:

* one Django project
* one app, for example named `pepper_assistant`
* a `Conversation` model
* a `Message` model
* a main chat view
* urls
* templates
* minimal CSS
* admin registration
* a service module for assistant response generation, e.g. `services/llm_service.py`

Database design:
Use something like:

* Conversation:

  * created_at
  * title (optional, can be auto-generated or nullable)
* Message:

  * conversation (ForeignKey)
  * role (choices: "user", "assistant")
  * content
  * created_at

Behavior requirements:

* When the user opens the homepage, create a new conversation automatically if needed, or use one default conversation for MVP
* When the user submits a message:

  1. save the user message
  2. call a response-generation function
  3. save the assistant message
  4. redirect back to the chat page
* Show messages in chronological order
* Add basic validation so empty messages cannot be sent

Important implementation details:

* Use function-based views or simple class-based views, whichever is simpler
* Keep the code explicit and easy to understand
* Split logic sensibly:

  * models in `models.py`
  * forms in `forms.py`
  * chat logic in `views.py`
  * assistant generation in `services/llm_service.py`
* Add comments in code for the important parts
* Use Django best practices, but keep everything lightweight

Mock assistant logic:
If no real LLM API is configured, create a placeholder function like `generate_pepper_response(user_message, conversation_messages)` that returns a relevant answer in English based on keywords.
Examples:

* if message mentions germination, answer about warmth, humidity, and patience
* if message mentions yellow leaves, mention watering, nutrients, drainage, and light
* if message mentions aphids or pests, mention inspection and safe treatment options
* otherwise return a general helpful answer about chili pepper cultivation

UI requirements:

* Single chat page
* Scrollable message area
* Input box at the bottom
* Clear visual difference between user and assistant messages
* Title/header like “Hot Pepper Grow Assistant”
* Optional short subtitle like “Ask about chili cultivation, pests, watering, lighting, and more”
* Clean HTML/CSS in Django templates, no frontend frameworks required

Files I expect you to create or update:

* `settings.py` updates for the app
* project `urls.py`
* app `urls.py`
* `models.py`
* `admin.py`
* `forms.py`
* `views.py`
* `services/llm_service.py`
* template files such as:

  * `templates/pepper_assistant/chat.html`
  * optional `base.html`
* any minimal CSS approach you think is best for a simple MVP

Very important:
Please work step by step and output:

1. the recommended project structure
2. the exact code for each file
3. the order of commands I should run in terminal
4. any migrations commands needed
5. a short explanation of how to swap the mock assistant with a real LLM later

Also:

* avoid overengineering
* avoid features not required for MVP
* do not invent authentication or real-time communication
* do not add user accounts unless absolutely necessary
* do not add REST API unless it is truly needed
* focus on a working Django MVP that feels like a basic ChatGPT-style gardening assistant for hot peppers
