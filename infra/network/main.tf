##
# Network
##
resource "google_compute_network" "this" {
  #checkov:skip=CKV2_GCP_18:No firewall rules needed

  name = "${module.naming.product["compute_network"]}-${module.naming.suffix}"

  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "this" {
  #checkov:skip=CKV_GCP_26:No Flow Logs needed
  #checkov:skip=CKV_GCP_74:No private access needed
  #checkov:skip=CKV_GCP_76:No private access needed

  for_each = { for subnet in var.subnets : subnet.name => subnet }

  name = "${module.naming.product["compute_subnetwork"]}-${each.key}-${module.naming.suffix}"

  network = google_compute_network.this.self_link

  ip_cidr_range = each.value.ip_cidr_range
  region        = var.location
}
