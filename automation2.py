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

print(">>> automation")
# print(comments)
# print(product_name)
# print('-------------')


# Run Bash commands in Bash prompt
for cmd in bash_commands:
    print(cmd)
    #subprocess.run(cmd, shell=True)

