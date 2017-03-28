'''
Build recommendations based on trained XGBoost model

by Daniel Kohlsdorf
'''

from model import *
import xgboost as xgb
import numpy as np

TH = 0.8

def classify_worker(item_ids, target_users, items, users, output_file, model):
    with open(output_file, 'w') as fp:
        pos = 0
        average_score = 0.0
        num_evaluated = 0.0
        for i in item_ids:
            data = []        
            ids  = []

            # build all (user, item) pair features based for this item
            for u in target_users:        
                x = Interaction(users[u], items[i], -1)
                if x.title_match() > 0:
                    f = x.features()
                    data += [f]
                    ids  += [u]

            if len(data) > 0:
                # predictions from XGBoost
                dtest = xgb.DMatrix(np.array(data))
                ypred = model.predict(dtest)

                # compute average score
                average_score += sum(ypred)
                num_evaluated += float(len(ypred))

                # use all items with a score above the given threshold and sort the result
                user_ids = sorted(
                    [
                        (ids_j, ypred_j) for ypred_j, ids_j in zip(ypred, ids) if ypred_j > TH
                    ],
                    key = lambda x: -x[1]
                )[0:99]                                                        

                # write the results to file
                if len(user_ids) > 0:            
                    item_id = str(i) + "\t"
                    fp.write(item_id)
                    for j in range(0, len(user_ids)):
                        user_id = str(user_ids[j][0]) + ","
                        fp.write(user_id)
                    user_id = str(user_ids[-1][0]) + "\n"
                    fp.flush()

            # Every 100 iterations print some stats
            if pos % 100 == 0:
                try:
                    score = str(average_score / num_evaluated)
                except ZeroDivisionError:
                    score = 0
                percentageDown = str(pos / float(len(item_ids)))
                print(output_file + " " + percentageDown + " " + score)
            pos += 1        
