ECE 493 Capstone Project

KnowledgeKart is a student trading platform where users can post listings to sell to other users. Users can also view and search for listings, interacting with users using a chat interface.

There are several containers in the compose file:
  - postgres (database)
  - pgadmin4 (database administration)
  - nginx (reverse proxy / tls)
  - flask (frontend)
  - grafana (analytics)
  - etl (analytics process)
  - init-grafana (initial grafana script)

TO RUN:

Ensure you have either Docker Desktop, or Docker Engine and Docker CLI.
See: https://docs.docker.com/get-docker/

- Clone the repo into your desired directory. 
- Direct into the directory. Use:
    - docker compose build
    - docker compose up
  To start the containers.
You can also use
  - docker compose up --build
as a shorthand for this.

To run in the background, add the -d flag to the end.

You can now navigate to localhost/

There are three default administrative users:
- kkowner@ualberta.ca (pass: kkownerpass)
- kkadmin@ualberta.ca (pass: kkadminpass)
- kkmod@ualberta.ca  (pass: kkmodpass)

Do not change these user's password, and instead change the .env file before startup.

There are several sample users:
- joe 
- bob
- alice
- tim
- mark

Addresses end with @ualberta, and their passes are <name>pass.

To access analytics, go to localhost/grafana

Login with either:
- kkowner and kkownerpass
- kkadmin and kkadminpass

To stop Docker, use CTRL+C in the terminal, or in another terminal
- docker compose down

To remove changes to the database, use:
- docker compose down --volumes
which removes volumes, and refreshes everything on next startup.

You can clear installed images by using
  - docker image prune -a
This clears all images and allows for a fresh run.