FROM python:3.7-alpine
ADD ./myflask /codebase
WORKDIR /codebase
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
