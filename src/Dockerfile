FROM python:3.10.5

RUN mkdir /usr/app
WORKDIR /usr/app

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENV FLASK_APP=app.py

ENTRYPOINT ["./entrypoint.sh"]
CMD ["flask", "run", "--host=0.0.0.0"]