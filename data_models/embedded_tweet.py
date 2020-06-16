"""This class creates the object structure for Embedded Tweet content"""

from data_models.contents import ContentType, _Content


class ETweet(_Content):
    """This class creates Embedded Tweet object"""

    def __init__(self, tweet_id):
        super(ETweet, self).__init__(ContentType.EMBEDDED_TWEET)
        self.tweet_id = tweet_id
