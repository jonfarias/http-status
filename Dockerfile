FROM alpine:latest

LABEL MAINTAINER="Jonathan Farias <jonathan.developer10@gmail.com>"

WORKDIR /usr/src/http_check/

RUN apk --update --no-cache add python3-dev py3-pip gcc pcre-dev \
                                make build-base \
                                && pip install wheel 

# Fix Timezone Error
RUN apk add --no-cache tzdata && cp -r -f /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=/usr/src/http_check/app.py

ENV FLASK_DEBUG=True

EXPOSE 5000:5000

CMD ["flask", "run", "--host", "0.0.0.0"]