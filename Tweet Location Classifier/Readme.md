## Tweet classification

A classic application of Bayes Law is in document classification. Let’s examine one particular classification
problem: estimating where a Twitter \tweet" was sent, based only on the content of the tweet itself. We’ll
use a bag-of-words model, which means that we’ll represent a tweet in terms of just an unordered \bag" of
words instead of modeling anything about its grammatical structure. In other words, a tweet can be modeled
as simply a histogram over the words of the English language (or, more generally, all possible tokens that
occur on Twitter). If, for example, there are 100,000 words in the English language, then a tweet can be
represented as a 100,000-dimensional binary vector, wherein each dimension there is a 1 if the word appears
in the tweet and a zero otherwise. Of course, vectors will be very sparse (most entries are zero).
Implement a Naive Bayes classifier for this problem.
