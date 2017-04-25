# Baseline Example for Offline Challenge

The baseline script will periodically check the
recsys online api for updates on the daily data,
download the new data, compute a solution 
and then submit it to the system.

The frequency of checks is every 10 minutes.
Once a solution is computed the script will not perform
another pass that day. The example is only computing
the recommendations based on the xgboost solution
from the offline challenge's baseline, so you have to
put your solution in there.

The files 'parser.py' and 'model.py' are the same as
for the offline challenge. The worker script 'recommendation_worker.py',
is rewritten to match the online challenge.

The main script to execute and schedule a solution is: 'online_schedule.py'.
You need the following libraries: 
    + httplib2
    + xgboost
    + numpy

I tested this with python 3.
In order to run the test you have to grab the user data from:

   https://recsys.xing.com/data/online

And put the users.csv into the data folder.

Train a xgboost model using the offline challenges scripts:
   https://github.com/recsyschallenge/2017/tree/master/baseline

And copy the xgboost model to 'data/recsys2017.model'.

Then you will be set to go :)