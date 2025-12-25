FROM node

WORKDIR /server
RUN ls -l
# RUN npm i
RUN npm i -g ts-node
#RUN cd src/server/server.ts

#CMD ts-node server.ts