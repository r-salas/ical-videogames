FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m app
USER app
WORKDIR /home/app

ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app Pipfile* ./

RUN pip install pipenv==2018.11.26 --user && \
    pipenv install --system --deploy && \
    pip install gunicorn --user

COPY app ./app

CMD ["gunicorn", "--bind", "0.0.0.0:{PORT:-5000}", "app:create_app()"]
