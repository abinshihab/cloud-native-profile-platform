terraform {
  backend "s3" {
    bucket         = "cloud-native-profile-platform-terraform-state"
    key            = "global/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "cloud-native-profile-platform-terraform-locks"
    encrypt        = true
  }
}
