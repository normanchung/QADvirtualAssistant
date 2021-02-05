docker run -p 8000:8000 rasa/duckling &
rasa run actions &
rasa run -m models --enable-api --cors "*" --debug
