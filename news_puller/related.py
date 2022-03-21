from sklearn.metrics.pairwise import euclidean_distances


def calculate_similarity(new, data):
  similarity_collection = []
  
  for compare_to in data:
    distance = euclidean_distances(new['topics'], compare_to['topics'])[0][0]

    if distance < 4:
      print("Distance ====> %d " % distance)
      compare_to['distance'] = distance
      similarity_collection.append(compare_to)

  sort_by_distance = sorted(similarity_collection, key=lambda d: d['distance']) 

  print('****** Text Similarity::Ending ******')

  return sort_by_distance[:16]

