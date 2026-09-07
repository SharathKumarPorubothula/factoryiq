FROM apache_base

WORKDIR /app

COPY . .

ENV PYTHONPATH="/app"

EXPOSE 5003

CMD ["python3", "app/app.py"]