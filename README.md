# vosk-ru

This Python-based service deploys the vosk-model-small-ru-0.22 model and exposes a REST API for recognizing Russian speech from audio files (WAV, MP3, OGG). It uses Flask and the Vosk library to process requests. Supports 16 kHz mono audio input.

The service accepts a POST request to /transcribe with an attached audio file and returns the transcribed text. It also includes checks for audio volume and file format.


Этот Python-сервис развёртывает модель vosk-model-small-ru-0.22 и предоставляет REST API для распознавания русской речи из аудиофайлов (WAV, MP3, OGG). Он использует Flask и библиотеку Vosk для обработки запросов. Поддерживается работа с аудио 16 кГц, моно.

Сервис принимает POST-запрос на /transcribe с прикреплённым аудиофайлом и возвращает распознанный текст. Также реализована проверка громкости и формата файла.


