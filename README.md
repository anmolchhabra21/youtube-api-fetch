## Youtube API Search

#### Goal: To make an API to fetch the latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.
      
The backend Flask server asynchronously calls the yt-API to fetch the latest videos in reverse chronological order, stores them in the database, and we can access the resources by starting the app and heading over to a route like `http://localhost:5000/videos?page=3&per_page=10`, that is paginated.
## Bonus Points

- Added support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the following available key.
- The dashboard lets you view the stored videos with pagination on the front end.
- Docker and requrirements.txt included, so no time and extra dependency cluster to be faced while setting up locally.       
- Added pdAdmin support, to visualize and query the db on the go.

### ScreenShots: 
![image](https://github.com/anmolchhabra21/youtube-api-fetch/assets/93809908/e094cd49-b747-428f-beed-85ab67cc9c6d)
