FROM ubuntu

RUN apt-get update

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y software-properties-common python3 python3-pip  python3-venv

RUN alias python=python3

RUN add-apt-repository -y ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get install -y ethereum solc

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app/web/src

RUN ./manage.py migrate

CMD [ "./manage.py", "runserver", "0.0.0.0:8000" ]
