##
# Global
##
project_id = "" # To be modified

project_name     = "example"
environment_type = "dev"
location         = "europe-west6"

subnets = [
  {
    name          = "frontend"
    ip_cidr_range = "10.0.0.0/24"
  },
  {
    name          = "backend"
    ip_cidr_range = "10.0.1.0/24"
  },
]
