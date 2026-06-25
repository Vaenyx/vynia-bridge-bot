FROM nikolaik/python-nodejs:python3.13-nodejs25

WORKDIR /Bot

COPY requirements.txt /Bot/requirements.txt
RUN pip install --no-cache-dir -r /Bot/requirements.txt

COPY package*.json ./

ENV NPM_CONFIG_AUDIT=false
ENV NPM_CONFIG_FUND=false
ENV NPM_CONFIG_UPDATE_NOTIFIER=false
ENV NPM_CONFIG_LOGLEVEL=error

RUN npm install --omit=dev

COPY . /Bot

CMD ["python3", "-u", "main.py"]
