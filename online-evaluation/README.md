Online Evaluation
=====================

![Recsys2017 Timeline](img/timeline.png)

The online evaluation is set up as follows. The goal of each team is the same as during the _offline challenge_: given a new item (job posting), identify those users that are interested in the job and that are at the same time also of interest to the recruiter who is associated with the posting.

- `X_0`: Some days before the online evaluation challenge starts, a new dataset will be released for the participating teams: 
  + users: teams will be presented with a set of users and their profile information at the beginning of the challenge, the teams  (cf. [users.csv](http://2017.recsyschallenge.com/#dataset-users)). 
    - This set stays valid throughout the whole online evaluation period (until `X_end`). 
  + items: details about items that those users recently interated with (cf. [items.csv](http://2017.recsyschallenge.com/#dataset-items)). 
  + interactions: the interactions that those users performed recently (cf. [interactions.csv](http://2017.recsyschallenge.com/#dataset-interactions))
- Each day the teams then receive... 
  + a set of target users = those user IDs to whom the team can recommend new items (cf. [targetUsers.csv](http://2017.recsyschallenge.com/#dataset-targets))
  + the new items for which can be recommended to the target users. Format of the item description is the same as during the offline evaluation: [items.csv](http://2017.recsyschallenge.com/#dataset-items)
  + updated interactions: the interactions that have been collected during the previous day (cf. [interactions.csv](http://2017.recsyschallenge.com/#dataset-interactions))
    - The impressions/interactions will also include entries that have been triggered by other teams or by XING's search and recommendation systems. 
- `X_t-1` till `X_t`: Within these 24 hours, teams can submit their solution files (columns: `item_id`, `user_ids`). Here, the following restrictions hold: 
  + Teams will be allowed to
submit each user id from their target list at maximum one time. 
  + It is ok if the team chooses to not play out a recommendation for a given target user (notice that rolling out a recommendation that just receives negative feedback, will result in a negative score, see: [Evaluation Metrics](http://2017.recsyschallenge.com/#evaluation)). 
  + If the team submits a posting older than 24 hours, a user
not in their target list or a user they already sent a recommendation to that
day, the system will ignore the following information.
- `X_w`: the score will be calculated on all item-user pairs a team submitted (given that the above mentioned restrictions were not violated).
  + Submitted recommendations can be interacted with for one week. 
  + Afterwards, the interactions of a user with that item do not
count towards the final score. 
- `X_res`: The winning team is the one that achieved the highest
sum of their two best scoring weeks. The winnner of the challenge will be announced one week after
the last submisssion slot.


## Differences to Offline Evaluation

- TODO...


