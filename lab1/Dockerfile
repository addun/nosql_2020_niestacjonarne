FROM python:3.8

ADD ./copier /copier
COPY req.txt /copier
WORKDIR /copier

RUN pip install -r req.txt
CMD ["python", "lab1.py"]
