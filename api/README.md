Submission System API (alpha version)
=====================

The API should allow teams to automate their recommender systems and particularly the process of 
downloading data (relevant for online challenge) and uploading solutions. 

Current list of endpoints: 

- [Offline evaluation](#offline-evaluation) 
  + [GET /api/team](#get-apiteam)
  + [POST /api/submission](#post-apisubmission)
- [Online evaluation](#online-evaluation) 
  + [GET /api/online/data/status](#get-apionlinedatastatus)
  + [GET /api/online/data/items](#get-apionlinedataitems)
  + [GET /api/online/data/users](#get-apionlinedatausers)
  + [GET /api/online/data/interactions](#get-apionlinedatainteractions)
  + [POST /api/online/submission](#post-apionlinesubmission)
  + [GET /api/online/submission](#get-apionlinesubmission)

## Offline Evaluation

### GET /api/team

Get team details. 

#### Example request

```
curl -vv -XGET -H 'Authorization: Bearer RAtN...LTA1NjkyOGU5OTE5Mw==' 'https://recsys.xing.com/api/team'
```

Notes: 

- `RAtN...LTA1NjkyOGU5OTE5Mw==` is the access token of the team. It can be generated on the [team details page (access token)](https://recsys.xing.com/team).


#### Example response

```javascript
{
  "name":"Data Rangers 2",
  "remaining_submissions_today":17,
  "submissions":[
    {
      "score":26100,
      "rank":2,
      "label":"test42 (time-decay)",
      "submitted_at":"2017-03-11T00:15:34.000+01:00"
    },
    {
      "score":10003,
      "rank":14,
      "label":"random testing",
      "submitted_at":"2017-03-10T23:38:04.000+01:00"
    },
    ...
  ]
}
```

Notes: 

- `name`: name of the team
- `remaining_submissions_today`: number of submissions that the team can still do on the given day (CET timezone)
- `submissions` pas submissions of the team
  + `score`: the score that was achieved
  + `rank`: the rank that the team achieved with the submission (at the time the submission was done)
  + `label`: the (optinal) label that the team passed when [submitting the solution](#post-apisubmission)
  + `submitted_at`: timestamp when the solution was submitted
- Response codes: 
  + `200` OK
  + `401` Unauthorized (in case the access token is no longer valid or was not properly set in the Header of the request)
  
### POST /api/submission

Uploads a new solution for the team.

#### Example request

```
curl -vv -XPOST -H 'Authorization: Bearer RAtN...LTA1NjkyOGU5OTE5Mw==' 'https://recsys.xing.com/api/submission?label=test42%20(time-decay)' --data-binary @solution_file.csv
```

Notes: 

- `RAtN...LTA1NjkyOGU5OTE5Mw==` is the access token of the team. It can be generated on the [team details page (access token)](https://recsys.xing.com/team).
- `label`: optional label that should be assigned to the submission (won't be visible to other teams)
- `solution_file.csv` is the actual solution file that should be uploaded. See: [Format instructions](https://recsys.xing.com/submission#instructions)

#### Example response

```javascript
{
  "result": {
    "score": 10004,
    "rank": 13,
    "label": "test42 (time-decay)",
    "submitted_at": "2017-03-11T00:44:04.764+01:00"
  },
  "is_top_score": false,
  "remaining_submissions_today": 18,
  "lines_skipped": [1]
}
```

Notes: 

- `result`: the result that the uploaded solution achieved (relevant for offline challenge)
  + `score`: the score that was achieved
  + `rank`: the rank that the score achieved wrt to the [current leaderboard](https://recsys.xing.com/leaders)
  + `label`: the label that was assigned to the submission 
  + `submitted_at`: timestamp when the solution was submitted
- `is_top_score`: boolean that indicates whether the current upload achieved an equal or higher score than the current best solution of the team
- `remaining_submissions_today`: number of submissions that the team can still do on the given day (CET timezone)
- `lines_skipped`: array of line numbers that were skipped / not processed
- Response codes: 
  + `200` OK (currently, a 200 is also returned when the no submissions are possible anymore according to `remaining_submissions_today`, i.e. check whether `remaining_submissions_today > 0` before submitting)
  + `400` Bad Request (e.g. if the solution file could not be parsed properly)
  + `401` Unauthorized (in case the access token is no longer valid or was not properly set in the Header of the request)


## Online Evaluation

The APIs for the online evaluation (see also: [details about online evaluation procedure](https://github.com/recsyschallenge/2017/tree/master/online-evaluation)) can only be used by those teams that are approved for the online challenge. The API endpoints below, require again an access token that can be generated on the [team details page (access token)](https://recsys.xing.com/team) and is different from the token that was used for the offline challenge: 

<img src="images/teams-access-tokens.png" width="450px" />

All requests need to mention the access token as part of the HTTP authorization header, e.g.: 

```
curl -XGET -H 'Authorization: Bearer RGF0...A2OQ==' 'https://recsys.xing.com/api/online/data/status'
```

`RGF0...A2OQ==` is the access token that can be (re-)generated on [recsys.xing.com/team](https://recsys.xing.com/team). The token is valid throughout the online challenge (in case it is not regenerated by the owner of the team). If a team overloads the API then the token will be disabled. 

### GET /api/online/data/status

Once a day, a new dataset is released. We strongly encourage the teams to download the dataset only once per day. `GET /api/online/data/status` should be called to get to know whether the new dataset is ready to be downloaded. The dataset will then contain:  

- new items that should be pushed to as recommendations to users (see: [GET /api/online/data/items](#get-apionlinedataitems))
- new target users for your team (see: [GET /api/online/data/users](#get-apionlinedatausers))  
- updated interaction data (see: [GET /api/online/data/interactions](#get-apionlinedatainteractions))


#### Example

Get status:

```
curl -XGET -H 'Authorization: Bearer RGF0...A2OQ==' 'https://recsys.xing.com/api/online/data/status'
```

Response: 

```javascript
{
  "current": {
    "num_items":10927,
    "updated_at":"2017-03-29T04:20:23.000+02:00"
  }
}
```

Notes: 

- Attributes: 
  + `num_items`: number of new items that can be recommended to the users for whom the team is responsible 
  + `updated_at`: timestamp when the data was exported so that it can be downloaded
- Teams need to and should download the data only once per day. `GET /api/online/data/status` can be polled e.g. every 5 minutes to get to know when the new data is available (as soon as `updated_at` corresponds to the current date, teams can download the new datasets).


### GET /api/online/data/items

Downloading the new target items (including details) that teams can push as recommendations to their users. Those target items will be _new_ job posting that typically were published on xing.com within the last 24 hours. 

#### Example

Download target items: 

```
curl -XGET -H 'Authorization: Bearer RGF0...A2OQ==' 'https://recsys.xing.com/api/online/data/items'
```

Response is a tab-separated text file: 

```
id  title career_level  discipline_id industry_id country is_payed  region  latitude  longitude employment  tags  created_at
30    3 15  9 de  0 7 50.8  8.9 1 3323880,4078788,1025029,88816,1032508,2922746,2282775,878709  1450216800
70  2994300,665762,901938,127655,3680343  3 5 18  de  0 1 48.7  9.01127655,3680343,366525,2114599,901938,2994300,665762,427470,3284568,3175069,792161,3671787,1023516 1475791200
...
```

Notes: 

- the format of the file corresponds to the one of the _items.csv_ file that was used during the offline challenge
- description of columns, see: [Dataset / Items](http://2017.recsyschallenge.com/#dataset-items)


### GET /api/online/data/users

Get the list of target user IDs for the given day. Each day, the team will get a new list of target users to whom they are allowed to push the new items as recommendations. The target users do not overlap between the teams, i.e. each team will get a dedicated list of target users. 

#### Example

Get target user IDs: 

```
curl -XGET -H 'Authorization: Bearer RGF0...A2OQ==' 'https://recsys.xing.com/api/online/data/users'
```

Example response

```
726
172
98
1009
...
```

Notes: 

- each line features one target user ID
- the target user IDs refer to the users that are part of the dataset that is released to the teams at the beginning of the online challenge


### GET /api/online/data/interactions

Download the updated interaction data. The tab-separated file (format see: [Dataset / Interactions](http://2017.recsyschallenge.com/#dataset-interactions)) will contain also the interaction data from the last day (for which a team possibly pushed already recommendations). 

#### Example

Example request: 

```
curl -XGET -H 'Authorization: Bearer RGF0...A2OQ==' 'https://recsys.xing.com/api/online/data/interactions'
```

Response is a tab-separated text file: 

```
user_id item_id interaction_type  created_at
2082156 80  1 1484299172
1934123 140 1 1486388563
1320213 240 1 1479409825
297303  310 1 1484817366
1635596 310 1 1486370081
857319  340 1 1485121421
```

Format: [Dataset / Interactions](http://2017.recsyschallenge.com/#dataset-interactions)


## POST /api/online/submission

Upload recommendations for the [target users](#get-apionlinedatausers) of the team. The format of the submission is the same as the format of the solutions during the offline challenge: 

```
item_id     user_ids
762817      46271, 18262, 81725, 18236, 49762, 61726
172         7612, 65182
67816       78161, 97615, 89010, 176241, 18651, 49785, 59872, 67
...
```

Notes: 

- `item_id` and `user_ids` have to be separated by tab or whitespace (the first number is interpreted as item ID and all following IDs are interpreted as the IDs of users/candidates to whom the item should be recommended).
  + `item_id` has to be one item from the current items, see: [GET /api/online/data/items](#get-apionlinedataitems)
  + `user_ids` have to be IDs from users that are part of the current target users of the team, see: [GET /api/online/data/users](#get-apionlinedatausers)
- `user_ids` do not need to be sorted
- For each item, we accept at maximum 250 users (we cut off after 250 users).
- Important difference to the offline evaluation: 
  + each user may receive at maximum 1 recommendation per day. 
  + Hence, the submission file must not contain a user twice. 
  + We strongly encourage the teams to not spam users with recommendations (ie. no best guess, no randomness, etc.). It is perfectly fine to not recommend items to all of the current target users.  
  + Background: users will receive push notifications once a recommendation is pushed to them and we do not want to bother the users more than once per day. You should thus wisely decide whether you want to push an item as recommendation and, if so, which item. 
- `POST /api/online/submission` can be called more than once per day (at maximum 1000 times per day), i.e. recommendations can be submitted in smaller batches. However, the first recommendation that is pushed to a user _wins_, i.e. if a first file already contained a row such as `42  78,728,97` then the following submissions should not contain the user IDs `78,728,97` because those users already got their _recommendation of the day_ (additional recommendations to those users on the same day will be neglected).

#### Example

Example request: 

```
curl -XPOST -H 'Authorization: Bearer RGF0...A2OQ==' 'https://recsys.xing.com/api/online/submission' --data-binary @submission-2017-05-01.csv
```

Example response:

```
{"num_accepted_recos": 17827}
```

The `num_accepted_recos` is the number of user-item pairs that were successfully accepted and were sent to XING's push recommendation component. 

## GET /api/online/submission

Download the submission of the team for the current day. This endpoint is rather for the teams to cross-check which of the recommendations that were submitted by the team via [POST /api/online/submission](#post-apionlinesubmission) were accepted and have been further processed by XING's push recommendation component. 

#### Example

Example request: 

```
curl -XGET -H 'Authorization: Bearer RGF0...A2OQ==' 'https://recsys.xing.com/api/online/submission' 
```

Example response:

```
854173  52381
816205  71625, 17353, 881
701204  162, 91826
712783  928361
773903  1023
654400  837361
...
```
