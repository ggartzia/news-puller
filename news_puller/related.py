from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances


def get_distance(new, compare):
  vectorizer = CountVectorizer()

  corpus = []
  corpus.append(' '.join(new['topics']))
  corpus.append(' '.join(compare['topics']))
  features = vectorizer.fit_transform(corpus).todense()

  return euclidean_distances(features[0],features[1])[0][0]


def calculate_similarity(new, data):
  similarity_collection = []
  for compare_to in data:
    distance = get_distance(new, compare_to)

    if distance < 4:
      compare_to['distance'] = distance
      similarity_collection.append(compare_to)

  sort_by_distance = sorted(similarity_collection, key=lambda d: d['distance']) 

  return sort_by_distance[:16]
