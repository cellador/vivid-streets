#!/bin/sh
if [ ! -f "backend-secret.env" ]; then
    echo "JWT_SECRET_KEY="$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32 ; echo '') > backend-secret.env
fi

if [ ! -f "react-secret.env" ]; then
    touch react-secret.env
fi

echo "Setup done."
echo "You can now run the app using \"docker-compose up --build\"."
echo ""

echo "Do you wish to reset your docker instance as well? [y/N]"
echo "WARNING: This will stop ALL docker container and remove ALL unused docker volumes,"
echo "         not only those created by this app. It won't affect anything outside of docker."
while true; do
   read -p "> " yn
    case $yn in
        [Yy]* ) docker container rm $(docker container ls -a -q) 2>/dev/null; docker volume prune; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes (y/Y) or no (n/N).";;
    esac
done
