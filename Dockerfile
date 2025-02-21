FROM python:slim
WORKDIR /app
COPY requirements.txt config.yaml ./
COPY ppim-migrator ./ppim-migrator
RUN pip3 install -r requirements.txt --break-system-packages
ENV PYTHONPATH=/app
ENTRYPOINT [ "python", "-m", "ppim-migrator" ]
