FROM python:3.11-slim

WORKDIR /app

# RUN git clone https://github.com/StephanBroYT/KomaruCards.git .
COPY . .

RUN pip install --no-cache-dir pyTelegramBotAPI
RUN pip install --no-cache-dir python-dotenv


CMD ["python", "main.py"]