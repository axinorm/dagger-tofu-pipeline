output "region" {
  value       = local.regions_trigram
  description = "Trigram of the Google Cloud region"
}

output "suffix" {
  value       = local.resource_suffix
  description = "Resource suffix composed of <project_name>-<environment_type>-<region_trigram>"
}

output "product" {
  value       = local.product_abbreviations
  description = "Product abbreviation"
}
