FROM python:3.6.9
COPY . ../Falsk_app_2
WORKDIR ../Falsk_app_2
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["./app.py"]
