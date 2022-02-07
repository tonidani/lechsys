FROM lechsys-backend-master_toni-python-app-base:latest

# RUN apt-get install -y apt-transport-https
# RUN apt-get update -y && \
#     apt-get install -y --no-install-recommends python3.8 python3.8-dev python3.8-distutils python3.8-venv python3-pip


# RUN python3 -m pip install setuptools-rust
# RUN apt-get -y install libmysqlclient-dev
# RUN apt-get -y install build-essential libssl-dev libffi-dev \
#     python3-dev cargo
# RUN python3 -m pip install -r requirements.txt

# cmd odpali przy starci docker-compose, a run podczas budowania obrazu
COPY . .
CMD ["./migrate.sh"]

# CMD ["./migrate.sh"]


# CMD ["python3", "pip", "install", "-r", "requirements.txt"]


# build environment
# FROM node:9.6.1 as builder
# RUN mkdir -p /usr/src/app
# WORKDIR /usr/src/app
# ENV PATH /usr/src/app/node_modules/.bin:$PATH
# COPY package.json /usr/src/app/package.json
# RUN yarn install
# RUN yarn add react-scripts@1.1.1 
# COPY . /usr/src/app
# RUN yarn build
# CMD ["yarn", "start"]
# EXPOSE 3000


# # production environment
# FROM nginx:1.13.9-alpine
# COPY --from=builder /usr/src/app/build /usr/share/nginx/html
# CMD ["nginx", "-g", "daemon off;"]
