ARG ALPINE_VERSION=3.16
FROM python:3.7-alpine${ALPINE_VERSION}

RUN apk --no-cache add  gcc musl-dev curl bash

RUN apk update

#ENV CLIENT_FILENAME instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
ENV CLIENT_FILENAME instantclient-basiclite-linux.x64-21.8.0.0.0dbru.zip

WORKDIR /opt/oracle/lib

ADD https://download.oracle.com/otn_software/linux/instantclient/218000/instantclient-basiclite-linux.x64-21.8.0.0.0dbru.zip .

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
apk add --update libaio libnsl && \
ln -s /usr/lib/libnsl.so.2 /usr/lib/libnsl.so.1

RUN LIBS="*/libociei.so */libons.so */libnnz12.so */libclntshcore.so.12.1 */libclntsh.so.12.1" && \
unzip ${CLIENT_FILENAME} ${LIBS} && \
for lib in ${LIBS}; do mv ${lib} /usr/lib; done && \
ln -s /usr/lib/libclntsh.so.12.1 /usr/lib/libclntsh.so && \
rm ${CLIENT_FILENAME}


WORKDIR /

RUN pip install --upgrade pip

ADD app /app
RUN addgroup -S worker && adduser -D -h /home/worker -s /bin/bash worker -G worker

USER worker

WORKDIR /home/worker

COPY --chown=worker:worker /app/requirements.txt requirements.txt

RUN pip install --no-cache-dir --user -r requirements.txt


ENV PATH="/home/worker/.local/bin:/usr/lib:${PATH}"

COPY --chown=worker:worker /app /home/worker/app

RUN chmod u+x /home/worker/app/application.bash


#RUN PATH="/usr/lib:${PATH}"

#ENTRYPOINT ["/bin/bash", "-c", "/home/worker/app/application.bash"]
