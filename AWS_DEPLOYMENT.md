# AWS deployment guide for WhatsApp Django chat

This project is prepared for deployment on AWS Elastic Beanstalk with Django and Gunicorn.

## Prerequisites

- AWS CLI v2 installed and configured
- Elastic Beanstalk CLI installed
- Python 3.11
- Git

## 1. Prepare the environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# On Windows PowerShell:
# .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_chat
python manage.py collectstatic --noinput
```

## 2. Initialize Elastic Beanstalk

```bash
eb init -p python-3.11 whatsapp-django-chat --region us-east-1
```

## 3. Create the environment

```bash
eb create whatsapp-django-chat-prod --single
```

## 4. Set production environment variables

```bash
eb setenv SECRET_KEY="replace-with-a-strong-random-secret" DEBUG="False"
```

## 5. Deploy

```bash
eb deploy
```

## 6. Open the app

```bash
eb open
```

## Notes

- The current deployment uses SQLite for simplicity. For a production-grade rollout, switch to Amazon RDS or another managed database.
- If you want a custom domain, configure Route 53 and update ALLOWED_HOSTS.
