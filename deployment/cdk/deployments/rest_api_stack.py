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

        """
        # Create the ECR Repository only once
        ecr_repository = ecr.Repository(self,
                                        "restapi-repository",
                                        repository_name="restapi-repository")
        """

        # Create the ECS Cluster (and VPC)
        vpc = ec2.Vpc(self,
                      "restapi-vpc",
                      max_azs=3)

        # Create ECS Cluster
        cluster = ecs.Cluster(self,
                              "restapi-cluster",
                              cluster_name="restapi-cluster",
                              vpc=vpc)

        # Create the ECS Task Definition with placeholder container (and named Task Execution IAM Role)
        execution_role = iam.Role(self,
                                  "restapi-execution-role",
                                  assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                                  role_name="restapi-execution-role")

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
                                                    "restapi-task-definition",
                                                    execution_role=execution_role,
                                                    family="restapi-task-definition")

        container = task_definition.add_container(
            id="restapi-container",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )

        # Add Port mapping to container
        container.add_port_mappings(ecs.PortMapping(container_port=9090, protocol=ecs.Protocol.TCP))

        # Create the ECS Service
        service = ecs.FargateService(self,
                                     "restapi-service",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     desired_count=2,
                                     service_name="restapi-service")

        # Add security group to this service.
        service.connections.security_groups[0].add_ingress_rule(peer = ec2.Peer.any_ipv4(),
                                                                connection = ec2.Port.tcp(9090),
                                                                description="Allow http inbound"
                                                                )

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

        # Adding a target to listener will automatically create a target group
        listener.add_targets(id="restapi-ecs-lb-target-grp",
                             targets=[service.load_balancer_target(container_name="restapi-container",
                                     container_port=9090)],
                             port=9090,
                             target_group_name="restapi-ecs-lb-target-grp"
                             )

        # Add the target group created automatically when creating the service to listener
        #listener.add_target_groups("restapi-ecs-lb-target-grp", target_grp)
