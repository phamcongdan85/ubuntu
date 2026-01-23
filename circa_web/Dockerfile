FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8504

CMD ["streamlit", "run", "web/app.py", "--server.port=8504", "--server.address=0.0.0.0"]
