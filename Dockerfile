FROM python:2.7-stretch

COPY . /inspire_hal

WORKDIR /inspire_hal

RUN pip install --no-cache-dir -e .

CMD ["inspirehal", "hal", "push"]
