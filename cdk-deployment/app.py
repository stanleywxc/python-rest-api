#!/usr/bin/env python3

from aws_cdk import core

from deployments.rest_api_stack import EcsDevopsSandboxCdkStack


app = core.App()
EcsDevopsSandboxCdkStack(app, "rest-api-stack")

app.synth()
