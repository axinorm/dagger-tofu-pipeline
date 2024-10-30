variable "project_name" {
  type        = string
  description = "Project name"
}

variable "environment_type" {
  type        = string
  description = "Environment type, should be dev, test, prod"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment_type)
    error_message = "Valid values for environment_type are dev, test or prod"
  }
}

variable "location" {
  type        = string
  description = "Location of resources, should be a valid Google Cloud region"

  validation {
    condition     = contains(["europe-west1", "europe-west6"], var.location)
    error_message = "Valid values are europe-west1 or europe-west6"
  }
}
