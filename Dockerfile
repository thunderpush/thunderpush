FROM python:3.6-alpine
LABEL maintainer="Krzysztof Jagiello <me@kjagiello.com>"

RUN mkdir /app
WORKDIR /app

RUN apk add --no-cache gcc

COPY setup.py .
COPY thunderpush/ thunderpush
RUN python setup.py install
RUN apk del gcc

CMD thunderpush -H 0.0.0.0 ${PUBLIC_KEY} ${PRIVATE_KEY}
