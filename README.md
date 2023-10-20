# automation


### step 1
dvc init

### step2  

# add dvc files

dvc add data/omail data/onet data/otrim models/omail models/onet models/otrim

# To track the changes with git, run:
git add data/omail.dvc data/onet.dvc data/otrim.dvc data/.gitignore models/otrim.dvc models/onet.dvc models/omail.dvc models/.gitignore

# To enable auto staging, run:
dvc config core.autostage true

### step 3 

# crete s3 bucket : s3://chatbot-bkt/dvc/

# add s3 bucket
# dvc remote add -d myremote s3://<bucket>/<key>
dvc remote add -d myremote s3://chatbot-bkt/dvc/

git add .dvc/config

# set aws credentils in command prompt
set AWS_ACCESS_KEY_ID=
set AWS_SECRET_ACCESS_KEY=



