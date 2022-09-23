FROM registry.access.redhat.com/ubi8/ubi-minimal:8.6

RUN --mount=type=tmpfs,destination=/var/cache\
    --mount=type=tmpfs,destination=/root/.cache\
    --mount=type=cache,target=/var/cache/yum\
    --mount=type=cache,target=/var/cache/dnf\
    --mount=type=cache,target=/root/.cache\
    microdnf update -y &&\
    microdnf install -y\
    python3\
    python3-pip\
    &&\
    python3 -m pip install --upgrade pip

COPY requirements.txt .
RUN --mount=type=tmpfs,destination=/root/.cache\
    --mount=type=cache,target=/root/.cache\
    python3 -m pip install -r requirements.txt

COPY . ./
RUN python3 -m pip install .

ENTRYPOINT ["auto_report"]
