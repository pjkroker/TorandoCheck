import logging
import json
import glob
import os

from docker_helper import DockerHelper
from subproccess_helper import run, run_shell


# Set up basic configuration for logging
logging.basicConfig(
    filename='my_logfile.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)
logging.debug("---Starting Setup---")
METHOD_NAME = "add"
CLASS_NAME = "org.apache.commons.math3.complex.Complex"
DOCKERFILE_PATH = '/Users/paul/paul_data/projects_cs/jdoc_randoop/dockerfile'
VOLUME_PATH = "/Users/paul/paul_data/projects_cs/jdoc_randoop/scripts"
IMAGE = 'toradocu-x86'
RANDOOP_TIME_LIMIT = 60
WORKDIR = "/Users/paul/paul_data/projects_cs/jdoc_randoop"
logging.debug("---Set up Docker---")
docker_helper = DockerHelper()
logging.debug("---Finishing Setup---")



if __name__ == '__main__':
    logging.info("---1. Load analyzed.json file---")# with all the java information
    with open(os.path.join(WORKDIR, "analyzed.json"), 'r') as file:
        analyzed = json.load(file)
    analyzed = analyzed[0]
    logging.info("---2. Generate Oracles using Toradocu/JDoctor---")

    logging.debug("---2.1. Generate Oracles---")
    container = docker_helper.run_container(IMAGE, "sh /scripts/java.sh", VOLUME_PATH)
    exit_code = container.wait()["StatusCode"]
    logging.debug(f"Container exited with code {exit_code}")
    logging.debug("---The following is the output from the container---")
    logging.debug(container.logs(stdout=True, stderr=True).decode('utf-8'))

    logging.debug("---2.2. Parse Oracles for specified Method---")
    with open(VOLUME_PATH + "/toy-specs.json", 'r') as file:
        data = json.load(file)
    oracles = []
    for method in data:
        #print(method["operation"]["name"])
        if method["operation"]["name"] == METHOD_NAME:
            oracles.append(method)
    # Write oracles to a file
    with open("oracles_for_" + METHOD_NAME + ".json", 'w') as f:
        json.dump(oracles, f, indent=2)



    logging.info("---3. Generate Error Revealing Tests using Randoop---")

    logging.debug("---3.1. Generate dependencies---")
    result = run_shell("jdeps -apionly -v -R -cp /Users/paul/paul_data/projects_cs/jdoc_randoop/scripts/commons-math/target/classes scripts/commons-math/target/classes/org/apache/commons/math3/complex/Complex.class | grep -v '^[A-Za-z]' | sed -E 's/^.* -> ([^ ]+) .*$/\\1/' | sort | uniq",shell=True)
    logging.debug(result["stdout"])
    with open('methodlist.txt', 'w') as f:
        f.write(result["stdout"])
    logging.debug("---3.2. Generate Error Revealing Tests---")
    result = run("java",
                 ["--class-path", "libs/randoop-all-4.3.3.jar:scripts/commons-math/target/classes", "randoop.main.Main",
                  "gentests", "--testclass=org.apache.commons.math3.complex.Complex", "--classlist=methodlist.txt",  "--time-limit=60", "--stop-on-error-test", "--use-jdk-specifications=false", "--error-test-basename=ErrorTest"])
    logging.debug(result["stderr"])
    logging.debug(result["stdout"])





    logging.info("---4. Write result into result.txt---")
    # Build the full pattern
    pattern = os.path.join(WORKDIR, "ErrorTest*.java")
    # Use glob to find matching files
    matches = glob.glob(pattern)
    if matches:
        logging.info("Error-revealing tests were generated.")
        with open('results.txt', 'w') as f:
            f.write("postiv")
    else:
        logging.info("No error-revealing tests were not generated.")
        with open('results.txt', 'w') as f:
            f.write("negativ")





#5 minuten time limit
#nur error revealing tests   nur toradocu specs -use-jdk-specifications=false
#error teast revealing tests nicht wegwerfen
#result.txt - postitiv oder negativ
#classlist nutzen anstatt methodlist
# java stdbib entfernen aus methodlist.txt
