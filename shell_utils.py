import subprocess

def run_command(command):
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return str(result.stdout)