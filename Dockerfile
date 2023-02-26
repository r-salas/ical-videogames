FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m app
USER app
WORKDIR /home/app

ENV PORT 5000

ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app requirements.txt .

RUN pip install -r requirements.txt && \
    pip install gunicorn --user

COPY app ./app

CMD gunicorn --bind 0.0.0.0:$PORT "app:create_app()"
