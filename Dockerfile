FROM python:3.8
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY certificate_generator.py kubeconfig_generator.py server.py user_creator.py ./
ENTRYPOINT [ "python", "-u", "server.py" ]
EXPOSE 80