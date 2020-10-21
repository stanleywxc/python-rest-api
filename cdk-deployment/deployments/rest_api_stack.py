"""AWS CDK module to create ECS infrastructure"""
from aws_cdk import (core, aws_ecs as ecs, aws_ecr as ecr, aws_ec2 as ec2, aws_iam as iam)

class EcsRestAPICdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the ECR Repository
        ecr_repository = ecr.Repository(self,
                                        "ecs-rest-api-repository",
                                        repository_name="ecs-rest-api-repository")

        # Create the ECS Cluster (and VPC)
        vpc = ec2.Vpc(self,
                      "ecs-rest-api-vpc",
                      max_azs=3)
        cluster = ecs.Cluster(self,
                              "ecs-rest-api-cluster",
                              cluster_name="ecs-rest-api-cluster",
                              vpc=vpc)

        # Create the ECS Task Definition with placeholder container (and named Task Execution IAM Role)
        execution_role = iam.Role(self,
                                  "ecs-rest-api-execution-role",
                                  assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                                  role_name="ecs-rest-api-execution-role")
        execution_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
                ]
        ))
        task_definition = ecs.FargateTaskDefinition(self,
                                                    "ecs-rest-api-task-definition",
                                                    execution_role=execution_role,
                                                    family="ecs-rest-api-task-definition")


        container = task_definition.add_container(
            "ecs-rest-api",
            image=ecs.ContainerImage.from_registry("rest-api")
        )
        """
        container = task_definition.add_container(
            "ecs-devops-sandbox",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )
        """

        # Create the ECS Service
        service = ecs.FargateService(self,
                                     "ecs-rest-api-service",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     service_name="ecs-rest-api-service")
