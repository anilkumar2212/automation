# automation


# step 1
dvc init

# step 2 

# crete s3 bucket : s3://chatbot-bkt/dvc/

# add s3 bucket
# dvc remote add -d myremote s3://<bucket>/<key>
dvc remote add -d myremote s3://chatbot-bkt/dvc/
# set aws credentils in command prompt
set AWS_ACCESS_KEY_ID=
set AWS_SECRET_ACCESS_KEY=


