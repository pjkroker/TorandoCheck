import logging
import time

import docker

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.debug("---Start Setup---")
logging.debug("---Set up Docker---")
# Connect to Docker daemon
client = docker.from_env()
# Path to your Dockerfile
dockerfile_path = '/Users/paul/paul_data/projects_cs/jdoc_randoop/dockerfile'  # Assuming Dockerfile is in the current directory
image_name = 'my_python_image'

# Build the image
try:
    # Open the Dockerfile in read mode and pass it to the build process
    with open(dockerfile_path, 'rb') as dockerfile:
        image, logs = client.images.build(
            fileobj=dockerfile,  # Pass the file object directly
            tag=image_name,  # Use the correct image name
            rm=True  # Clean up intermediate containers
        )

        # Print logs to see build output
        for log in logs:
            # Each log is a dictionary; print the 'stream' key, if it exists
            if 'stream' in log:
                print(log['stream'].strip())  # Print the stream content (log output)
            elif 'error' in log:
                print(f"Error: {log['error'].strip()}")  # Print error messages, if any
            else:
                print(f"Unknown log entry: {log}")  # Handle any unexpected log entries

except Exception as e:
    print("FEHLER")
    print(f"Error: {e}")

    exit(1)
#image = "ubuntu:latest"
#image = "maven:3.8.6-jdk-8"
#client.images.pull(image)
#client.images.build(path=dockerfile_path, tag=image_name)

# Run container and execute script
# container = client.containers.run(
#     image=image,
#     command="sh /scripts/myscript.sh",  # This is inside the container
#     volumes={
#         "/Users/paul/paul_data/projects_cs/jdoc_randoop/scripts": {  # This is on the host
#             "bind": "/scripts",              # This will appear inside the container
#             "mode": "ro"
#         }
#     },
#     detach=True,
# )
#
# # Get output
# output = container.logs().decode()
# logging.debug(output)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.info("---1. Load JSON file---")
    logging.info("---2. Generate Oracles using Toradocu/JDoctor---")
    logging.debug("---2.1. Generate Oracles---")
    container = client.containers.run(
        image=image,
        command="sh /scripts/java.sh",  # This is inside the container
        volumes={
            "/Users/paul/paul_data/projects_cs/jdoc_randoop/scripts": {  # This is on the host
                "bind": "/scripts",  # This will appear inside the container
                "mode": "rw"
            }
        },
        tty=True,  # Add this
        stdin_open=True,  # And this
        detach=True,
    )

    # Wait a bit to ensure the process has time to write logs
    time.sleep(120)

    #for line in container.logs(stream=True):
        #print(line.decode().strip())
    # Get output
    output = container.logs(stdout=True, stderr=True).decode()
    logging.debug("Docker output")
    logging.debug(output)
    exit_code = container.wait()["StatusCode"]
    logging.debug(f"Container exited with code {exit_code}")
    logging.debug("---2.2. Parse Oracles for specified Method---")
    logging.info("---3. Generate Error Revealing Tests using Randoop---")
    logging.debug("---3.1. Find relevant classes for testing using JDEPS---")
    logging.info("---4. Write result into result.txt---")



