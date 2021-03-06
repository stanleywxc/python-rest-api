#!/usr/bin/env python3

from aws_cdk import core

from deployments.rest_api_stack import EcsRestAPICdkStack


app = core.App()
EcsRestAPICdkStack(app, "rest-api-stack")

app.synth()
