## ETL_Project1

# Docker installation
Install Docker from web and run docker init to intialize.

# Python environment for postgres database 
libraries:
Install pandas (for data manipulation), pyarrow, fastparquet (to read database file(parquet))

Install sqlalchemy, to deal with sql in python with pandas. (we use create_engine function to connect postgresdb to pandas)

Install psycopy2 (to interact with PostgreSQL databases using Python)

# Postgres Database connection and configuration:
Setting up postgres image in Docker from command line:
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v path_to_the_database_in_local/ny_taxi_postgres_data:/var/lib/postgresql/pg_data \
-p 5432:5432 \
postgres:13 
Ingestion script:

It shows "server started" after initialization.

After successfully establishing postgres for docker, for postgres cli, run this commands:
pip install pgcli //(postgres client for cl)
pgcli -h localhost -p 5432 -u root -d ny_taxi //conecting to db from cli

# Connecting pgadmin to Postgres DB
To interact with the database in a GUI, we can use pgadmin by creating a network with pgadmin container and Postgres container. Use the following cli docker commands:

#Pgadmin-Postgres Docker Network:

docker network create pg-network     // Creates a network named 'pg-network'

docker run -it \                    // To run the postgres container again by adding  network and name details to communicate with pgadmin within the network.
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v /Users/revanthvemula/ETL_Project1/ny_taxi_postgres_data:/var/lib/postgresql/pg_data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13

// another way:(didnt tried it)
docker stop existing_postgres_container_name
docker network connect your_network_name existing_postgres_container_name
docker start existing_postgres_container_name

docker run -it \                   // To create pgadmin container within the network.
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin-1 \
dpage/pgadmin4

# Ingestion script and Dockerizing ingestion script
Write python script for ingestion (here ingest_data.py)
We need argparse library to read arguments passed in cli.
Create a dockerfile in vs code and wirte the following for dockerizing the ingestion script:
FROM python:3.12

RUN apt-get install wget
RUN pip install pandas psycopg2 sqlalchemy pyarrow fastparquet 

WORKDIR /app
COPY ingest_data.py ingest_data.py

To dockerize the ingestion script, run the following commands in cli:
docker build -t ingest_taxi_data:v001 .

docker run -it \
  --network=pg-network \
  ingest_taxi_data:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=nyc_taxi_trips \
    --url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"

ENTRYPOINT ["python","ingest_data.py"]
# Creating Docker-compose file (helps you to pack and share the container)
Instead of running seperate run statements for postgres and pgadmin, you can set up a docker-compose file which you can share across with other users.

make sure you stop the docker images for postgres and pgadmin before running the docker-compose up

To ensure the data is persistent across all the container runs, you need to specify same network in the docker-compose and also when you are making any changes to db in host machine.

You need to create a volume mount for the pgadmin so it doesnt get erase everytime you close and open it.

# Setting up GCP SDK
Install the SDK using: brew install --cask google-cloud-sdk

Create a gcp account-> new project-> Generate keys and download the file using json.

Using the downloaded keys we can connect the local machine to gcp by running:
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

Refresh token/session, and verify authentication by running: gcloud auth application-default login

It redirects you to the webpage and asks you to authenticate.

For the project in GCP, add these roles in addition to Viewer : Storage Admin , Storage Object Admin , BigQuery Admin.

Enable these APIs for the project:
https://console.cloud.google.com/apis/library/iam.googleapis.com
https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

# Setting up Terraform
Download terraform and intialize it using: terraform init

other execution statements:
To preview local changes against a remote state, and to view an Execution Plan: terraform plan

To apply changes to cloud:
terraform apply

To remove the stack from the Cloud:
terraform destroy

Create a "main.tf" where you manage all the resources and "variables.tf" file to create variables you use in setting up resources.

# Set up GCP environment for Cloud VM and SSH access
Create a SSH key in ~/.ssh directory by using following command in cli:
ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048

Copy the public key (KEY_FILENAME.pub) and add the SSH key in gcp portal by going into compute engine/settings/metadata.

Create a VM instance in gcp and copy the external IP into the local terminal in the command: ssh -i ~/.ssh/gcp revanthv@<insert external ip here>
or
Create a ~/.ssh/config file in local with details of Host, HostName, User, IdentityFile and save it.(Refer ~/.ssh/config file attached in repo)
To connect to  vm server, run $ssh <Host> 

To setup ssh vm on vscode, install Remote - SSH extension in your local vscode and toggle to "click on remote window" option on bottom left corner, select "connect to host" option and type in your host name.

Install docker in the vm environment using: sudo apt install docker.io

To run docker without sudo (since docker daemon always runs as the root user):
follow the steps at the link: https://docs.docker.com/engine/install/linux-postinstall/

Create a folder "bin" where you can keep exxecutable files and install docker-compose in it by running wget https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-linux-x86_64 -O docker-compose

after installing docker-compose, change the file to executable file using $ chmod +x docker-compose

To make docker-compose accessible from any directory,edit this to PATH variable:
open bashrc file using $ nano .bashrc,in home folder and add the command: export PATH = "${HOME}/bin:${PATH}" ,at the end of the file and save it.
Again in cli, enter $ source .bashrc , to logout and login again into bashrc. 

Run $ docker-compose up -d in the project directory path 

Later install pgcli to interact with postgres.

To interact with postgres and pgadmin in local, forward the postgres port(5432) and pgadmin(8080) in vm to local by using "ports" section in vscode.

Download Terraform into bin directory(executable) in vm by using terraform linux binary download package.

Next to safely transer the gcp keys json file which was saved earlier while setting up gcp terraform environment on local, using sftp. (Open the directory where the keys json file is saved and run $ sftp <vm config file name> --> $put <keysfilename.json>)

Now you can configure gcp cli in the vm using the same process we followed to setup in local.

To stop the vm from terminal -> $sudo shutdown now

# Setting up Airflow to shcedule tasks
Create a new sub-directory called airflow in the project directory.

Inside airflow, create dags,logs and plugins folders using the following commands.
$mkdir -p ./dags ./logs ./plugins
$echo -e "AIRFLOW_UID=$(id -u)" > .env

.env is created and used to store airflow user id, if it is not automatically create a .env file and enter AIRFLOW_UID=50000 in the file.

We are running the airflow service in docker setup, to create a docker setup for airflow latest version, use:
$curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

A docker-compose yaml file is created with all the ariflow services(you can always remove unused services from the yaml file for better performance)

Insided the docker-compose file, in x-airflow-common:
Remove the image tag, to replace it with your build from your Dockerfile, as shown
Mount your google_credentials in volumes section as read-only
Set environment variables: GCP_PROJECT_ID, GCP_GCS_BUCKET, GOOGLE_APPLICATION_CREDENTIALS & AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT, as per your config.
Change AIRFLOW__CORE__LOAD_EXAMPLES to false (optional)

Docker Build:
Create a Dockerfile pointing to Airflow version you've just downloaded, such as apache/airflow:2.2.3, as the base image,

And customize this Dockerfile by:

Adding your custom packages to be installed. The one we'll need the most is gcloud to connect with the GCS bucket/Data Lake.
Also, integrating requirements.txt to install libraries via pip install









