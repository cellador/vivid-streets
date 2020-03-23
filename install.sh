if [[ ! -f "backend-secret.env" ]]; then
    touch backend-secret.env
fi

if [[ ! -f "react-secret.env" ]]; then
    touch react-secret.env
fi

echo "Setup done."
echo ""

echo "(WARNING: This will affect and remove ALL running docker container)"
while true; do
   read -p "Do you wish to reset your docker instance as well? [y/N] " yn
    case $yn in
        [Yy]* ) docker container rm $(docker container ls -a -q) 2>/dev/null; docker volume prune; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes (y/Y) or no (n/N).";;
    esac
done
