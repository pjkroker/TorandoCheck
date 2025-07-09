# TorandoCheck
TorandoCheck combines Toradocu and Randoop to find inconsistencies.
Toradocu comes preconfigured in a Docker container, which must be run with an x86 architecture for compatibility. 
On non-x86 systems, this can be achieved using virtualization tools like QEMU with Docker Desktop, wich is activated by default.

## Project Structure
Your project in a folder named `repository` and a file `analyzed.json` should be in the same directory, like this:
```
.
├── main.py
├── libs/
├── ....
├── analyzed.json
├── repository/
│   ├── src/
│   └── pom.xml
```
The `analyzed.json` file contains information about the method to be tested.

## Setup
This tool was developed using Python 3.12. It’s recommended to create a virtual environment before installing dependencies to avoid conflicts.

```pip install -r requirements.txt```

### Requirements

TorandoCheck compiles the analyzed project automatically using Maven.
Therefore, make sure the following are installed and properly configured on your system:

- Java JDK (compatible with the target project, not just the JRE)
  - The JDK must include the jdeps tool, which is used during analysis. Inlcuded by default.
- Apache Maven

The compilation is triggered with:

```mvn -f repository/ clean package -DskipTests```

Make sure this command runs successfully on your system before using TorandoCheck.

You must also have Docker installed and properly configured to use the Toradocu container image.
### Building the Docker Image Manually

If you prefer to build the Docker image locally instead of pulling it from Docker Hub, use the following command:

`docker build --progress=plain --platform=linux/amd64 -t pjkroker/toradocu-x86 .`

 Replace . with the path to the directory containing the Dockerfile, if it's not the current directory.