Baseline
========

!!!!!! DELETE THE HEADER IN THE TARGET FILES !!!!!!!
========

This is the simple baseline that creates the sample_solution.csv file.
The baseline system extracts features from interacted user-item pairs
and "learns" if a user will interact positively with an item.
The underlying learning algorithm is [XGboost](https://xgboost.readthedocs.io/en/latest/).
Which is a tree ensembeling method that most winning teams used last year.

The features are:
  + number of matches in title ids [Int]
  + discipline matches [0, 1]
  + career level matches [0, 1]
  + industry matches [0, 1]
  + country match[0, 1]
  + region match [0,1]

Files:
  + The data model along with the feature extraction can be found in `model.py`.
  + Parsing the data is performed in `parser.py`.
  + A parallel prediction algorithm is given in `recommendation_worker.py`.
    The recommendation worker uses the target items and users. If we have
    a title match at all the score for each user is predicted.
  + The main training and testing is performed in `xgb.py`
  
In order to build the baseline XGboost has to be installed with the python binindgs.
