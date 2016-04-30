import requests, hmac, uuid, urllib.request, json, hashlib, time

class privateAPI():
    """List of abilities: auth (in __init__), upload, follow, unfollow,
    list of followers, list of followed by,
    set description to media
    In future: write a comment, set like, direct messages"""

    followURL = "https://i.instagram.com/api/v1/friendships/create/{}/"
    unfollowURL = "https://i.instagram.com/api/v1/friendships/destroy/{}/" 
    loginURL = "https://i.instagram.com/api/v1/accounts/login/"
    uploadURL = "https://i.instagram.com/api/v1/media/upload/"
    configureURL = "https://i.instagram.com/api/v1/media/configure/"
    followerListURL = "https://i.instagram.com/api/v1/friendships/{}/followers/"
    followingListURL = "https://i.instagram.com/api/v1/friendships/{}/following/"
    userMediaURL = "https://i.instagram.com/api/v1/feed/user/{}/"
    userInfoURL = "https://i.instagram.com/api/v1/users/{}/info/"

    def __init__(self, username, password):
        self.password = password
        self.username = username
        
        # INITIAL CONFIG
        self.user_agent = 'Instagram 4.1.1 Android (11/1.5.0; 285; 800x1280; samsung; GT-N7000; GT-N7000; smdkc210; en_US)'
        self.guid = str(uuid.uuid1())
        self.device_id = 'android-{}'.format(self.guid)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})

        # LOGIN
        self.data = json.dumps({
            "device_id": self.device_id,
            "guid": self.guid,
            "username": self.username,
            "password": self.password,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })

        self.sig = hmac.new('b4a23f5e39b5929e0666ac5de94c89d1618a2916'.encode('utf-8'), self.data.encode('utf-8'), hashlib.sha256).hexdigest()
        self.payload = 'signed_body={}.{}&ig_sig_key_version=4'.format(
            self.sig,
            urllib.request.quote(self.data)
        )

        self.loginResponse = self.session.post(self.loginURL, self.payload)
        # print "LOGGED IN: ", self.loginResponse.json()

    def upload(self, filename, description):
        # UPLOAD MEDIA
        self.data = {
            "device_timestamp": time.time(),
        }
        self.files = {
            "photo": open(filename, 'rb'),
        }

        self.uploadResponse = self.session.post(self.uploadURL, self.data, files = self.files)
        # print "UPLOAD RESPONSE: ", self.uploadResponse.json()

        self.media_id = self.uploadResponse.json().get("media_id")
        # print "MEDIA ID: ", self.media_id

        # CONFIGURE MEDIA
        self.data = json.dumps({
            "device_id": self.device_id,
            "guid": self.guid,
            "media_id": self.media_id,
            "caption": description or "",
            "device_timestamp": time.time(),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })

        self.sig = hmac.new('b4a23f5e39b5929e0666ac5de94c89d1618a2916'.encode('utf-8'), self.data.encode('utf-8'), hashlib.sha256).hexdigest()
        self.payload = 'signed_body={}.{}&ig_sig_key_version=4'.format(
            self.sig,
            urllib.request.quote(self.data)
        )

        return self.session.post(self.configureURL, self.payload)

    def follow(self, user_id):
        self.data = json.dumps({
            "user_id" : user_id,
            "_uid": self.loginResponse.json()["logged_in_user"]["pk"]
        })

        self.sig = hmac.new('b4a23f5e39b5929e0666ac5de94c89d1618a2916'.encode('utf-8'), self.data.encode('utf-8'), hashlib.sha256).hexdigest()
        self.payload = 'signed_body={}.{}&ig_sig_key_version=4'.format(
            self.sig,
            urllib.request.quote(self.data)
        )

        return self.session.post(self.followURL.format(user_id), self.payload)

    def unfollow(self, user_id):
        self.data = json.dumps({
            "user_id" : user_id,
            "_uid": self.loginResponse.json()["logged_in_user"]["pk"]
        })

        self.sig = hmac.new('b4a23f5e39b5929e0666ac5de94c89d1618a2916'.encode('utf-8'), self.data.encode('utf-8'), hashlib.sha256).hexdigest()
        self.payload = 'signed_body={}.{}&ig_sig_key_version=4'.format(
            self.sig,
            urllib.request.quote(self.data)
        )

        return self.session.post(self.unfollowURL.format(user_id), self.payload)

    def currentUser(self):
        return self.loginResponse.json()

    def listFollower(self, user_id, max_id = ""):
        if not max_id:
            return self.session.get(self.followerListURL.format(user_id))
        else:
            return self.session.get(self.followerListURL.format(user_id), params = {"max_id" : max_id})

    def listFollowing(self, user_id, max_id = ""):
        if not max_id:
            return self.session.get(self.followingListURL.format(user_id))
        else:
            return self.session.get(self.followingListURL.format(user_id), params = {"max_id" : max_id})

    def userMedia(self, user_id, max_id = ""):
        if not max_id:
            return self.session.get(self.userMediaURL.format(user_id))
        else:
            return self.session.get(self.userMediaURL.format(user_id), params = {"max_id" : max_id})
 
    def userInfo(self, user_id):
        return self.session.get(self.userInfoURL.format(user_id))

