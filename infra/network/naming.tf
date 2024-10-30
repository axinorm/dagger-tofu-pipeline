module "naming" {
  source = "../modules/naming"

  project_name     = var.project_name
  environment_type = var.environment_type
  location         = var.location
}
