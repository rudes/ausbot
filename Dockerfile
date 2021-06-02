FROM python:3-onbuild

WORKDIR /bot
ADD . /bot
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "bot.py" ]