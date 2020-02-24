import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os
from TextNLP import TextNLP

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		# consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXX'
		# consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		# access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		# access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
		consumer_key = "ljmfx8E61O5AvzBh4JAwBfQjq"
		consumer_secret = "CEAFpOzu4epH4oblxvKGuVkiF50t6SgvLqiQKKxXbbeypS6mYf"
		access_token = "1227275607437869056-HTP3vPH66pvH8so81pHQoIvdpMr44V"
		access_token_secret = "bCVAXdKLANmGlEEyLcoWbZdY9XU1ILoxitetLaAqT839g"

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		textNLP = TextNLP()
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return textNLP.textPreProcessingOnlyAlphabetic(tweet)

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob( tweet)
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.user_timeline(screen_name='AccessibleGC', count=200,
												 include_rts=True,
												 tweet_mode='extended')

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = self.clean_tweet(tweet.full_text)
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(parsed_tweet['text'] )

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	# calling function to get tweets
	tweets = api.get_tweets(query = 'Donald Trump', count = 500)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	# percentage of neutral tweets
	print("Neutral tweets percentage: {} " .format(100* (len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

	# printing first 5 positive tweets
	print("\n\nPositive tweets:")
	for tweet in ptweets[:10]:
		print(tweet['text'])

	# printing first 5 negative tweets
	print("\n\nNegative tweets:")
	for tweet in ntweets[:10]:
		print(tweet['text'])


#Print
	OUTPUT_FILE = "AccessibleGC.csv"

	if os.path.exists(OUTPUT_FILE):
		os.remove(OUTPUT_FILE)
	out = open(OUTPUT_FILE, mode='w')
	out.write('tweet title,sentiment')
	for tweet in ptweets:
		out.write("\n"+tweet['text'] +",Positive")
	for tweet in ntweets:
		out.write("\n"+tweet['text'] +",Negative")
	for tweet in [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']:

		out.write("\n" + tweet['text'] + ",Neutral")
	out.close()  # close file
	print(len(tweets))
	show_wordcloud(ntweets)

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
stopwords = set(STOPWORDS)

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title:
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()



if __name__ == "__main__":
	# calling main function
	main()

