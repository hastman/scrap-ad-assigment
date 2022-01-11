FROM python:3.6.9-slim
RUN apt-get update && apt-get install -y ca-certificates wget

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
    CMD wget -O/dev/null -nv -t1  http://localhost:8000/health || exit 1

CMD ["newrelic-admin","run-program","uvicorn", "main:app","--root-path","/v1" ,"--host", "0.0.0.0", "--port", "8000"]