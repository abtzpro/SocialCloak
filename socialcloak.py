import facebook
import tweepy
import re


# Your access token from Facebook
FACEBOOK_ACCESS_TOKEN = '<your_access_token_here>'

# The user ID of the account you want to scrub
FACEBOOK_USER_ID = '<user_id_here>'

# Regex patterns for identifying PII
PHONE_REGEX = r'(\d{3})[-. ]?(\d{3})[-. ]?(\d{4})'
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Initialize the Graph API
facebook_graph = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN, version="3.0")

# Get the user's profile information
facebook_profile = facebook_graph.get_object(FACEBOOK_USER_ID)

# Get the user's posts
facebook_posts = facebook_graph.get_connections(facebook_profile['id'], 'posts')

# Loop through the posts and delete any with PII or potentially negative content
for post in facebook_posts['data']:
    # Check for PII in the post's message
    if re.search(PHONE_REGEX, post['message']) or re.search(EMAIL_REGEX, post['message']):
        # Delete the post
        facebook_graph.delete_object(post['id'])
    # Check for potentially negative content in the post's message
    elif 'job' in post['message'].lower() or 'interview' in post['message'].lower() or 'fired' in post['message'].lower():
        # Delete the post
        facebook_graph.delete_object(post['id'])
    # Check for potentially negative content in the post's comments
    else:
        comments = facebook_graph.get_connections(post['id'], 'comments')
        for comment in comments['data']:
            if 'job' in comment['message'].lower() or 'interview' in comment['message'].lower() or 'fired' in comment['message'].lower():
                # Delete the comment
                facebook_graph.delete_object(comment['id'])


# Your access token and secret from Twitter
TWITTER_ACCESS_TOKEN = '<your_access_token_here>'
TWITTER_ACCESS_SECRET = '<your_access_secret_here>'

# Your API key and secret from Twitter
TWITTER_API_KEY = '<your_api_key_here>'
TWITTER_API_SECRET = '<your_api_secret_here>'

# Initialize the API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Get the user's timeline
twitter_timeline = twitter_api.user_timeline()

# Loop through the tweets and delete any with PII or potentially negative content
for tweet in twitter_timeline:
    # Check for PII in the tweet's text
    if re.search(PHONE_REGEX, tweet.text) or re.search(EMAIL_REGEX, tweet.text):
        # Delete the tweet
        twitter_api.destroy_status(tweet.id)
    # Check for potentially negative content in the tweet's text
    elif 'job' in tweet.text.lower() or 'interview' in tweet.text.lower() or 'fired' in tweet.text.lower():
        # Delete the tweet
        twitter_api.destroy_status(tweet.id)

print("Social media PII scrubbing complete!")
