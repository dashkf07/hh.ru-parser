# pull official base image
FROM node:latest as build
# set working directory
WORKDIR /frontend
# add `/app/node_modules/.bin` to $PATH
ENV PATH /frontend/node_modules/.bin:$PATH
# install app dependencies
COPY package.json ./
COPY package-lock.json ./
# Silent clean install of npm
RUN npm ci --silent
RUN npm install react-scripts@3.4.1 -g --silent
# add app
COPY . /frontend/

# Build production
RUN npm run build
RUN npm install -g serve

## Start the app on port 3006
CMD serve -s build -l 3006