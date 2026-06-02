terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "restaurant-analytics-s3-natasa"
    key          = "restaurant/terraform.tfstate"
    region       = "eu-central-1"
    use_lockfile = true
    encrypt      = true
  }
}

provider "aws" {
  region = var.aws_region
}

module "s3" {
  source = "./modules/s3"
  env    = var.env
}

module "neon" {
  source = "./modules/neon"
  env    = var.env

}
