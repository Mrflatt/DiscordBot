FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY /src /usr/src/app/

CMD [ "python", "bot.py" ]