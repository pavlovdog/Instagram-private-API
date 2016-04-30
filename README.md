### Python's lib for using Instagram's private API
==================================================

#### List of abilities
- Upload photo with captions
- Get info about a user
- Get list of user's medias (with pagination)
- Get list of user's followers
- Get list of user's followings
- Follow/unfollow users

#### Example
```python
from api import privateAPI

api = privateAPI(username = "potekhinthebest", password = "potekhin")

# Basic info about user
response = api.userInfo(user_id = "427553890")
info = response.json()

print ("USERNAME: ", info["user"]["username"])
# USERNAME:  leomessi

# Upload image. !!! Image must be square and have JPG format !!!
api.upload("path_to_image/image.jpg", "Description for image \n #hot #hacker #wow")

# Follow/unfollow user
api.follow(user_id = "427553890")
api.unfollow(user_id = "427553890")

# List of followers without max_id parameter (necessary for pagination)
response = api.listFollower(user_id = "427553890")
list_followers = response.json()

# List of followings with pagination
response = api.listFollowing(user_id = "427553890") # First page
list_followings = response.json()
next_max_id = list_followings["next_max_id"]

response = api.listFollowing(user_id = "427553890", max_id = next_max_id) # Second page

# List of user's media with pagination
response = api.userMedia(user_id = "427553890") # First page
next_max_id = response.json()["items"][-1]["next_max_id"]

response = api.userMedia(user_id = "427553890", max_id = next_max_id) # Second page
media_list = response.json()
```
