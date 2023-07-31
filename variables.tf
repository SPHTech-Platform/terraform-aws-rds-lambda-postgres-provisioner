variable "enabled" {
  type        = bool
  default     = true
  description = "Defines whether this module should create resources"
}

variable "timeout" {
  type        = number
  default     = 30
  description = "The amount of time your Lambda Function has to run in seconds"
}

variable "vpc_config" {
  type = object({
    vpc_id             = string
    subnet_ids         = list(string)
    security_group_ids = list(string)
  })
  description = "VPC configuration for Lambda function"
}

variable "invoke" {
  type        = bool
  default     = true
  description = "Defines whether lambda function should be invoked immediately after provisioning"
}

variable "lambda_name" {
  type        = string
  description = "value of lambda name"
}

variable "rds_arn" {
  type        = string
  description = "value of rds arn"
}

variable "rds_port" {
  type        = string
  description = "value of rds port"
}

variable "rds_endpoint" {
  type        = string
  description = "value of rds port"
}

variable "rds_user_secret_name" {
  type        = string
  description = "value of rds user secret name"
}

variable "rds_master_user_secret_name" {
  type        = string
  description = "values of rds master user secret name"
  default     = null
}

variable "rds_master_user_secret_arn" {
  type        = string
  description = "values of rds master user secret arn"
}
