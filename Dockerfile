# syntax=docker/dockerfile:1
FROM monarchinitiative/linkml:latest

WORKDIR /app

# Copy whatever resources we need into the app (JSON/LinkML/JSON-LD schemas etc.)
COPY ./iSamplesSchemaBasic0.3.yml .
COPY ./iSamplesSchema0.5.yml .

CMD [ "/bin/bash" ]