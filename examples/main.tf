locals {
  secret_name_with_postfix = element(split(":", module.rds_aurora_postgres_testing.cluster_master_user_secret[0].secret_arn), length(split(":", module.rds_aurora_postgres_testing.cluster_master_user_secret[0].secret_arn)) - 1)
  segments                 = split("-", local.secret_name_with_postfix)
  master_user_secret_name  = join("-", slice(local.segments, 0, length(local.segments) - 1))

}

module "db_provisioner" {

  source      = "SPHTech-Platform/rds-lambda-postgres-provisioner/aws"
  version     = "0.1.1"
  lambda_name = "appsec"

  #Insert your RDS module here
  rds_endpoint                = module.rds_aurora_postgres_testing.cluster_endpoint
  rds_port                    = module.rds_aurora_postgres_testing.cluster_port
  rds_master_user_secret_name = local.master_user_secret_name
  rds_user_secret_name        = module.rds_user_secret.name

  #Insert your VPC details here here
  vpc_config = {
    vpc_id             = local.vpc_id
    subnet_ids         = local.app_subnets
    security_group_ids = [aws_security_group.postgres_sec_group.id]
  }

  #Insert your RDS module here
  rds_arn = module.rds_aurora_postgres_testing.cluster_arn

  invoke = true

  depends_on = [
    module.rds_aurora_postgres_testing,
    module.rds_user_secret #Insert your RDS module here
  ]
}

resource "random_string" "test" {
  length  = 16
  lower   = true
  special = false
}

# mlflow RDS admin user
module "rds_user_secret" {
  source = "../../../modules/secretmanager"

  name        = "database-user-secret-2"
  description = " RDS user secrets"

  secret_string = {
    username = "user35"
    password = random_string.test.result
    database = "testing35"
  }
}

