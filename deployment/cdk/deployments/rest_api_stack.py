"""AWS CDK module to create ECS infrastructure"""
from aws_cdk import core
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2

class EcsRestAPICdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the ECR Repository
        ecr_repository = ecr.Repository(self,
                                        "reatapi-repository",
                                        repository_name="reatapi-repository")

        # Create the ECS Cluster (and VPC)
        vpc = ec2.Vpc(self,
                      "reatapi-vpc",
                      max_azs=3)

        # Create ECS Cluster
        cluster = ecs.Cluster(self,
                              "reatapi-cluster",
                              cluster_name="reatapi-cluster",
                              vpc=vpc)

        # Create the ECS Task Definition with placeholder container (and named Task Execution IAM Role)
        execution_role = iam.Role(self,
                                  "reatapi-execution-role",
                                  assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                                  role_name="reatapi-execution-role")

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

        # Create the task-definition
        task_definition = ecs.FargateTaskDefinition(self,
                                                    "reatapi-task-definition",
                                                    execution_role=execution_role,
                                                    family="reatapi-task-definition")

        """
        container = task_definition.add_container(
            "reatapi-container",
            image=ecs.ContainerImage.from_registry("rest-api")
        )
        """

        container = task_definition.add_container(
            "ecs-devops-sandbox",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )

        # Add Port mapping to container
        container.add_port_mappings(ecs.PortMapping(container_port=9090, protocol=ecs.Protocol.TCP))

        """
        # Create the ECS Service
        service = ecs.FargateService(self,
                                     "reatapi-service",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     service_name="reatapi-service")
        """
        
        # Create NetworkLoadBalancer first
        loadbalancer = elbv2.NetworkLoadBalancer(self,
                                                 id="restapi-ecs-lb",
                                                 cross_zone_enabled=True,
                                                 load_balancer_name="restapi-ecs-lb",
                                                 vpc=vpc,
                                                 internet_facing=False
                                                 )

        # Create NetworkListener
        listener = elbv2.NetworkListener(self,
                                         id="restapi-ecs-lb-listener",
                                         load_balancer=loadbalancer,
                                         port=9090,
                                         protocol=elbv2.Protocol.TCP
                                         )

        # Create the service
        service = ecs_patterns.NetworkLoadBalancedFargateService(self,
                                        "reatapi-service",
                                        cpu=256,
                                        memory_limit_mib=512,
                                        task_definition=task_definition,
                                        cluster=cluster,
                                        desired_count=2,
                                        service_name="reatapi-service",
                                        load_balancer=loadbalancer)

        # Create a HealthCheck
        health = elbv2.HealthCheck(enabled=True, path="/health/check", interval=5)

        listener.add_target_groups("restapi-ecs-lb-target-grp", service.target_group)

        """
        # Add add the service to target and then to NetworkListener
        listener.add_targets(id="restapi-ecs-lb-target",
                            port=9090,
                            target_group_name="restapi-ecs-lb-target-grp",
                            targets=[service],
                            health_check=health)
        """

