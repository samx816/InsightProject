# GamePost

As Data Engineering Fellows at Insight Data Science, we were given
3 weeks to design and implement a project that demonstrates
knowledge of a data pipeline and distributed platforms. The result of my work
during this time is my project, GamePost.

GamePost is a tool that streams data from social media (more specifically Twitter)
and processes the tweets to determine a count of game mentions for certain
game titles. Furthermore, GamePost can tell the user how many mentions of a title were made
during a specific time period. This has many uses for the entertainment industry, some of them being: 
for analyzing the effectiveness of an advertisement method, to determine whether 
a product's release date coincides with a more popular product from a competitor 
company, and to guide marketing resources.

<h2>How it Works</h2>
GamePost takes the data from Twitter and puts it into a Kinesis stream, where AWS Lambda
will extract and process the data. There can be as many Lambda functions as there are
shards in a stream, and AWS Lambda can also process the data in mini batches. The relevant
results are then stored in Amazon DynamoDB for future queries. This serverless architecture
makes maintenance very light and the work of data engineers simpler. Without having to
worry about servers and clusters, engineers can complete projects faster, resulting in 
greater productivity.
