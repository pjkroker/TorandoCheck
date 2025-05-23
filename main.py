import logging
import json
import glob
import os

from docker_helper import DockerHelper
from subproccess_helper import run, run_shell


# Set up basic configuration for logging
logging.basicConfig(
    filename='./output/torando_check.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)
logging.debug("---Starting Setup---")
# PACKAGE = "org.apache.commons.math3.complex"
# METHOD_NAME = "add"
# S_CLASS_NAME = "Complex"
# FQ_CLASS_NAME = "org.apache.commons.math3.complex.Complex"

SEED = "12345"

IMAGE = 'pjkroker/toradocu-x86'
RANDOOP_TIME_LIMIT = "0" #If nonzero, Randoop is nondeterministic
RANDOOP_DETERMINISTIC = "true"
RANDOOP_ATTEMPTED_LIMIT = "10000"


WORKDIR_A = os.path.dirname(__file__)
WORKDIR_R=os.sep + os.path.basename(WORKDIR_A)

REPOSITORY_R = os.path.join(WORKDIR_R, "repository") #TODO Check path if not maven
REPOSITORY_A = os.path.join(WORKDIR_A, "repository")

SOURCEDIR_R = os.path.join(REPOSITORY_R, "src", "main", "java") #TODO Check path if not maven project

CLASSDIR_R = os.path.join(REPOSITORY_R, "target", "classes")#TODO Check path if not maven
CLASSDIR_A = os.path.join(REPOSITORY_A, "target", "classes")

OUTPUTDIR_R = os.path.join(WORKDIR_R, "output")
OUTPUTDIR_A = os.path.join(WORKDIR_A, "output")


logging.debug(f"Absolute paths: Working Directory is: {WORKDIR_A}, Repository to be analyzed is in: {REPOSITORY_A}, Outputs will be in: {OUTPUTDIR_A}")
logging.debug(f"Corresponding relative paths:  Java Source code is in: {SOURCEDIR_R}, Java Class Files are in: {CLASSDIR_R}, Outputs will be in: {OUTPUTDIR_R}")

logging.debug("---Set up Docker---")
docker_helper = DockerHelper()
#build docker image manually from file (replace . with the path to the dockerfile"), container must be x86
#docker build --progress=plain --platform=linux/amd64 -t toradocu-x86 .
logging.debug("---Finishing Setup---")







if __name__ == '__main__':
    error = ""
    logging.info("---1. Load analyzed.json file---")# Contains all information about the method to be analyzed
    with open(os.path.join(WORKDIR_A, "analyzed.json"), 'r') as file:
        analyzed = json.load(file)
    analyzed = analyzed[0]

    PACKAGE = analyzed["package"]
    METHOD_NAME = analyzed["signature"]["name"]
    S_CLASS_NAME = analyzed["parent"]["name"]
    FQ_CLASS_NAME = PACKAGE + "." + S_CLASS_NAME
    CLASS_FILE_A = os.path.join(CLASSDIR_A, FQ_CLASS_NAME.replace(".", os.sep) + ".class")
    logging.debug(f"Generating Tests for: {METHOD_NAME} from {S_CLASS_NAME} in {PACKAGE} (Fully Qualified Class Name is:{FQ_CLASS_NAME})")
    logging.debug(f"Class file should be at: {CLASS_FILE_A}")

    logging.info("---2. Generate Oracles using Toradocu/JDoctor---")
    logging.debug("---2.1. Compile Project")
    result = run_shell(f"mvn -f {REPOSITORY_A} clean package -DskipTests", shell=True)
    logging.debug(result["stdout"])

    logging.debug("---2.2. Generate Oracles---") #TODO Do we need AspectJ file? Is this correct ?"[main] INFO org.toradocu.Toradocu - Oracle generator disabled: aspect generation skipped."
    #container = docker_helper.run_container(IMAGE, "sh /scripts/java.sh", VOLUME_PATH)
    #print(f"java -jar /toradocu/build/libs/toradocu-1.0-all.jar --target-class {FQ_CLASS_NAME} --source-dir {"/jdoc_randoop/repository/src/main/java/"} --class-dir {CLASSDIR_R} --randoop-specs {os.path.join(OUTPUTDIR, "toradocu_oracles.json")}")
    logging.debug(f"Will mount wokrdir on container's filesystem as {os.path.sep + os.path.basename(os.path.normpath(WORKDIR_A))}")
    container = docker_helper.run_container(IMAGE,
                                            f"java -jar /toradocu/build/libs/toradocu-1.0-all.jar --target-class {FQ_CLASS_NAME} --source-dir {"/jdoc_randoop/repository/src/main/java/"} --class-dir {CLASSDIR_R} --randoop-specs {os.path.join(OUTPUTDIR_R, "toradocu_oracles.json")}",
                                            WORKDIR_A, os.path.sep + os.path.basename(os.path.normpath(WORKDIR_A))) # TODO guest path must be linux
    #container = docker_helper.run_container(IMAGE," ls /jdoc_randoop/repository/target/classes/",WORKDIR_A)
    exit_code = container.wait()["StatusCode"]
    logging.debug(f"Container exited with code {exit_code}")
    logging.debug("---The following is the output from the container---")
    logging.debug(container.logs(stdout=True, stderr=True).decode('utf-8'))

    logging.debug("---2.3. Parse Oracles for specified Method---")
    logging.debug(f"extract specification for: {METHOD_NAME}")
    with open(os.path.join(OUTPUTDIR_A, "toradocu_oracles.json"), 'r') as file:
        data = json.load(file)
    oracles = []
    for method in data:
        logging.debug(f"Current Method is: {method["operation"]["name"]}")
        if method["operation"]["name"] == METHOD_NAME:
            oracles.append(method)
    if len(oracles) == 0:
        logging.error(f"No oracles defined for {METHOD_NAME}")
    logging.debug(f"Found oracles: {oracles}")

    with open(os.path.join(OUTPUTDIR_A, "oracles_for_" + METHOD_NAME + ".json"), 'w') as f: # Write oracles to a file
        json.dump(oracles, f, indent=2)



    logging.info("---3. Generate Error Revealing Tests using Randoop---")

    logging.debug("---3.1. Generate dependencies---")
    result = run_shell(f"jdeps -apionly -v -R -cp {CLASSDIR_A} {CLASS_FILE_A} | grep -v '^[A-Za-z]' | sed -E 's/^.* -> ([^ ]+) .*$/\\1/' | sort | uniq",shell=True)
    with open(os.path.join(OUTPUTDIR_A, "methodlist.txt"), 'w') as f:
        f.write(result["stdout"])
    logging.debug(f"{METHOD_NAME} has the following dependencies: {result["stdout"]}")
    #TODO Parse methodlist.txt and remove anything from Java STDB
    logging.debug("---3.2. Generate Error Revealing Tests---")
    #result = run("java",["--class-path", "libs/randoop-all-4.3.3.jar:scripts/commons-math/target/classes", "randoop.main.Main","gentests", "--testclass=org.apache.commons.math3.complex.Complex", "--classlist=methodlist.txt",  "--time-limit=60", "--stop-on-error-test", "--use-jdk-specifications=false", "--error-test-basename=ErrorTest"])
    #--class-path libs/randoop-all-4.3.3.jar:scripts/commons-math/target/classes randoop.main.Main gentests --testclass=org.apache.commons.math3.complex.Complex --classlist=methodlist.txt --time-limit=60 --stop-on-error-test --use-jdk-specifications=false --error-test-basename=ErrorTest
    #TODO Windows ; UNIX :

    result = run_shell(f"java --class-path {os.path.join(WORKDIR_A, "libs", "randoop-all-4.3.3.jar")}:{CLASSDIR_A} randoop.main.Main gentests --testclass={FQ_CLASS_NAME} --classlist={os.path.join(OUTPUTDIR_A, "methodlist.txt")} --time-limit={RANDOOP_TIME_LIMIT} --stop-on-error-test --use-jdk-specifications=false --error-test-basename=ErrorTest --junit-output-dir={OUTPUTDIR_A} --deterministic={RANDOOP_DETERMINISTIC} --attempted-limit={RANDOOP_ATTEMPTED_LIMIT}",shell=True)
    logging.debug(result["stderr"])
    logging.debug(result["stdout"])


    logging.info("---4. Write result into result.txt---")
    # Check If error revealing tests have been wirtten do disk or not
    pattern = os.path.join(OUTPUTDIR_A, "ErrorTest*.java")# Build the full pattern
    matches = glob.glob(pattern)# Use glob to find matching files
    if matches:
        logging.info("Error-revealing tests were generated.")

        with open(os.path.join(OUTPUTDIR_A, "result.txt"), 'w') as f:
            f.write("postiv")
    else:
        logging.info("No error-revealing tests were generated.")
        with open(os.path.join(OUTPUTDIR_A, "result.txt"), 'w') as f:
            f.write("negativ")

    logging.info("---End of the Script--")




#5 minuten time limit
#nur error revealing tests   nur toradocu specs -use-jdk-specifications=false
#error teast revealing tests nicht wegwerfen
#result.txt - postitiv oder negativ
#classlist nutzen anstatt methodlist
# java stdbib entfernen aus methodlist.txt
