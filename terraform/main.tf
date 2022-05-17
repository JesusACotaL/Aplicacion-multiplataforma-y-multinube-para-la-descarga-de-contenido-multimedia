terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  backend "state" {
    bucket = "prog-web-proyecto-manga-tf"
    key = "manga-back-state"
    region = "us-west-1"
  }

}
