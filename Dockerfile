FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN chmod +x /app/run.sh
EXPOSE 8000

ENTRYPOINT ["/usr/bin/python"]