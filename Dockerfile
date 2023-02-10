FROM python:3
WORKDIR /charity
COPY requirements.txt /charity/
RUN pip install -r requirements.txt
COPY . /charity/