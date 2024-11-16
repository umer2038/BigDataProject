# -*- coding: utf-8 -*-
"""model_training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ckBug9892fprbFSgshFfZJqMOBji6eaX
"""

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

def train_recommendation_model(spark, features_file):
    """
    Trains a recommendation model using collaborative filtering with Alternating Least Squares (ALS).

    Parameters:
        spark (SparkSession): Spark session object.
        features_file (str): Path to the CSV file containing extracted features.
    """
    # Load features data
    features_df = spark.read.csv(features_file, header=True, inferSchema=True)

    # Define assembler to create feature vector
    assembler = VectorAssembler(inputCols=["feature1", "feature2", ...], outputCol="features")
    data = assembler.transform(features_df)

    # Split data into training and test sets
    (training_data, test_data) = data.randomSplit([0.8, 0.2])

    # Initialize ALS model
    als = ALS(maxIter=5, regParam=0.01, userCol="user_id", itemCol="track_id", ratingCol="rating",
              coldStartStrategy="drop")

    # Fit ALS model to training data
    model = als.fit(training_data)

    # Evaluate model on test data
    predictions = model.transform(test_data)
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
    rmse = evaluator.evaluate(predictions)

    print("Root Mean Squared Error (RMSE) = " + str(rmse))

    # Save model
    model.save("recommendation_model")

def main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("MusicRecommendationModel") \
        .getOrCreate()

    # Path to the CSV file containing extracted features
    features_file = 'extracted_features.csv'

    # Train recommendation model
    train_recommendation_model(spark, features_file)

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    main()