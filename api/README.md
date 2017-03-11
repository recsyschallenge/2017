Submission System API (alpha version)
=====================

The API should allow teams to automate their recommender systems and particularly the process of 
downloading data (relevant for online challenge) and uploading solutions. 

Current list of endpoints: 

- [GET /api/team](#get-apiteam)
- [POST /api/submission](#post-apisubmission)

## GET /api/team

Get team details. 

### Example request

```
curl -vv -XGET -H 'Authorization: Bearer RAtN...LTA1NjkyOGU5OTE5Mw==' 'https://recsys.xing.com/api/team'
```

Notes: 

- `RAtN...LTA1NjkyOGU5OTE5Mw==` is the access token of the team. It can be generated on the [team details page (access token)](https://recsys.xing.com/team).


### Example response

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
  
## POST /api/submission

Uploads a new solution for the team.

### Example request

```
curl -vv -XPOST -H 'Authorization: Bearer RAtN...LTA1NjkyOGU5OTE5Mw==' 'https://recsys.xing.com/api/submission?label=test42%20(time-decay)' --data-binary @solution_file.csv
```

Notes: 

- `RAtN...LTA1NjkyOGU5OTE5Mw==` is the access token of the team. It can be generated on the [team details page (access token)](https://recsys.xing.com/team).
- `label`: optional label that should be assigned to the submission (won't be visible to other teams)
- `solution_file.csv` is the actual solution file that should be uploaded. See: [Format instructions](https://recsys.xing.com/submission#instructions)

### Example response

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
  + `200` OK
  + `400` Bad Request (e.g. if the solution file could not be parsed properly)
  + `401` Unauthorized (in case the access token is no longer valid or was not properly set in the Header of the request)
