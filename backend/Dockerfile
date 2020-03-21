FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
