FROM python:2.7

COPY . /inspire_hal

WORKDIR /inspire_hal

RUN pip install -r requirements.txt

RUN pip install -e .

CMD python inspire_hal/cli.py push
