cd /var/lib/neo4j/data/databases/
sudo rm -rf gdm.db/
sudo mkdir gdm.db
cd ~/Community_Detection
sudo neo4j stop
sudo neo4j start
