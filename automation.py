import subprocess

# Define the DVC commands
dvc_commands = [
    "dvc init"
]

# Run DVC commands in Python
for cmd in dvc_commands:
    subprocess.run(cmd, shell=True)

print("dvc init done")