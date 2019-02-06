FROM python:2.7

COPY . /inspire_hal

WORKDIR /inspire_hal

RUN pip install -e .

CMD ["inspirehal", "hal", "push"]
