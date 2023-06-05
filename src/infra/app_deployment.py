from cdktf import TerraformOutput, TerraformStack
from cdktf_cdktf_provider_azurerm.app_service_plan import AppServicePlan
from cdktf_cdktf_provider_azurerm.container_registry import ContainerRegistry
from cdktf_cdktf_provider_azurerm.data_azurerm_role_definition import (
    DataAzurermRoleDefinition,
)
from cdktf_cdktf_provider_azurerm.linux_web_app import (
    LinuxWebApp,
    LinuxWebAppSiteConfig,
    LinuxWebAppSiteConfigApplicationStack,
)
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.role_assignment import RoleAssignment
from constructs import Construct

from common.config import Config


class AppDeploymentStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: Config):
        super().__init__(scope, id)
        self.config = config

        # Configure the AzureRM Provider
        # you need to set environment variables for authentication
        # https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
        self.provider = AzurermProvider(self, "azurerm", features={})

        self.container_registry = ContainerRegistry(
            self,
            id_="container_registry",
            name=self.config.docker.registry_name,
            location=config.terraform.location,
            resource_group_name=config.terraform.resource_group_name,
            sku="Basic",
        )

        # TODO: refactor this to service_plan
        # https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/service_plan
        self.app_service_plan = AppServicePlan(
            self,
            id_="app_service_plan",
            name="patrickappserviceplan",
            location=config.terraform.location,
            resource_group_name=config.terraform.resource_group_name,
            kind="Linux",
            reserved=True,
            sku={
                "tier": "Free",
                "size": "F1",
            },
        )

        docker_image_string = (
            f"{self.container_registry.login_server}/{self.config.docker.image_name}"
        )

        self.linux_webapp = LinuxWebApp(
            self,
            id_="linux_webapp",
            name="patricklinuxwebapp",
            location=config.terraform.location,
            resource_group_name=config.terraform.resource_group_name,
            service_plan_id=self.app_service_plan.id,
            site_config=LinuxWebAppSiteConfig(
                application_stack=LinuxWebAppSiteConfigApplicationStack(
                    docker_image=docker_image_string,
                    docker_image_tag="latest",
                ),
                always_on=False,
                container_registry_use_managed_identity=True,
            ),
            identity={"type": "SystemAssigned"},
        )

        self.acr_pull_role = DataAzurermRoleDefinition(
            scope_=self,
            id_="acr_pull_role",
            name="AcrPull",
            scope=self.container_registry.id,
        )

        self.acr_pull_role_assignment = RoleAssignment(
            self,
            id_="acr_pull_role_assignment",
            principal_id=self.linux_webapp.identity.principal_id,
            role_definition_id=self.acr_pull_role.id,
            scope=self.container_registry.id,
        )

        TerraformOutput(
            self,
            "registry_url",
            value=self.container_registry.login_server,
        )

        TerraformOutput(
            self,
            "webapp_url",
            value=self.linux_webapp.default_hostname,
        )
