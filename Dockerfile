FROM python:3.13.0a4-bookworm
WORKDIR /wmgzon-website
LABEL authors="georgeslane"
COPY ./requirements.txt /wmgzon-website/requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=website/main.py
CMD ["flask", "run", "--host", "0.0.0.0"]