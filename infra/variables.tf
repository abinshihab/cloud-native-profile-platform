variable "aws_region" {
  type        = string
  description = "AWS region to deploy into"
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Project name used for naming resources"
  default     = "cloud-native-profile"
}

variable "site_bucket_name" {
  type        = string
  description = "S3 bucket name for the website (must be globally unique)"
}

variable "dynamodb_table_name" {
  type        = string
  description = "DynamoDB table name for visitor counter"
  default     = "visitor_counter_v2"
}

variable "dynamodb_pk_value" {
  type        = string
  description = "Partition key value used by the visitor counter"
  default     = "site#awsbenshehab"
}

variable "initial_visitor_count" {
  type        = number
  description = "Initial visitor count to seed (e.g., 1057)"
  default     = 1057
}
