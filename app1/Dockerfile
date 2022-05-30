FROM node:16-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
COPY . .

CMD [ "/usr/src/app/bin/www" ]