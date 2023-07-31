# module "db_provisioner" {

#   source      = "SPHTech-Platform/rds-lambda-postgres-provisioner/aws"
#   version     = "0.1.4"
#   lambda_name = "anyname"

#   #Insert your RDS module here
#   rds_endpoint               = module.rds_aurora_postgres_testing.cluster_endpoint
#   rds_port                   = module.rds_aurora_postgres_testing.cluster_port
#   rds_master_user_secret_arn = module.rds_aurora_postgres_testing.cluster_master_user_secret[0].secret_arn
#   rds_user_secret_name       = module.rds_user_secret.name

#   #Insert your VPC details here here
#   vpc_config = {
#     vpc_id             = local.vpc_id
#     subnet_ids         = local.app_subnets
#     security_group_ids = [aws_security_group.postgres_sec_group.id]
#   }

#   #Insert your RDS module here
#   rds_arn = module.rds_aurora_postgres_testing.cluster_arn

#   invoke = true

#   depends_on = [
#     module.rds_aurora_postgres_testing, #Insert your RDS module here
#     module.rds_user_secret
#   ]
# }

# resource "random_string" "test" {
#   length  = 16
#   lower   = true
#   special = false
# }

# module "rds_user_secret" {
#   source = "../../../modules/secretmanager"

#   name        = "database-user-secret-2"
#   description = " RDS user secrets"

#   secret_string = {
#     username = "user35"
#     password = random_string.test.result
#     database = "testing35"
#   }
# }
