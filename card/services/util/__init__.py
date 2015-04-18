from google.appengine.ext import ndb

def _tokenize_string(phrase):
  tokens = []
  for word in phrase.split():
    min_token = 3
    if len(word) > min_token:
      token_size = min_token
      while len(word) >= token_size:
        tokens.append(word[0:token_size])
        token_size += 1
  return tokens

def _save_batch(index, cards, documents):
  index.put(documents)
  ndb.put_multi(cards)