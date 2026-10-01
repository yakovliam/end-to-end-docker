FROM python:3.12-alpine

WORKDIR /home

COPY --chown=65532:65532 scripts.py /home/scripts.py
COPY --chown=65532:65532 data /home/data

USER 65532:65532

ENTRYPOINT ["python3", "/home/scripts.py"]
