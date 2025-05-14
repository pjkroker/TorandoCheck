FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies and Java 8
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    curl \
    wget \
    gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Java environment
#ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd4
#ENV PATH=$JAVA_HOME/bin:$PATH

# Install Maven
RUN apt-get update && apt-get install -y maven
RUN readlink -f /usr/bin/java

# Set Maven environment variables
#ENV MAVEN_HOME=/opt/apache-maven-3.9.8
#ENV PATH=$MAVEN_HOME/bin:$PATH

# Verify both work
RUN java -version
RUN mvn -version

#RUN apt-get install -y libgomp1 libblas3 liblapack-dev libopenblas-dev libnd4j-dev


WORKDIR /app
CMD ["bash"]
