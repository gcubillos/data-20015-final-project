The data is separated into several folders. One contains the full texts that will be used to summarize. Another folder contains a gold-standard summary of a text. That is a human generated summary that was found on the internet. Another folder contains the produced-summaries by the text-summarizer.

First, simple small texts will be used to build the summaries. The dataset used for this is D. Greene and P. Cunningham. "Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering", Proc. ICML 2006. The idea is to build several summarizers that can effectively summarize a narrow domain of news articles (taking into account the categories present in the dataset) and then trying to create a consolidated summarizer that can summarize news articles.  Additionally, a functionality of reading articles from internet could 
also be added.

Could be done through an statistical approach and then with the remaining sentences try to compress 
them.