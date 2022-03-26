from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances


def join_topics(new):
  return ' '.join([n.get("name") for n in new['topics']])


def calculate_similarity(new, data):
  similarity_collection = []
  vectorizer = CountVectorizer()
  new_topics = join_topics(new)

  for compare_to in data:
    corpus = []
    corpus.append(new_topics)
    corpus.append(join_topics(compare_to))
    print("topics to campare::: ", corpus)
    features = vectorizer.fit_transform(corpus).todense()

    distance = euclidean_distances(features[0],features[1])[0][0]

    if distance < 4:
      compare_to['distance'] = distance
      similarity_collection.append(compare_to)

  sort_by_distance = sorted(similarity_collection, key=lambda d: d['distance']) 

  return sort_by_distance[:16]
