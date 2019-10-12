
#!/bin/bash


echo "I am assuming you are in the home directory of Community Detection Folder"
source venv/bin/activate
source requirements.sh > /dev/null

echo "Please enter your choice of graph: (amazon, dblp, youtube)"
read cat

echo "Please enter your choice of size: large may be slower to compute (small, medium, large)"
read var

source clear_db.sh /dev/null
echo "DB takes some time to restart, so Hwz your life?"
sleep 20

python3 initialize.py $cat $var

echo "Using Python2 at /usr/bin/python to run the metrics"
/usr/bin/python metrics_code/metrics.py datasets/$cat/$cat.graph.$var datasets/$cat/$cat.comm.$var predictions/$cat.ISpred.$var results/$cat.IS.$var >> results/$cat.IS.$var.console
/usr/bin/python metrics_code/metrics.py datasets/$cat/$cat.graph.$var datasets/$cat/$cat.comm.$var predictions/$cat.LApred.$var results/$cat.LA.$var >> results/$cat.LA.$var.console

echo "Please check the below given files for your results"
echo results/results/$cat.LA.$var.console -- "Results computed after the LA computation"
echo results/results/$cat.IS.$var.console -- "Results computed after the IS computation"
echo "For more Detailed output look in the csv files in the results folder"
