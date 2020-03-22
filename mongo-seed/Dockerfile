FROM mongo:4.2.3

COPY init.json /init.json
CMD mongoimport --host mongodb --db vivid-streets --collection locations --type json --file /init.json --jsonArray