FROM ubuntu:22.04

# Source: https://github.com/rexes-ND/dockerfiles/blob/main/jupyter-venv/Dockerfile
RUN groupadd --gid 1000 rexes \
    && useradd --uid 1000 --gid 1000 -m rexes \
    && apt-get update \
    && apt-get install -y sudo \
    && echo rexes ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/rexes \
    && chmod 0440 /etc/sudoers.d/rexes

USER rexes

RUN sudo apt-get install -y \
    python3 \
    python3-venv \
    tzdata

WORKDIR /home/rexes/backend

RUN python3 -m venv /home/rexes/venv
ENV PATH="/home/rexes/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD sudo chmod +x entrypoint.sh && ./entrypoint.sh

EXPOSE 8000
