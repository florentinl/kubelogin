FROM python:3.8
RUN useradd notroot \
    && mkdir /home/notroot \
    && chown -R notroot:notroot /home/notroot

USER notroot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY certificate_generator.py kubeconfig_generator.py server.py user_creator.py ./
ENTRYPOINT [ "python", "server.py" ]