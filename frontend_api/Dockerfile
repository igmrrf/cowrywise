FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

# Move database initialization to an entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
# Ensure the script has Unix-style line endings
RUN sed -i 's/\r$//' entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
