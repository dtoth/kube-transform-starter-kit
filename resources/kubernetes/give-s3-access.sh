# This script is used to give the kt-pod service account access to the S3 bucket

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Patch the kt-pod SA with the role ARN
kubectl patch serviceaccount kt-pod \
  -n default \
  -p "{\"metadata\":{\"annotations\":{\"eks.amazonaws.com/role-arn\":\"arn:aws:iam::${ACCOUNT_ID}:role/kt-s3-access-role\"}}}"
