import multiprocessing
import threading
from sklearn.metrics.pairwise import euclidean_distances
from news_puller.db import Database


class SimilarityThread (threading.Thread):
   def __init__(self, threadID, new, data_array, startIndex, totalSize):
   threading.Thread.__init__(self)
   self.threadID = threadID
   self.data_array = data_array
   self.totalSize = totalSize
   self.startIndex = startIndex


   def run(self):
      self.similarity_collection = calculateSimilarity(self.new, self.data_array, self.startIndex, self.totalSize)


def calculateDistance(new1, new2):
  return euclidean_distances(new1['topics'], new2['topics'])[0][0]


def calculateSimilarity( new, data_array, from, to ):
  similarity_collection = {}
  
  for idx in range(from, to):
    compare_to = data_array[idx]
      
    distance = calculateDistance(new, compare_to)

    if distance < 4:
      print("Distance ====> %d " % distance)
      similarity_collection[compare_to['id']] = distance

  return similarity_collection


def processTextSimilarity(new, data_array):
  similarity_collection = {}
  
  num_cores = multiprocessing.cpu_count()
  print(":::num cores ==> %d " % num_cores)
  threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4"]
  threadID = 1;
  threads = []
  rootIndex = round(len(data_array)/4)
  startIndex = 0
  for tName in threadList:
    thread = SimilarityThread(threadID, new, data_array, startIndex, startIndex+rootIndex)
    thread.start()
    startIndex += rootIndex
    threads.append(thread)
    threadID += 1

  # Wait for all threads to complete
  for t in threads:
    t.join()
    similarity_collection.update(t.similarity_collection)
  
  sort_by_distance = sorted(similarity_collection.items(), key=lambda x: x[1], reverse=True)
  
  return sort_by_distance[:16]


def get_related(new):
  print('****** Text Similarity::start ******')
  data_array = Database.select_last_news(48, new['theme'], 0)

  article_similarity = processTextSimilarity(new, data_array)

  print('****** Text Similarity::Ending ******')
  
  return article_similarity
