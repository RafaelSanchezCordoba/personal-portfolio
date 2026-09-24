terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 6.0"
        }
    }
}

provider "aws" {
    region = "eu-north-1"
    profile = "rafa-iac"
}

provider "aws" {
  alias   = "us_east_1"
  region  = "us-east-1"
  profile = "rafa-iac"
}