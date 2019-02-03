## Part 1: Part-of-speech tagging

Natural language processing (NLP) is an important research area in artificial intelligence, dating
back to at least the 1950’s. One of the most basic problems in NLP is part-of-speech tagging, in
which the goal is to mark every word in a sentence with its part of speech (noun, verb, adjective,
etc.). This is a first step towards extracting semantics from natural language text.

Her position covers a number of daily tasks common to any social director.
DET NOUN VERB DET NOUN ADP ADJ NOUN ADJ ADP DET ADJ NOUN
where DET stands for a determiner, ADP is an adposition, ADJ is an adjective, and ADV is an
adverb.1 Labeling parts of speech thus involves an understanding of the intended meaning of the
words in the sentence, as well as the relationships between the words.

What to do. Your goal in this part is to implement part-of-speech tagging in Python, using Bayes
networks.
1. First you’ll need to estimate the probabilities of the HMM above, namely P (S1), P (Si+1jSi),
and P (WijSi). To do this, use the labeled training file we’ve provided.

2. Your goal now is to label new sentences with parts of speech, using the probability distributions learned in step 1. To get started, consider the simplified Bayes net in Figure 1(b).
To perform part-of-speech tagging, we’ll want to estimate the most-probable tag s∗ i for each
word Wi

3. Now consider the Bayes net of Figure 1(a), which is a richer model that incorporates dependencies between words. Implement the Viterbi algorithm to find the maximum a posteriori
(MAP) labeling for the sentence { i.e. the most likely state sequence

4. Consider the Bayes Net of Figure 1c, which is a better model of language because it incorporates some longer-term dependencies between words. It’s no longer an HMM, so one
can’t use Viterbi, but we can use MCMC. Write code that uses MCMC to sample from theposterior distribution of Fig 1c, P (SjW ), after a warm-up period, and shows five sampled
particles. Then estimate the best labeling for each word (by picking the maximum marginal
for each word, s∗ i = arg maxsi P (Si = sijW ); as in step 2).
