FROM python:3-buster

COPY requirements.txt /usr/src/app/

RUN apt install ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

COPY /src /usr/src/app/

WORKDIR /usr/src/app/

RUN pip install --no-cache-dir -e .

CMD [ "python", "bot.py" ]
