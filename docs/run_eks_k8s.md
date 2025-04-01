This guide will help you create the full stack of resources you need to run kube-transform at scale in AWS.

That includes:
- A Kubernetes cluster with AWS EKS in [*Auto Mode*](https://aws.amazon.com/eks/auto-mode/)
- An S3 bucket (to act as your shared file store)
- An ECR repository (to hold your docker images)
- and the relevant IAM permissions between those resources

We'll use Terraform to manage the creation and destruction of our AWS resources.

Note that following these instructions will incur charges on your AWS account.

Pre-requisites:
- You're running Mac OSX (this has been tested with Sonoma 14.5)
- You've installed homebrew

Run the following commands from the root `kube_transform_starter_kit` directory.

### Install AWS CLI
```
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
aws --version # verify
```

### Install Terraform
```
brew update
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
brew upgrade hashicorp/tap/terraform
```

To verify your installation:
`terraform --version`

### Create an IAM User for Terraform
- If you don't already have an AWS account, create one.
- Log into your AWS account via the AWS console.
- Create a `terraform-user` in your AWS account via AWS console.
    - Go to: `IAM/Users/Create User`
        - User name: `terraform-user`
        - Include Console access: `True`
        - `I want to create an IAM user`
        - `Attach Policies Directly`
        - Attach: `AdministratorAccess`
        - `Create User`
        - Note the Access Key and Secret Access Key provided.

### Configure AWS CLI
- Run `aws configure`
- Supply the access key and secret, specify your region.
    - I used `us-east-1`. If you deviate from this, there may be a couple small changes you'll need to make elsewhere in the repo.
- Run `aws sts get-caller-identity` to verify that your AWS cli is properly authenticated.

### Create the EKS cluster
```
terraform -chdir=resources/terraform init
terraform -chdir=resources/terraform plan
terraform -chdir=resources/terraform apply -auto-approve
```
- Note that this may take a while to complete (15 minutes or so).
- When this completes, you will have an EKS Kubernetes control plane managed by AWS. This costs ~0.1 USD/hour.

### Create the kt-pod service account
Now, update your kube config to point to your EKS cluster:
```
aws eks update-kubeconfig --region us-east-1 --name kube-transform-eks-cluster
```

Then run:
```
kubectl apply -f resources/kubernetes/kt-pod-rbac.yaml
```

This creates a Kubernetes service account called `kt-pod`, and says that pods holding this service account can create Jobs in the default namespace in your cluster.

`kube-transform` assigns this service account to its controller pod, so it must exist in your cluster.

Now run:
```
./resources/kubernetes/give-s3-access.sh
```

In Terraform, we created an IAM Role that can access your S3 bucket.
Here, we're saying that the kt-pod service account should assume that role.

Congrats! Your cluster is ready to use.


### Helpful Tips

#### Kill all jobs
```
kubectl delete jobs --all
```

#### Destroy your EKS cluster
```
terraform -chdir=resources/terraform destroy --auto-approve
```
- This will take several minutes to complete. It will destroy the VPCs, subnets, and EKS cluster created by terraform.
- If successful, this will stop all costs from EKS. You may still be charged a small amount for S3 and ECR storage, since it won't delete S3 buckets or ECR repos unless they are empty.

#### Update your kube config to point to EKS
```
aws eks --region us-east-1 update-kubeconfig --name kube-transform-eks-cluster
```
To verify, run:
`kubectl config current-context`

Note that this updates your kube config, which is referenced by both kubectl and the kubernetes python package.

If you want to later point back to your minikube cluster, you can run: `kubectl config use-context minikube`

#### Install the metrics server (optional)
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
- This lets you use `kubectl top pods` to see resource usage in EKS.
- Once you run this command, you'll have a persistent node to run the metrics server, which will cost additional money. Be sure to shut down the metrics server if not needed:
```
kubectl delete deployment metrics-server -n kube-system
```