# Adapted from: github.com/aneesha/RAKE/rake.py
from __future__ import division
import operator
import nltk
import string
import re

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

class RakeKeywordExtractor:

  def __init__(self):
    self.stopwords = set(nltk.corpus.stopwords.words()+['/','-'])
    self.top_fraction = 1 # consider top third candidate keywords by score

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []
    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x,
        nltk.word_tokenize(sentence.lower()))
      phrase_list.append(words)
    for phrase in phrase_list:
      for i,ph in enumerate(phrase):
        if ph=='|':
          del phrase[i]
    return phrase_list

  def load_stop_words(self,stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
      for word in line.split():  # in case more than one per line
          stop_words.append(word)
    return stop_words

  def _clean_list(self,bhks_sts_list,rmv_word_list):
    clean_lists = []
    rmv_word_list = rmv_word_list+['']
    for bhk_sts_list in bhks_sts_list:
      cln_list = []
      for element in bhk_sts_list:
        if element not in rmv_word_list:
          cln_list.append(element)
      clean_lists.append(' '.join(cln_list))
    return clean_lists

  def _check_status(self,bhks_list,sts_word_list):
    bhks_sts_list = []
    for bhks in bhks_list:
      bhks_sts = []
      list_sts = []
      for sts in bhks:
        if sts in sts_word_list:
          list_sts.append(sts)
        else:
          bhks_sts.append(sts)
      bhks_sts_list.append(bhks_sts+[' '.join(list_sts)])
    return bhks_sts_list

  def _join_bhks(self,phrase_list):
    no_list = ['one','two','three','four','five','six','seven','eight','nine','ten']
    make_bhk = []
    for phrase in phrase_list:
      make_bhk_list = []
      num_list = ''
      for num,item in enumerate(phrase):
        if (len(item)==1 and isNumeric(item)) or ('.' in item and len(item)==3) or (item in no_list):
          num_list = item
        else:
          make_bhk_list.append(num_list+item)
          num_list = ''
      make_bhk.append(make_bhk_list)
    return make_bhk

  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    for phrase in phrase_list:
      degree = len(filter(lambda x: not isNumeric(x), phrase)) - 1
      for word in phrase:
        word_freq[word] += 1
        word_degree[word, degree] += 1 # other words
    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    # word score = deg(w) / freq(w)
    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]
    return word_scores

  def _calculate_phrase_scores(self, phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        phrase_score += word_scores[word]
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores
    
  def extract(self, text, incl_scores=False):
    self.sts_word_path = '/home/karan/Nexchange/nltk/StatusstopWords.txt'
    self.rmv_word_path = '/home/karan/Nexchange/nltk/rmvstopwords.txt'
    
    sentences = nltk.sent_tokenize(text)
    
    phrase_list = self._generate_candidate_keywords(sentences)

    bhks_list = self._join_bhks(phrase_list)
    
    sts_word_list = self.load_stop_words(self.sts_word_path)
    bhks_sts_list = self._check_status(bhks_list,sts_word_list)
    
    rmv_word_list = self.load_stop_words(self.rmv_word_path)
    cln_bhks_list = self._clean_list(bhks_sts_list,rmv_word_list)

    return cln_bhks_list