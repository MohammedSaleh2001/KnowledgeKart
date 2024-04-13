# ECE 493 Capstone Project

KnowledgeKart is a student trading platform where users can post listings to sell to other users. Users can also view and search for listings, interacting with users using a chat interface.

There are several containers in the compose file:
  - postgres (database)
  - pgadmin4 (database administration)
  - nginx (reverse proxy / tls)
  - flask (frontend)
  - grafana (analytics)
  - etl (analytics process)
  - init-grafana (initial grafana script)

<b> TO RUN: </b>

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

<br></br>

<b> NOTE: </b>

You may need to use sudo before Docker commands for them to operate properly.
Check out this URL to mitigate this.
https://www.linkedin.com/pulse/how-run-docker-commands-without-sudo-andrey-byhalenko-gawzf/

<b> NOTE: </b>

There is a chance that Docker does not have permission to files.
If you receive:
<i> error docker-entrypoint-initdb.d/init.sh: /bin/sh: bad interpreter: Permission denied postgres exited with code 126 </i>

Try: 
- chmod +x db-setup/init.sh

If you receive:
<i>open .docker/buildx/current: permission denied</i>

Try: 
- sudo chown -R $(whoami) ~/.docker

<b> NOTE: </b>

Certain distros and Windows struggle with Docker DNS resolving. If containers cannot communicate, compose down then compose up.

<br></br>

You should now be able to navigate to localhost/

There are three default administrative users:
- kkowner@ualberta.ca (pass: kkownerpass)
- kkadmin@ualberta.ca (pass: kkadminpass)
- kkmod@ualberta.ca  (pass: kkmodpass)

Do not change these user's password, and instead change the .env file before startup.

There are several sample users:
- joe@ualberta.ca (pass:  joepass)
- bob@ualberta.ca (pass:  bobpass)
- alice@ualberta.ca (pass: alicepass)
- tim@ualberta.ca (pass: timpass)
- mark@ualberta.ca (pass: markpass)

To access analytics, go to localhost/grafana
The specific dashboard is at localhost/grafana/d/analytics/

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

## Functional Requirements

Here is further description on some functional requirements.

EMAIL FRS:
- The best way to evaluate that emails are working is register using your own ualberta email, and kkadmin@ualberta.ca, since we would rather not spam joe :) .

FR18:
- There are two verdicts, close and suspend, but will mark the report as closed in the database.
- The difference is that suspend is reflected in the kkuser table in main.

FR20:
- Administrative users can file a report against a user, to ensure that a reason will be given, which allows them to suspend. 

FR21: 
- See SQL/analytics/core, where there are three fact tables, and the "sale" fact table being core_listing.
- dim_date, dim_time, dim_status, dim_condition, and dim_categorytype are the relevant tables
- in the files themselves, you can see reduced columns

FR22: 
- SQL/analytics/core/1-CREATE_TABLE_core_delta.sql is where delta columns are stored. Primary keys are used as facts.

FR23:
- See SQL/analytics/datamart, where there are 6 reports aggregating information.
- For the final sentence, the use of "such as" was deliberate, as at the time what would be visualized. We formally decided to use category and condition.

FR24:
- Data mart updates are done first by update_etl changing the core database, and core_etl re-performing the operations

FR25:
- The analytics dashboard is refreshed every minute (see top right corner)
- Slicing is done through the time picker in the top right, and specific date/time dimensions on the top left
- Dicing is done through category and condition. There are figures/graphs already diced by status.
- To export figures and reports, click the ellipses at the top right of any figure, and select "View Data". There should be an option to export as .csv