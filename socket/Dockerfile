FROM alpine:3.15.0
COPY . /app
WORKDIR /app
ARG SSHPASS
ARG USER
ARG SERVER
ARG PORT=34567
ENV USER $USER
ENV SERVER $SERVER
ENV SSHPASS $SSHPASS
ENV PORT $PORT
RUN apk add openssh
RUN apk add --update --no-cache sshpass
EXPOSE 5000
CMD sh socket.sh