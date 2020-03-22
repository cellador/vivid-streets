FROM node:13.10

WORKDIR /usr/src/app

COPY package.json /usr/src/app/package.json
RUN npm install --silent
RUN npm install react-scripts@3.4.0 -g --silent

# start app
CMD ["npm", "start"]
