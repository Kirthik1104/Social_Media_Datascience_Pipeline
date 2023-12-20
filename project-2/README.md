<html>
<h1>Project Progress</h1>
This project represents progress in several key areas:

<h2>Moderate Hate Speech Analysis:</h2> Conducted an analysis of Moderate Hate Speech on Reddit and 4chan, enhancing the dataset with three new columns: success, class, and confidence. These additions serve to classify comments effectively.

<h2>Data Collection:</h2> Daily data collection from r/politics, capturing an average of approximately 9 comments per day, contributing to an enriched dataset.

<h2>Graph Generation:</h2> Generated crucial graphs in alignment with project requirements, providing visual insights into the dataset's characteristics.

<h2>Sentiment Analysis:</h2> Carried out sentiment analysis, supplementing the findings with an additional graph to deepen understanding and insights into the dataset.

<h3>Note</h3>
Currently, there are 6 background jobs continuously collecting data, updating the moderate hate speech column, and pulling data from the r/politics subreddit.
The jobs are scheduled and managed using <h5>nohup: nohup python3 scheduling.py &</h5> in Linux, ensuring consistent and automated updates to the dataset for ongoing analysis and enhancement.
</html>
