ECE 493 Capstone Project

KnowledgeKart is a student trading platform where users can post listings to sell to other users. Users can also view and search for listings, interacting with users using a chat interface.

There are several containers in the compose file:
    - postgres (database)
    - pgadmin4 (database administration)
    - sleeper (for nginx)
    - nginx (reverse proxy / tls)
    - flask (frontend)
    - grafana (analytics)

To add new files for Flask, add to /flaskapp. To add new templates, add to /flaskapp/templates.

TO RUN:

Ensure you have either Docker Desktop, or Docker Engine and Docker CLI.

- Clone the repo into your desired directory. 
- Direct into the directory. Use:
    - docker compose build
    then
    - docker compose up
  To start the containers.
- You can also use
    - docker compose up --build
  as a shorthand for this.

You can now navigate to localhost/ or localhost/grafana.

There are two default users for Flask, kkowner and kkadmin, with default passwords kkownerpass and kkadminpass.

To assess changes to the database, use:
- docker compose down --volumes
to have the database script be re-ran on next startup.