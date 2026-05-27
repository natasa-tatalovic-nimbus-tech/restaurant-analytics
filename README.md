## AWS Infrastructure Setup

### Prerequisites
#AWS CLI installed and configured (`aws sts get-caller-identity` works)
#Terraform >= 1.6 installed (`terraform -version` works)

### Bootstrap (run once, never again)
#Before running Terraform for the first time, create the remote state backend manually:

# Create S3 state bucket
aws s3 mb s3://restaurant-analytics-s3-natasa --region eu-central-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket restaurant-analytics-s3-natasa \
  --versioning-configuration Status=Enabled

# Create DynamoDB lock table
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-central-1

### Deploy infrastructure
'''
cd terraform
terraform init
terraform plan -var-file=environments/dev.tfvars -var="neon_connection_string=postgres://..."
terraform apply -var-file=environments/dev.tfvars -var="neon_connection_string=postgres://..."
'''