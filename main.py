import logging

from docker_helper import DockerHelper

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.debug("---Starting Setup---")
logging.debug("---Set up Docker---")
docker_helper = DockerHelper()
DOCKERFILE_PATH = '/Users/paul/paul_data/projects_cs/jdoc_randoop/dockerfile'
VOLUME_PATH = "/Users/paul/paul_data/projects_cs/jdoc_randoop/scripts"
IMAGE = 'toradocu-x86'
logging.debug("---Finishing Setup---")


if __name__ == '__main__':
    logging.info("---1. Load JSON file---")

    logging.info("---2. Generate Oracles using Toradocu/JDoctor---")
    logging.debug("---2.1. Generate Oracles---")

    container = docker_helper.run_container(IMAGE, "sh /scripts/java.sh", VOLUME_PATH)

    exit_code = container.wait()["StatusCode"]
    logging.debug(f"Container exited with code {exit_code}")
    logging.debug("---The following is the output from the container---")
    logging.debug(container.logs(stdout=True, stderr=True).decode('utf-8'))
    logging.debug("---2.2. Parse Oracles for specified Method---")
    logging.info("---3. Generate Error Revealing Tests using Randoop---")
    logging.debug("---3.1. Find relevant classes for testing using JDEPS---")
    logging.info("---4. Write result into result.txt---")



