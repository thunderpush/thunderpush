FROM python:3-alpine

RUN mkdir /app
WORKDIR /app

RUN apk add --no-cache gcc

COPY setup.py .
COPY thunderpush/ thunderpush
RUN python setup.py install

CMD thunderpush -H 0.0.0.0 ${PUBLIC_KEY} ${PRIVATE_KEY}
