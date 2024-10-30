##
# Global
##
variable "project_id" {
  type        = string
  description = "Project ID to deploy resources"
}

variable "project_name" {
  type        = string
  description = "Project name"
}

variable "environment_type" {
  type        = string
  description = "Environment type, should be dev, test, prod"
}

variable "location" {
  type        = string
  description = "Location of resources, should be a valid Google Cloud region"
}

##
# Network
##
variable "subnets" {
  type = list(object({
    name          = string
    ip_cidr_range = string
  }))
  description = "List of subnets to create inside the network"
}
