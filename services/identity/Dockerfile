FROM apache_base

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/app"

EXPOSE 5001

CMD ["python3", "app/app.py"]