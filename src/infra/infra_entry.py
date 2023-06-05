#!/usr/bin/env python
from cdktf import App

from common.config import config
from infra.app_deployment import AppDeploymentStack

if __name__ == "__main__":
    app = App()
    AppDeploymentStack(app, "app-deployment-stack", config=config)

    app.synth()
