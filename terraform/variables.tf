variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "env" {
  type        = string
  description = "Deployment environment: dev, staging, prod"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "env must be dev, staging, or prod."
  }
}
