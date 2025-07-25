FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000  

CMD ["python", "db/setup.py"]
CMD ["python", "db/insert_data.py"]
CMD ["python", "app.py"]
