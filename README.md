# TorandoCheck
TorandoCheck combines Toradocu and Randoop to find inconsistencies.
Toradocu comes preconfigured in a Docker container, which must be run with an x86 architecture for compatibility. 
On non-x86 systems, this can be achieved using virtualization tools like QEMU with Docker Desktop, wich is activated by default.

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


## Building the Docker Image Manually

If you prefer to build the Docker image locally instead of pulling it from Docker Hub, use the following command:

`docker build --progress=plain --platform=linux/amd64 -t pjkroker/toradocu-x86 .`