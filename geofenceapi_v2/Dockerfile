FROM python:3.6.9-slim

RUN useradd --create-home --shell  /bin/bash apirunner
USER apirunner
VOLUME /data
RUN mkdir /home/apirunner/geofenceapi
WORKDIR /home/apirunner/geofenceapi
COPY --chown=apirunner:apirunner . .
ENV PATH="/home/apirunner/.local/bin:${PATH}"
RUN echo "export PATH=$PATH"
RUN pip install --user --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3  \ 
    CMD curl --fail http://localhost:8000/health || exit 1

#CMD ["NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]