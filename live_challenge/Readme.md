Live Challenge
----------------

##Online Data Description:

+ Xing releases user information once:
	- Xing hands out X users with their respective profile information
	- The user information contains the same fields as released in the offline challenge
	- The user information is not updated during the challenge
	- The set of users doesn't change during the challenge

+ Xing releases target users once per day:
	- Every day we hand out a set of K target users for each team
	- The set of target users is a subset of the released users
	- Each team will get a different target user set every day
	- Teams can only submit recommendations for those users

+ Xing releases item information once per day:
	- Every day we hand out Y new items to be recommended by the teams to their target users
	- The item information will contain the same information as released in the offline challenge
	- The items can only be recommended for 24 hours after the release

+ Xing releases interactions from previous day, once a day:
	- Every day we hand out all recommendations that were played out
	- The interactions can be of the following type:
		* User Click
		* User Delete
		* User Bookmark / Reply Intention
		* User Delete
		* Recruiter interest
		* Team Impression 
		* Xing Decline
	- The user interactions are the same as in the offline challenge
	- The team's impression indicate that a team attempted a recommendation (the team is not known)
	- A xing decline is an indicator that our recommender filtered the recommendation out. That means that we do not guarantee that all recommendations are shown to the user

##Recommendations:
	
+ After the teams received the daily data dump and their target users:
	- The teams have 24 hours to submit their recommendations.
	- The target users change every day.
	- The items change every day.

+ Recommendations:
	- Every team can submit one recommendation per target user that day		
	- There is no guarantee that the recommendation is player out since each item has to pass our recommendation filters.
	- A recommendation is valid for 7 days. In other words means once played out we count interactions with the item for one week
		  extactly afer the release. Afterwards the interaction does not count into a teams score.

+ The scoring function stays the same as in the offline challange:
	- Clicks, Bookmarks / Reply Intentions, Recruiter interest count positive towards the teams score.
	- Deletes count negative towards the score.
	- Unclicked impressions or declines do not influence the score.

+ Winning:
	- The winner of the challenge is announced one week after the final submission
	- Per week the score is summed over all recommendations
	- The final score for a team is the sum of their best two weeks
