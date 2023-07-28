# AWS RDS Lambda database provisioner

## Introduction

This module provisions an AWS lambda function which creates a new database and optionally a new user in RDS instance
within a VPC. Supported engines are `postgres` and `mysql`. A newly created user or a master user (in case when you
don't need a new user) will be granted all permissions to the created database.

This module is aim to solve a **cold-start problem** - when you execute `terraform apply` and all your
infrastructure is provisioned in one run. If are trying to solve a different problem, then you
should be optimizing for Day 2 operations and provision a database by other means  (e.g. using
[terraform postrgres provider](https://registry.terraform.io/providers/cyrilgdn/postgresql/latest/docs)).

**Features**:
- Master user password as well as new user password can be passed to the module either via
    - Module variables
    - Parameters in SSM Parameter Store (**Recommended!**)
    - Secrets in Secrets Manager (**Recommended!**)
- Lambda function execution logs are shipped to Cloudwatch
- No database or user will be created if they already exist

**Notes on using secrets from AWS Secrets Manager**:
- When [referencing secrets stored in Secrets Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/integration-ps-secretsmanager.html),
  the `/aws/reference/secretsmanager` prefix must be used
- A secret must contain password in the `password` field or be a plain-text secret

**Caveats**:
- This lambda function needs internet access in order to comminitcate with AWS API. You need to associate this
  function with one or more private subnets in your VPC and make sure that their routing tables have a default
  route pointing to NAT Gateway or NAT Instance in a public subnet. Associating a lambda function with a public
  subnet doesn't give it internet connectivity or public IP address. More context:
  [Give Internet Access to a Lambda Function in a VPC](https://aws.amazon.com/premiumsupport/knowledge-center/internet-access-lambda-function/)
- This lambda function **DOES NOT DROP provisioned database or user** on destroy in order to prevent accidental data
  loss. Please make sure to delete provisioned database and user manually.
- ENIs attached to a lambda function may cause `DependencyViolation` error when you try to destroy associated
  security groups and/or subnets.
  More context: [Corresponding issue on github](https://github.com/terraform-providers/terraform-provider-aws/issues/10329)

**Backlog**:
- [ ] Support SSL connections to RDS

This module is backed by best of breed terraform modules maintained by [Cloudposse](https://github.com/cloudposse).

## Terraform versions

Terraform 0.12. Pin module version to `~> 1.0`. Submit pull-requests to `terraform012` branch.

Terraform 0.13. Pin module version to `~> 2.0`. Submit pull-requests to `master` branch.

## Usage

### Simple usage example

The following example creates a database `new_database` and a user `new_user` with the passwords
passed via variables.

```hcl
  module "db_provisioner" {
    source  = "aleks-fofanov/rds-lambda-db-provisioner/aws"
    version = "~> 2.0"

    source    = "git::https://github.com/aleks-fofanov/terraform-aws-rds-lambda-db-provisioner.git?ref=master"
    name      = "stack"
    namespace = "cp"
    stage     = "prod"

    db_instance_id                = "prod-stack-db"
    db_instance_security_group_id = "sg-XXXXXXXX"
    db_master_password            = "XXXXXXXX"

    db_name          = "new_database"
    db_user          = "new_user"
    db_user_password = "XXXXXXXX"

    vpc_config = {
      vpc_id             = "vpc-XXXXXXXX"
      subnet_ids         = ["subnet-XXXXXXXX", "subnet-XXXXXXXX"]
      security_group_ids = []
    }
  }
```

### Example with passwords passed via SSM Parameters

This example creates a database `new_database` and a user `new_user` with the passwords
passed via SSM Parameters.

```hcl
module "db_provisioner" {
  source  = "aleks-fofanov/rds-lambda-db-provisioner/aws"
  version = "~> 2.0"

  name      = "stack"
  namespace = "cp"
  stage     = "prod"

  db_instance_id                       = "prod-stack-db"
  db_instance_security_group_id        = "sg-XXXXXXXX"
  db_master_password_ssm_param         = "/cp/prod/stack/database/master_password"
  db_master_password_ssm_param_kms_key = "alias/aws/ssm"

  db_name                            = "new_database"
  db_user                            = "new_user"
  db_user_password_ssm_param         = "/cp/prod/stack/database/new_user_password"
  db_user_password_ssm_param_kms_key = "alias/aws/ssm"

  vpc_config = {
    vpc_id             = "vpc-XXXXXXXX"
    subnet_ids         = ["subnet-XXXXXXXX", "subnet-XXXXXXXX"]
    security_group_ids = []
  }
}
```

### Example without creating a new user

This example creates a database `new_database` without a new user with the master user password
passed via SSM Parameter.

```hcl
module "db_provisioner" {
  source  = "aleks-fofanov/rds-lambda-db-provisioner/aws"
  version = "~> 2.0"

  name      = "stack"
  namespace = "cp"
  stage     = "prod"

  db_instance_id                       = "prod-stack-db"
  db_instance_security_group_id        = "sg-XXXXXXXX"
  db_master_password_ssm_param         = "/cp/prod/stack/database/master_password"
  db_master_password_ssm_param_kms_key = "alias/aws/ssm"

  db_name = "new_database"

  vpc_config = {
    vpc_id             = "vpc-XXXXXXXX"
    subnet_ids         = ["subnet-XXXXXXXX", "subnet-XXXXXXXX"]
    security_group_ids = []
  }
}
```

Please refer to the `examples` folder for a complete example.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.4 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.10.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_provisoner_lambda"></a> [provisoner\_lambda](#module\_provisoner\_lambda) | terraform-aws-modules/lambda/aws | ~> 5.0 |

## Resources

| Name | Type |
|------|------|
| [aws_lambda_layer_version.psycopg2_lambda_layer](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_layer_version) | resource |
| [aws_lambda_invocation.default](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_invocation) | data source |
| [aws_lambda_layer_version.psycopg2_lambda_layer](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/lambda_layer_version) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_enabled"></a> [enabled](#input\_enabled) | Defines whether this module should create resources | `bool` | `true` | no |
| <a name="input_invoke"></a> [invoke](#input\_invoke) | Defines whether lambda function should be invoked immediately after provisioning | `bool` | `true` | no |
| <a name="input_lambda_name"></a> [lambda\_name](#input\_lambda\_name) | value of lambda name | `string` | n/a | yes |
| <a name="input_rds_arn"></a> [rds\_arn](#input\_rds\_arn) | value of rds arn | `string` | n/a | yes |
| <a name="input_rds_endpoint"></a> [rds\_endpoint](#input\_rds\_endpoint) | value of rds port | `string` | n/a | yes |
| <a name="input_rds_master_user_secret_name"></a> [rds\_master\_user\_secret\_name](#input\_rds\_master\_user\_secret\_name) | values of rds master user secret name | `string` | n/a | yes |
| <a name="input_rds_port"></a> [rds\_port](#input\_rds\_port) | value of rds port | `string` | n/a | yes |
| <a name="input_rds_user_secret_name"></a> [rds\_user\_secret\_name](#input\_rds\_user\_secret\_name) | value of rds user secret name | `string` | n/a | yes |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | The amount of time your Lambda Function has to run in seconds | `number` | `30` | no |
| <a name="input_vpc_config"></a> [vpc\_config](#input\_vpc\_config) | VPC configuration for Lambda function | <pre>object({<br>    vpc_id             = string<br>    subnet_ids         = list(string)<br>    security_group_ids = list(string)<br>  })</pre> | n/a | yes |

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Authors

Module is created and maintained by [Aleksandr Fofanov](https://github.com/aleks-fofanov).

## License

Apache 2 Licensed. See LICENSE for full details.

## Help

**Got a question?**

File a GitHub [issue](https://github.com/aleks-fofanov/terraform-aws-rds-lambda-db-provisioner/issues).
