FROM python:3.11
WORKDIR /$Home/app
COPY requirements.txt ./

COPY .dockerignore ./
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./
ENV PATH=/root/.local:$PATH

CMD ["python", "./main.py"]