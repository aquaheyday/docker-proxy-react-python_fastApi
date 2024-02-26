FROM nginx:1.25.1

COPY ./nginx.conf /etc/nginx/nginx.conf

RUN apt-get update

RUN apt-get install -y git unzip

EXPOSE 80

ENTRYPOINT ["nginx","-g","daemon off;"]