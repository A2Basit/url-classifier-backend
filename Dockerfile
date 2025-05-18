FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y g++ && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "index.py"]