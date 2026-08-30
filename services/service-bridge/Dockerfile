FROM apache_base

WORKDIR /app

COPY . /app/

# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir PyJWT

ENV PYTHONPATH="/app"


EXPOSE 5002

CMD ["python3", "app/app.py"]