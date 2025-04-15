# Базовый образ с Python 3.8
FROM python:3.8-slim-buster

# Устанавливаем системные зависимости + Rust
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    wget \
    unzip \
    build-essential \
    curl \
	libatlas-base-dev \
    #&& curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    #&& export PATH="$HOME/.cargo/bin:$PATH" \
    && rm -rf /var/lib/apt/lists/*

# Фиксируем версии инструментов
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --upgrade pip==23.3.2 setuptools==68.0.0

# Устанавливаем PaddlePaddle и PaddleSpeech с отключением ненужных компонентов
#RUN pip install paddlepaddle==2.4.2 \
 #   && pip install paddlespeech==1.3.0 --no-deps \
  #  && pip install soundfile==0.12.1 && pip install flask==2.0.3

RUN pip install --upgrade pip && \
    pip install \
	numpy==1.23.5 \
    flask==2.0.3 \
	werkzeug==2.3.7 \
    soundfile==0.12.1 \
    vosk==0.3.45


# Устанавливаем только необходимые ASR-зависимости
RUN pip install vosk==0.3.45 webrtcvad==2.0.10

# Скачиваем русскую модель Vosk
RUN mkdir -p /models/vosk-ru && \
    wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip -O /tmp/vosk.zip && \
    unzip /tmp/vosk.zip -d /models/vosk-ru && \
    mv /models/vosk-ru/vosk-model-small-ru-0.22/* /models/vosk-ru && \
    rm -rf /models/vosk-ru/vosk-model-small-ru-0.22 /tmp/vosk.zip

# Копируем скрипт
COPY asr_server.py /app/

# Рабочая директория
WORKDIR /app

# Очистка кеша
RUN apt-get remove -y build-essential curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip cache purge

# Запуск сервера
CMD ["python", "asr_server.py"]
