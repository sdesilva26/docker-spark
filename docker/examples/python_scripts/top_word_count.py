from __future__ import print_function

import sys
import time
from operator import add

from pyspark.sql import SparkSession

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("Usage: top_word_count.py AZURE_STORAGE_ACCOUNT_NAME "
		      "AZURE_STORAGE_ACOCUNT_ACCESS_KEY CONTAINER_NAME FILE_NAME", file=sys.stderr)
		sys.exit(-1)

	spark = SparkSession.builder.appName("PythonWordCount").getOrCreate()

	spark.conf.set("fs.azure.account.key.{}.blob.core.windows.net".format(sys.argv[1]),
		"{}".format(sys.argv[2]))
	start_time = time.time()
	lines = spark.read.text(
		"wasbs://{}@{}.blob.core.windows.net/{}".format(sys.argv[3], sys.argv[1],
			sys.argv[4])).rdd.map(lambda r: r[0])
	counts = lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add).map(
		lambda x: (x[1], x[0])).sortByKey(False)

	output = counts.take(100)
	print("The 100 most frequent words are :\n")
	i = 1
	for count, word in output:
		print("{}. {} ---> {}".format(i, word, count))
		i += 1

	end_time = time.time();

	print("Query took {:0.2f} seconds".format(end_time - start_time))
	print("Number of unique words in file {}".format(counts.count()))
	spark.stop()
