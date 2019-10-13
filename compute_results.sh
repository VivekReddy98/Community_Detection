
#!/bin/bash

echo "I am assuming you are in the home directory of Community Detection Folder"
echo "Plese set this environment Variable, For eg. /home/unityid/Community_Detection/ "/" at the end is important")
export GDMPATH=~/Community_Detection
export PYTHONPATH=$PYTHONPATH:$GDMPATH

echo "Please enter your choice of graph: (amazon, dblp, youtube)"
read cat

echo "Please enter your choice of size: large may be slower to compute (small, medium, large)"
read var


echo "DB takes some time to restart, so Hwz your life?"
sudo rm -rf /var/lib/neo4j/data/databases/graph.db
sudo mkdir /var/lib/neo4j/data/databases/graph.db
cd $GDMPATH
sudo neo4j stop
sudo neo4j start
sleep 20

python3 initialize.py $cat $var

echo "Using Python2 at /usr/bin/python to run the metrics"
/usr/bin/python metrics_code/metrics.py datasets/$cat/$cat.graph.$var datasets/$cat/$cat.comm.$var predictions/$cat.ISpred.$var results/$cat.IS.$var >> results/$cat.IS.$var.console
/usr/bin/python metrics_code/metrics.py datasets/$cat/$cat.graph.$var datasets/$cat/$cat.comm.$var predictions/$cat.LApred.$var results/$cat.LA.$var >> results/$cat.LA.$var.console

echo "......................................................................................"
echo "Scores for LA Computation"
echo " "
cat results/$cat.LA.$var.console

echo "......................................................................................."
echo "Scores for IS Computation"
echo " "
cat results/$cat.IS.$var.console

echo "For Detailed output look in the csv files in the results folder"

