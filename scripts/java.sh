#!/bin/sh
mvn -f /scripts/commons-math/ clean compile
ls /scripts/commons-math/
java -jar /scripts/libs/toradocu-1.0-all.jar --target-class org.apache.commons.math3.complex.Complex --source-dir /scripts/commons-math/src/main/java/ --class-dir /scripts/commons-math/target/classes/ --randoop-specs toy-specs.json
ls
java -version
mvn -version