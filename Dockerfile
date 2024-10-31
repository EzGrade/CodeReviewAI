FROM ubuntu:latest
LABEL authors="grade"

ENTRYPOINT ["top", "-b"]