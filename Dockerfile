FROM python:slim-bookworm
COPY requirements.txt config.yaml /root
COPY ppim-migrator /root/ppim-migrator
WORKDIR /root
RUN pip3 install -r requirements.txt
ENV PYTHONPATH=/root
ENTRYPOINT [ "python", "-m", "ppim-migrator" ]
