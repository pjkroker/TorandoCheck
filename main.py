import logging
import json

from docker_helper import DockerHelper
from subproccess_helper import run
# Set up basic configuration for logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.debug("---Starting Setup---")
NAME = "add"
DOCKERFILE_PATH = '/Users/paul/paul_data/projects_cs/jdoc_randoop/dockerfile'
VOLUME_PATH = "/Users/paul/paul_data/projects_cs/jdoc_randoop/scripts"
IMAGE = 'toradocu-x86'
RANDOOP_TIME_LIMIT = 60
logging.debug("---Set up Docker---")
docker_helper = DockerHelper()
logging.debug("---Finishing Setup---")


if __name__ == '__main__':
    logging.info("---1. Load ANALYZED JSON file---")# with all the java information

    logging.info("---2. Generate Oracles using Toradocu/JDoctor---")
    # logging.debug("---2.1. Generate Oracles---")
    #
    # container = docker_helper.run_container(IMAGE, "sh /scripts/java.sh", VOLUME_PATH)
    #
    # exit_code = container.wait()["StatusCode"]
    # logging.debug(f"Container exited with code {exit_code}")
    # logging.debug("---The following is the output from the container---")
    # logging.debug(container.logs(stdout=True, stderr=True).decode('utf-8'))
    logging.debug("---2.2. Parse Oracles for specified Method---")
    with open(VOLUME_PATH + "/toy-specs.json", 'r') as file:
        data = json.load(file)
    oracles = []

    for method in data:
        #print(method["operation"]["name"])
        if method["operation"]["name"] == NAME:
            oracles.append(method)
    # Write oracles to a file
    with open("oracles_for_" + NAME + ".json", 'w') as f:
        json.dump(oracles, f, indent=2)
    logging.info("---3. Generate Error Revealing Tests using Randoop---")
    logging.debug("---3.1. Find relevant classes for testing using JDEPS---")
    logging.debug("---3.1. Generate Error Revealing Tests---")
    logging.debug("---3.1. Generate only Regression Tests---")
    #result = run("java", ["Greet", "a"])
    result = run("java", ["--class-path", "libs/randoop-all-4.3.3.jar:scripts/commons-math/target/classes", "randoop.main.Main" , "gentests", "--testclass=org.apache.commons.math3.complex.Complex", "--time-limit=60"])
    #java -classpath libs/randoop-all-4.3.3.jar:scripts/commons-math/target/classes randoop.main.Main gentests --testclass=org.apache.commons.math3.complex.Complex --time-limit=60
    logging.debug(result["stderr"])
    logging.debug(result["stdout"])
    logging.info("---4. Write result into result.txt---")



