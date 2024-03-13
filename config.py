config = {
    "youtube": {
        "query": "football",
        # the interval in which youtube videos will be fetched repeatedly
        "repeatInterval": 10,
        # minimum number of videos that will be fetched atleast when youtube fetch job is scheduled after the first time onwards
        "videosLimitPerRun": 200,
        # minimum number of videos that will be fetched atleast when the youtube fetch job is scheduled for the first time
        "videosLimitFirstTime": 500,
    },
    'database': {
      'host': 'localhost',
      'port': 3306,
      'username': 'myuser',
      'password': 'mypassword',
      'database': 'mydb'
    },
}