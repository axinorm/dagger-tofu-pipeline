locals {
  regions_trigram = {
    "europe-west1" = "ew1"
    "europe-west6" = "ew6"
  }

  product_abbreviations = {
    # Network
    compute_network    = "vpc"
    compute_subnetwork = "snet"
  }

  resource_suffix = "${var.project_name}-${var.environment_type}-${local.regions_trigram[var.location]}"
}
