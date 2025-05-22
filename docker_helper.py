import logging
import docker

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class DockerHelper:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = docker.from_env()
        self.logger.info("Docker client initialized")


    def build_container(self):
        raise NotImplementedError("TODO")

    def run_container(self, image, command, host_volume_path, guest_volume_path):

        container = self.client.containers.run(
            image=image,
            command=command,  # This is inside the container
            volumes={
                host_volume_path: {  # This is on the host
                    "bind": guest_volume_path,  # This will appear inside the container
                    "mode": "rw"
                }
            },
            tty=True,  # Add this
            stdin_open=True,  # And this
            detach=True,
            stdout=True,  # capture stdout
            stderr=True,
        )
        return container
