FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
# Streamlit'in Cloud Run portunda çalışması için komut
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]