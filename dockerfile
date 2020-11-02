FROM python:3.7-alpine

RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev

# Add HDF5 support
RUN apk add --no-cache --allow-untrusted --repository http://dl-3.alpinelinux.org/alpine/edge/testing hdf5 hdf5-dev

RUN apk --no-cache --update-cache add gfortran build-base wget freetype-dev libpng-dev openblas-dev

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install --upgrade pip

ADD ./myflask /codebase
#ADD requirements.txt .
WORKDIR /codebase
RUN pip install -r requirements.txt
CMD ["python", "-u", "app.py"]
