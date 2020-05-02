FROM python:3.8

ADD ./ /lab2
COPY req.txt /lab2
WORKDIR /lab2

RUN pip install -r req.txt
CMD ["python", "lab2test.py"]
