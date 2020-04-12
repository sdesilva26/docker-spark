from __future__ import print_function

import sys
from operator import add
import time

from pyspark.sql import SparkSession


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: wordcount <file>", file=sys.stderr)
		sys.exit(-1)

	spark = SparkSession \
		.builder \
		.appName("PythonWordCount") \
		.getOrCreate()
	start_time = time.time()
	lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
	counts = lines.flatMap(lambda x: x.split(' ')) \
		.map(lambda x: (x, 1)) \
		.reduceByKey(add) \
		.map(lambda x: (x[1], x[0])) \
		.sortByKey(False)

	output = counts.take(100)
	print("The 100 most frequent words are :\n")
	for (count, word) in output:
		print("{} ---> {}".format(word, count))

	end_time = time.time();

	print("Query took {:0.2f} seconds".format(end_time - start_time))
	print("Number of unique words in file {}".format(counts.count()))
	spark.stop()