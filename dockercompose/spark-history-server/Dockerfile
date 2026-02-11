# Use the official Spark 4.0.1 image
FROM apache/spark:4.0.1

# Switch to root to manage jars
USER root

# Spark 4.0.1 is pre-built with Hadoop 3.4
ARG HADOOP_VERSION=3.4.0
# AWS SDK V2 version compatible with Hadoop 3.4.0
ARG AWS_SDK_V2_VERSION=2.23.19

WORKDIR /opt/spark/jars/

# 1. Download the Hadoop-AWS connector (for Hadoop 3.4)
RUN curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar

# 2. Download the AWS Java SDK V2 Bundle (Required for Hadoop 3.4+)
# Note: The artifact ID changed from 'aws-java-sdk-bundle' to 'bundle' under the new namespace
RUN curl -O https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_V2_VERSION}/bundle-${AWS_SDK_V2_VERSION}.jar

# Switch back to the default spark user
USER spark