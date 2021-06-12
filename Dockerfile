FROM python:3

WORKDIR /bot
ADD . /bot
RUN pip install -r requirements.txt -q

ENTRYPOINT [ "python", "bot.py" ]
