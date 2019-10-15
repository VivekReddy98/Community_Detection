# Overlapping Communities Detection
Graph Data Mining Course Project

This was implemeneted in reference to the algorithm presented in Paper-1 under resources folder  

### Tools Required:
1) Python 3
2) Python 2
3) Neo4j (Graph DB)

### Libraries required:
1) All the required libraries are present in requirements.txt file
2) neo4j -- Python Driver to access neo4j Database
3) py2neo -- py2neo is a client library to access and operate neo4j with python
Note: Use py2neo v4 (https://py2neo.org/v4/) 

### Neo4j Installation Guide:
Note: OS is assumed to be Linux (debian)
Note: Java 8 is required for Neo4j (VCL image already has Java 8)
1) wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
2) echo 'deb https://debian.neo4j.org/repo stable/' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
3) sudo apt-get update
4) sudo apt-get install neo4j=1:3.5.11 (Check the updated version while you are installing)
For more information, follow this link: https://neo4j.com/docs/operations-manual/current/installation/linux/debian/#debian-installation


### Useful Commands:
1) neo4j restart
2) neo4j start
3) neo4j stop
4) cypher-shell (To-pass cypher commands directly)

### Useful Locations:
1) /etc/neo4j/neo4j.conf -- <Edit the configuration parameters of the Neo4j Here
2) /var/lib/neo4j/data/databases/xxx.db/ -- Data is stored here. (graph.db is the default)
3) /var/lib/neo4j/plugins/ -- Add Any extra plugins here. 
4) Create this file:
5) sudo mkdir /var/lib/neo4j/data/databases/graph.db/

### Add Neo4j Algorithms Jar:
1) Resources : https://neo4j.com/docs/graph-algorithms/current/introduction/#_installation
2) Neo4j Download Center: https://neo4j.com/download-center/#enterprise
3) Download Neo4j Graph Algorithms jar from the Download center

#### Follow the below Specified Steps for adding Neo4j algorithm (Check your version while updating)
1) wget https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/neo4j-graph-algorithms-3.5.11.0-standalone.zip
2) Unzip neo4j-graph-algorithms-3.5.11.0-standalone.zip
3) mv neo4j-graph-algorithms-3.5.11.0-standalone.jar /var/lib/neo4j/plugins/
4) Edit the configuration file by adding:
5) "dbms.security.procedures.unrestricted=algo.*,apoc.*"
6) Also uncomment this line:
8) dbms.security.auth_enabled=false
9) Restart the neo4j server using neo4j restart, use sudo if you face any permission issues.

### Set up the environment and required folders:
0) Clone this repositiry preferabbly in /home/unityID/Community_Dection
1) Install virtual environment package:
2) apt-get install python-virtualenv
3) Create a virtual environment inside your project directory using 
4) virtualenv -p /usr/bin/python3 project_directory/venv (The second argument is he name of the folder which will be created, you might not want to change it)
5) Copy Datasets and metric_code folder from your local machine to this repository.
6) In your local Machine, go to the location where your have metric_code and datasets folders and run these commands.
7) scp -r metrics_code unityID@ip_addr:/home/unityID/Community_Detection
8) scp -r datasets unityID@ip_addr:/home/unityID/Community_Detection
9) start your virtual environment using the command
10) source venv/bin/activate
11) Install required packages using the command
12) pip install -r requirements.txt (These packages will be installed in the venv i.e. locally)

### Setting Environment variables.
1) Set the environment variable by editing the below given line in the script compute_results.sh
Point this path to the folder where your community detction folder is present.
2) export GDMPATH=/home/unityID/Community_Detection

### Brief overview to get the code running.
1) The Source Code is present in Utils folder and packaged as a library.
2) initialize.py will consolidate and compute the clusters for any given graph.
3) compute_results.sh will take these results and apply metric calculation script on them.
4) The predictions are stored in predictions folder
5) Since there are two parts in the algorithm LA and IS. Results after every step have been recorded for comparison purposes.
6) To view the summary of the results go to the "*.*.*.console" files.

### Instrcutions to get it running.
1) Read through the script compute_results.sh
2) Run it using the command source compute_results.sh
3) Enter your inputs where prompted.
4) After its completion, find the results in result folder.
5) Time taken by the algorithm is present in time_taken.txt
