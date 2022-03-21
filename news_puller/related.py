from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances


def calculate_similarity(new, data):
  similarity_collection = []
  vectorizer = CountVectorizer()
  
  for compare_to in data:
    corpus = []
    corpus.append(new['title'])
    corpus.append(compare_to['title'])
    features = vectorizer.fit_transform(corpus).todense()

    distance = euclidean_distances(features[0],features[1])[0][0]

    if distance < 4:
      print("Distance ====> %d " % distance)
      compare_to['distance'] = distance
      similarity_collection.append(compare_to)

  sort_by_distance = sorted(similarity_collection, key=lambda d: d['distance']) 

  print('****** Text Similarity::Ending ******')

  return sort_by_distance[:16]

