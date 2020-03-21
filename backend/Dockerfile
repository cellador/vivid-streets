FROM python:3-onbuild
COPY . /usr/src/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
