import os
   import tweepy
   import time
   from dotenv import load_dotenv

   load_dotenv()

   # Twitter API credentials
   CONSUMER_KEY = os.getenv('CONSUMER_KEY')
   CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
   ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
   ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

   # Authenticate to Twitter
   auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
   auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
   api = tweepy.API(auth, wait_on_rate_limit=True)

   def process_mentions(since_id):
       print("Checking for mentions...")
       new_since_id = since_id
       
       try:
           # Get mentions
           mentions = api.mentions_timeline(since_id=since_id, tweet_mode='extended')
           
           for mention in reversed(mentions):
               new_since_id = max(mention.id, new_since_id)
               username = mention.user.screen_name
               status_id = mention.id
               
               # Create response
               response = f"@{username} Thanks for mentioning me! How can I help you today? 😊"
               
               # Reply to mention
               api.update_status(
                   status=response,
                   in_reply_to_status_id=status_id
               )
               print(f"Replied to {username}")
               
       except tweepy.TweepError as error:
           print(f"Error: {error}")
       
       return new_since_id

   def main():
       since_id = None
       while True:
           since_id = process_mentions(since_id)
           print("Waiting for next check...")
           time.sleep(60)  # Check every 60 seconds

   if __name__ == "__main__":
       main()
