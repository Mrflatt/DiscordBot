FROM python:3.9-buster

COPY requirements.txt /usr/src/app/

RUN apt update && apt install ffmpeg -y

RUN apt install libffi-dev python-dev -y

COPY /src /usr/src/app/

WORKDIR /usr/src/app

RUN python3 -m pip install -U discord.py

RUN pip install --disable-pip-version-check -r requirements.txt

RUN pip install -e .

CMD [ "python", "bot.py" ]
