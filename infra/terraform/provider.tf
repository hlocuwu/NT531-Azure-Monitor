provider "azurerm" {
  features {
  }
  subscription_id                 = "c589ba9f-89bd-4da1-956a-4be8b4015cf0"
  environment                     = "public"
  use_msi                         = false
  use_cli                         = true
  use_oidc                        = false
  resource_provider_registrations = "none"
}
