# Event Management App

## Developer Setup

To set up, build, and run the project for the first time:

1. Clone the repository to your local system and open the project in Visual Studio Code or a similar code editor.
   - `git clone https://github.com/CS160-04-Spring2024/Event-Management-App.git`

2. Install Docker Desktop if you don’t have it already:
   [Docker Desktop](https://www.docker.com/products/docker-desktop/)

3. Download the .env file with the necessary environment variables and place them in the project directory, i.e “event-management-project/events/events”:
   [Sqlite + env file](https://drive.google.com/drive/folders/1xX6c8WhvVasSXLXijmZo-_rVtNsloQ-5?usp=sharing)
   (rename the env file to .env)

4. Download the db.sqlite database file from the previously shared directory and place it in the project directory, i.e “event-management-project/events/”

### Running The Web App using Docker:

- Navigate over to the project directory and start the docker container with the command:
   * `docker-compose up`

### Running The Web App locally (requires Python +3.10):

- Recommended: Create a new Python environment (using Venv):

  - Mac OS : `python3 -m venv {env_name}`
  - Windows : `py -m venv {env_name}`

- Recommended (contd.): Activate the new Python environment
  - Mac OS : `source {env_name}/bin/activate`
  - Windows : `{env_name}\Scripts\activate`

- Recommended (contd.): Potential error on Windows machines:-

* If the command to run the script fails to run due to an error along the lines of “File cannot be loaded because running scripts is disabled on this system.”
  - Run PowerShell as administrator
  - Run the command: Set-ExecutionPolicy RemoteSigned
  - Type Y and enter
  - Attempt to run the script again

- Install the requirements needed for the project by running the following command line:
  `pip3 install -r  .\requirements.txt`

- Navigate to the events directory and run the project on your local server by calling manage.py with the following command line:
  `python manage.py runserver`

- Navigate to your localhost at the appropriate port:
  Open the landing page through the link provided, which should look something like:
  `http://127.0.0.1:8000/`
