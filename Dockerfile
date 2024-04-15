# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

EXPOSE 3000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV DB_PASSWORD=nzzh3o4nu7b82Mo0u3Sp2A97

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
#CMD ["gunicorn", "--config", "gunicorn.conf.py", "app.app"]
#CMD ["flask", "run", "--host", "0.0.0.0"]
#CMD [ "python", "main.py" ]
#ENTRYPOINT [ "python" ]
#CMD [ "main.py" ]
