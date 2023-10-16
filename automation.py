import sys
import subprocess

comments = " ".join(sys.argv[1:-1])
product_name = sys.argv[-1]

bash_commands = [
    f'dvc add data/{product_name}',
    f'git add data/{product_name}.dvc',
    f'git commit -m {comments}',
    'dvc push',
    'git push'
]
# Run commands in prompt
for cmd in bash_commands:
    subprocess.run(cmd, shell=True)










# # Define the Bash commands
# bash_commands = [
#     'dvc add data/onet',
#     'git add data/onet.dvc',
#     'git commit -m "onet version add"',
#     'dvc push',
#     'git push'
# ]

# # Run Bash commands in Bash prompt
# for cmd in bash_commands:
#     subprocess.run(cmd, shell=True)


