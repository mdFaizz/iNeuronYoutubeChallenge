# iNeuronYoutubeChallenge

Link of the Challenge description: https://drive.google.com/file/d/1UcmG5-QLQKz57iyY6g6v9vLrmVZ4LIWf/view?usp=sharing

Modules:
1.  Pandas
2.  MySql
3.  bs4
4.  requests
5.  google-api-client
6.  json
7.  pytube
8.  Flask
9.  pymongo


Execution description:
1.  Flask framework paired with HTML and css was used to create a website for the front end.
2.  web scraping and google-api-client was used to fetch youtube data.
3.  MySQL and MongoDB was used to store the data of 4 youtubers.


# Links:
# heroku: https://ineuronyoutubechallengefaizan.herokuapp.com/
# azure: https://ineuronyoutubechallengefaizan.azurewebsites.net
# aws: http://ineuronyoutubechallengefaizan-env-1.eba-qmpvnbep.ap-southeast-1.elasticbeanstalk.com/

Deviations/Improvements from actual scope:
1.  videos for the 4 youtubers were supposed to be downloaded and stored in S3 or G-drive and a link to download was supposed to be added in the table, but since the videos needed upto 15 GB space this was not done. Instead pytube module was used to directly download the video to local on a single button click (also making to generic and available for all the videos on Youtube)
2.  MongoDB was only supposed to hold the comments and thumbnail data, instead all the other data was also uploaded for learning and back-up purposes.

How to Use:
1.  Refer video:- 

or

1.  Open any of the above links in your browser.

2.  Copy-Paste the youtube channel url in the input section.

3.  Click the "Check" button to verify the URL.

4.  If "Channel Id found" is displayed proceed or else please check the URL and try again.

5.  select the number of videos to load (min- 1 and max-50)

6.  Click "Submit" button, a new window is opened showing the results.

7.  Details include (for each row):

  a.  Video Thumbnail
  
  b.  Video Title (along with link to the youtube video) (clicking it opens the video in Youtube)
  
  c.  Video published data and time
  
  d.  view count
  
  e.  like count
  
  f.  comment count with link to open all the comments (clicking this opens a new window displaying all the comments on the video)
  

8.  Download Link (clicking this link downloads the video with the Video ID name and *.mp4 format)


# Image previews:

![image](https://user-images.githubusercontent.com/49452105/189480486-1bed21f3-1b93-42f3-98d5-ee3cd60cf8cc.png)

![image](https://user-images.githubusercontent.com/49452105/189480496-5f9e60ca-fe93-4a59-8c3f-1b57f8aeb933.png)

![image](https://user-images.githubusercontent.com/49452105/189480501-20cbf384-c6b1-4734-8c60-4aefd08fc8c1.png)

![image](https://user-images.githubusercontent.com/49452105/189480845-05af86a2-eac0-44f9-a0e3-2587ec59f43a.png)


# MySQL database table:
![image](https://user-images.githubusercontent.com/49452105/189480567-fa83abb5-e45a-4c86-a38a-4cc67f6c41b8.png)


# MongoDB data:
![image](https://user-images.githubusercontent.com/49452105/189480746-42793d34-ce4b-4a4b-b412-95d22baf79d1.png)

![image](https://user-images.githubusercontent.com/49452105/189480786-c178ed70-bf37-4137-ba6b-fa249353ecb5.png)

![image](https://user-images.githubusercontent.com/49452105/189480806-7ce0712f-f82c-4225-8cad-1d642d93b5a3.png)


