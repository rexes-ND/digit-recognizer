FROM node:20-bookworm-slim

WORKDIR /home/node/frontend

COPY package*.json ./

RUN npm install

COPY . .

RUN chown -R node:node .

USER node

CMD npm run dev
