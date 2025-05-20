#!/bin/sh
echo "Jetzt Commons-Math"
#mvn -f /scripts/commons-math/ clean compile
pwd
cd ..
ls /toradocu/build/libs/

#echo "Jetzt Toradocu"
#cd /scripts/
#git clone git@github.com:albertogoffi/toradocu.git
#cd toradocu/
#./gradlew shadowJar
#echo "Toradocu build complete"

echo "generiere oracle"
java -jar /toradocu/build/libs/toradocu-1.0-all.jar --target-class org.apache.commons.math3.complex.Complex --source-dir /scripts/commons-math/src/main/java/ --class-dir /scripts/commons-math/target/classes/ --randoop-specs /scripts/toy-specs.json
ls
#java -version
#mvn -version