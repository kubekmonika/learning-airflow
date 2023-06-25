# Knowledge

In this chapter, we look indepth at what operators represent, what they are, how they function, and when and how they are executed. We also demonstrate how operators can be used to communicate with remote systems via hooks, which allows you to perform tasks such as loading data into a database, running a command in a remote environment, and performing workloads outside of Airflow.

# Exercies example

Throughout this chapter, we will work out several components of operators with the help of a (fictitious) stock market prediction tool that applies sentiment analysis, which we’ll call StockSense. Wikipedia is one the largest public information resources on the internet. Besides the wiki pages, other items such as pageview counts are also publicly available. For the purposes of this example, we will apply the axiom that an increase in a company’s pageviews shows a positive sentiment, and the company’s stock is likely to increase. On the other hand, a decrease in pageviews tells us a loss in interest, and the stock price is likely to decrease.
