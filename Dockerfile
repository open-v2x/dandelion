FROM ubuntu:20.04

ARG GIT_BRANCH
ARG GIT_COMMIT
ARG RELEASE_VERSION
ARG REPO_URL

LABEL dandelion.build_branch=${GIT_BRANCH} \
      dandelion.build_commit=${GIT_COMMIT} \
      dandelion.release_version=${RELEASE_VERSION} \
      dandelion.repo_url=${REPO_URL}

COPY ./ /dandelion/
COPY ./etc/dandelion/gunicorn.py /etc/dandelion/gunicorn.py
COPY ./etc/dandelion/dandelion.conf.sample /etc/dandelion/dandelion.conf
COPY ./tools/run_service.sh /usr/local/bin/run_service.sh

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN export LANG=C.UTF-8 \
    && apt-get update -y && apt-get install -y --no-install-recommends apt-utils \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    traceroute lsof iputils-ping vim git wget curl locales-all ssl-cert \
    python3 python3-pip python3-dev python3-venv gcc make \
    && rm -rf /usr/bin/python /usr/bin/pip \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip \
    && cd /dandelion/ \
    && git init \
    && git config --global user.name build \
    && git config --global user.email build@mail.com \
    && git add . \
    && git commit -a -m "Build ${GIT_BRANCH} ${GIT_COMMIT}" \
    && cd / \
    && pip install dandelion/ \
    && apt-get clean \
    && rm -rf ~/.cache/pip

EXPOSE 28100

CMD ["run_service.sh"]
