from sklearn.metrics.pairwise import euclidean_distances
from news_puller.db import Database

def calculateDistance(new1, new2):
  return euclidean_distances(new1['topics'], new2['topics'])[0][0]


def calculateSimilarity( new, data_array):
  similarity_collection = []
  
  for idx in data_array:
    compare_to = data_array[idx]
    distance = calculateDistance(new, compare_to)

    if distance < 4:
      print("Distance ====> %d " % distance)
      compare_to['distance'] = distance
      similarity_collection.append(compare_to)

  return similarity_collection

 
def get_related(new):
  print('****** Text Similarity::start ******')
  data_array = Database.select_last_news(48, new['theme'], 0, 500)

  similarity_collection = calculateSimilarity(new, data_array)
  
  sort_by_distance = sorted(similarity_collection, key=lambda d: d['distance']) 
  
   print('****** Text Similarity::Ending ******')
   
  return sort_by_distance[:16]
