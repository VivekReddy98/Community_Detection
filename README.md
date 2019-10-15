# Overlapping Communities Detection
Graph Data Mining Course Project

This was implemeneted in reference to the algorithm presented in Paper-1 under resources folder  

### Tools Required:
1) Python 3
2) Python 2
3) Neo4j (Graph DB)

### Neo4j Installation Guide:
Note: OS is assumed to be Linux (debian). Follow this link to install Neo4j
1) Java 8 is required for Neo4j (VCL image already has Java 8)
2) Installation: sudo apt-get install neo4j=1:3.5.11 (Check the updated version while you are installing
For more information, follow this link: https://neo4j.com/docs/operations-manual/current/installation/linux/debian/#debian-installation

### Useful Locations:
1) /etc/neo4j/neo4j.conf -- Edit the configuration parameters on this file
2) /var/lib/neo4j/data/databases/xxx.db/ -- Data is stored here. (graph.db is the default)
3) /var/lib/neo4j/plugins/ -- Add Any extra plugins here. 

### Add Neo4j Algorithms Jar:
1) Resources : https://neo4j.com/docs/graph-algorithms/current/introduction/#_installation
2) Neo4j Download Center: https://neo4j.com/download-center/#enterprise
3) Download Neo4j Graph Algorithms jar from the Download center

#### Download the algo.* plugin using th command (Check your version while updating)
1) wget https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/neo4j-graph-algorithms-3.5.11.0-standalone.zip
2) Unzip neo4j-graph-algorithms-3.5.11.0-standalone.zip
3) mv neo4j-graph-algorithms-3.5.11.0-standalone.jar /var/lib/neo4j/plugins/
4) Edit the configuration file by adding:
5) dbms.security.procedures.unrestricted=algo.*, apoc.*
6) Restart the neo4j server using neo4j restart, use sudo if you face any permission issues.

### Clone this repository
1) Install virtual environment package:
python3 -m pip install --user virtualenv
2) sudo apt-get install python3-venv
3) Create a virtual environment inside your project directory using 
python3 -m venv venv (The second argument is he name of the folder which will be created, you might not want to change it)

You are good to go after this step.
1) Run compute_results.sh to get going. 
2) It'll install the packages and set the environment variables required.
