cd /var/lib/neo4j/data/databases/
sudo rm -rf graph.db/
sudo mkdir graph.db
cd ~/Community_Detection
sudo neo4j stop
sudo neo4j start
