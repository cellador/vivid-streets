# vivid-streets
Inspired by the #wirvsvirus hackathon

Check out our [minimum viable product design document](https://docs.google.com/document/d/12eWC8yBUxbbC6EBN0LuYz3d_Lq86mba4eY3HCKqORDM/edit?usp=sharing) for a better overview of what we're trying to do here.

Some more information on the tech stack can be found in the [wiki](https://github.com/cellador/vivid-streets/wiki)

A quick rundown how you can contribute can be seen in the [CONTRIBUTING.md](https://github.com/cellador/vivid-streets/blob/master/CONTRIBUTING.md)

## How to launch the app:

1. Install docker and docker-compose on your machine
2. Clone repository using `git clone https://github.com/cellador/vivid-streets.git`
3. From the project root, execute `./install.sh` but answer no (Enter `n`) to the question if it should reset your docker container. This will still create the files necessary (`backend-secret.env` and `react-secret.env`) to pass environent variables such as the Google Maps API key to the container. This script is additionally helpful if you want to reset your docker: a) have no other docker container installed on your computer and b) want to install a new react module using the package.json.
4. Add a Google Maps Javascript API key to the `react-secret.env` (append a line that says `REACT_APP_GOOGLE_MAPS_API_KEY={ Your key }`)
5. Whenever you want to run the app, check that the docker service is running and enter `docker-compose up --build` from the project root. Any code changes you save while the app is running are automatically applied, no need to restart the container.
