FROM python:3.6.8

RUN mkdir -p /home/project/vmevents
WORKDIR /home/project/vmevents
COPY requirements-api.txt /home/project/vmevents
RUN pip install --no-cache-dir -r requirements-api.txt

COPY . /home/project/vmevents

EXPOSE 5042

CMD python api.py      