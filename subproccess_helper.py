import subprocess

def run(command, args):
    """
    Runs a binary as a new subprocess and returns standard information about the process.
    Args:
            command (str): The command.
            args (list[str]): List of command-line arguments.
    Returns:
            dict: A dictionary containing:
                - 'stdout' (str): Standard output from the process.
                - 'stderr' (str): Standard error from the process.
                - 'returncode' (int): Exit code returned by the process.
                - 'pid' (int): Process ID of the launched subprocess.
    """
    # Launch the subprocess
    proc = subprocess.Popen(
        [command] + args,  # Combine binary path with argument list
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Wait for the process to finish and capture output
    stdout, stderr = proc.communicate()

    # Package result similar to subprocess.run()
    result = {
        "stdout": stdout,
        "stderr": stderr,
        "returncode": proc.returncode,
        "pid": proc.pid
    }
    return result

def run_shell(command, shell=False):
    """
    Runs a command with optional shell interpretation.
    Args:
        command (str or list): Command to run. If shell=True, must be str.
        shell (bool): Whether to run command through the shell.
    Returns:
        dict: Contains stdout, stderr, returncode, pid.
    """
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=shell
    )
    stdout, stderr = proc.communicate()
    return {
        "stdout": stdout,
        "stderr": stderr,
        "returncode": proc.returncode,
        "pid": proc.pid
    }
