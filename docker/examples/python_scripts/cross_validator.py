from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.sql import SparkSession

import time


spark = SparkSession \
	.builder \
	.appName("CrossValidatorExample") \
	.getOrCreate()

# Prepare training documents, which are labeled.
training = spark.createDataFrame([
	(0, "a b c d e spark", 1.0),
	(1, "b d", 0.0),
	(2, "spark f g h", 1.0),
	(3, "hadoop mapreduce", 0.0),
	(4, "b spark who", 1.0),
	(5, "g d a y", 0.0),
	(6, "spark fly", 1.0),
	(7, "was mapreduce", 0.0),
	(8, "e spark program", 1.0),
	(9, "a e c l", 0.0),
	(10, "spark compile", 1.0),
	(11, "hadoop software", 0.0)
], ["id", "text", "label"])

# Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
lr = LogisticRegression(maxIter=10)
pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

# We now treat the Pipeline as an Estimator, wrapping it in a CrossValidator instance.
# This will allow us to jointly choose parameters for all Pipeline stages.
# A CrossValidator requires an Estimator, a set of Estimator ParamMaps, and an Evaluator.
# We use a ParamGridBuilder to construct a grid of parameters to search over.
# With 3 values for hashingTF.numFeatures and 2 values for lr.regParam,
# this grid will have 3 x 2 = 6 parameter settings for CrossValidator to choose from.
paramGrid = ParamGridBuilder() \
	.addGrid(hashingTF.numFeatures, [10, 100, 1000, 5000]) \
	.addGrid(lr.regParam, [0.1, 0.01, 0.01]) \
    .addGrid(lr.threshold, [0.2, 0.5, 0.7]) \
	.addGrud(lr.maxIter, [10, 100, 1000, 5000]) \
	.build()

crossval = CrossValidator(estimator=pipeline, estimatorParamMaps=paramGrid,
                          evaluator=BinaryClassificationEvaluator(), numFolds=5)

# Run cross-validation, and choose the best set of parameters.
start_time = time.time()
cvModel = crossval.fit(training)
end_time = time.time()
print("The cross validation and hyperparameter search took: ", end_time - start_time, " seconds")

# Prepare test documents, which are unlabeled.
test = spark.createDataFrame([
	(4, "spark i j k"),
	(5, "l m n"),
	(6, "mapreduce spark"),
	(7, "apache hadoop")
], ["id", "text"])

# Make predictions on test documents. cvModel uses the best model found (lrModel).
prediction = cvModel.transform(test)
selected = prediction.select("id", "text", "probability", "prediction")
for row in selected.collect():
	print(row)