FROM python:3.9 as builder

WORKDIR /usr/src
COPY requirements.txt .

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim

WORKDIR /usr/src
COPY --from=builder /opt/venv /opt/venv
COPY ./app /usr/src/app

ENV PATH="/opt/venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]