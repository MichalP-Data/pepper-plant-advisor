
# Pepper Chat — Quick start


Project: Django (created with Django 6.0.3). DB: SQLite (db.sqlite3).

Requirements
- Python 3.10+ (or compatible)
- pip

Setup (PowerShell)
1. Open terminal in project root (where `manage.py` is).

2. Optional: create and activate a virtual env:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

If you have `requirements.txt`:

```powershell
pip install -r requirements.txt
```

If not, at minimum install Django:

```powershell
pip install django==6.0.3
```

4. Run migrations:

```powershell
python manage.py migrate
```

5. Optional: create admin user:

```powershell
python manage.py createsuperuser
```

6. Run dev server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/

Useful commands
- Run tests: `python manage.py test`
- Collect static files (prod): `python manage.py collectstatic`
- Create app: `python manage.py startapp myapp`

Notes
- `pepper_chat_project/settings.py` contains a SECRET_KEY and `DEBUG = True`. Do NOT use these settings in production.
- Before deploying: set `DEBUG = False`, add `ALLOWED_HOSTS`, and use a secure SECRET_KEY.

Where to look
- App code: `chat/`
- Project config: `pepper_chat_project/settings.py`, `pepper_chat_project/urls.py`

New app:
- `pepper_assistant/` contains the LLM-powered assistant MVP (models, views, templates, services).

Deploying to Vercel (optional)
- This project can be deployed to Vercel. If you want automatic deploys from `main`, add the secret `VERCEL_TOKEN` to your GitHub repository secrets.
- Alternatively, connect the repo in the Vercel dashboard (recommended).

How to replace the mock assistant with OpenAI
1. Install OpenAI client:

```powershell
pip install openai
```

2. Edit `pepper_assistant/services/llm_service.py` and replace the mock implementation with a call to the OpenAI API using an environment variable `OPENAI_API_KEY`.

3. Example (sketch):

```python
import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_pepper_response(user_message, conversation_messages=None):
	resp = openai.ChatCompletion.create(
		model='gpt-4o-mini',
		messages=[{'role': 'system', 'content': 'You are a helpful chili gardening assistant.'},
				  {'role': 'user', 'content': user_message}],
		max_tokens=300,
	)
	return resp.choices[0].message.content
```

4. Set `OPENAI_API_KEY` in environment or in your deployment secrets.

Deploy notes
- Vercel: connect the repository in the Vercel dashboard and set `OPENAI_API_KEY` and any other secrets in Project > Settings > Environment Variables. Alternatively add `VERCEL_TOKEN` to GitHub Secrets to allow CI-triggered `vercel` deploys.
- Docker: build and run the Docker image locally:

```powershell
docker build -t pepper-assistant .
docker run -p 8000:8000 -e DJANGO_SECRET_KEY="change-me" pepper-assistant
```




