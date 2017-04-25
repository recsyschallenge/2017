'''
Build recommendations based on trained XGBoost model

by Daniel Kohlsdorf
'''

from model import *
import xgboost as xgb
import numpy as np

TH = 0.9

def classify_worker(item_ids, target_users, items, users, output_file, model):
    item_dict = {}
    with open(output_file, 'w') as fp:
        pos = 0
        average_score = 0.0
        num_evaluated = 0.0
        for u in target_users:
            data = []        
            ids  = []

            # build all (user, item) pair features based for this item
            for i in item_ids:        
                x = Interaction(users[u], items[i], -1)
                if x.title_match() > 0:
                    f = x.features()
                    data += [f]
                    ids  += [i]

            if len(data) > 0:
                # predictions from XGBoost
                dtest = xgb.DMatrix(np.array(data))
                ypred = model.predict(dtest)

                # compute average score
                average_score += sum(ypred)
                num_evaluated += float(len(ypred))

                # use all items with a score above the given threshold and sort the result
                iids = sorted(
                    [
                        (ids_j, ypred_j) for ypred_j, ids_j in zip(ypred, ids) if ypred_j > TH
                    ],
                    key = lambda x: -x[1]
                )
                if(len(iids) > 0):
                    iid = iids[0]
                    if iid[0] not in item_dict:
                        item_dict[iid[0]] = []
                    item_dict[iid[0]] += [u]
            
            # Every 100 iterations print some stats
            if pos % 10 == 0:
                try:
                    score = str(average_score / num_evaluated)
                except ZeroDivisionError:
                    score = 0
                percentageDown = str(pos / float(len(item_ids)))
                print(output_file + " " + str(percentageDown) + " " + str(score))
            pos += 1        

        for item_id in item_dict.keys():
            if len(item_dict[item_id]) > 0:
                fp.write(str(item_id) + "\t")
                for user_id in item_dict[item_id][0:-1]:
                    fp.write(str(user_id) + ",")
                fp.write(str(item_dict[item_id][-1]) + "\n")
        fp.flush()

