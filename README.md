# AWS RDS Lambda Postgres provisioner
<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.4 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 4.0 |

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
| <a name="input_rds_master_user_secret_arn"></a> [rds\_master\_user\_secret\_arn](#input\_rds\_master\_user\_secret\_arn) | values of rds master user secret arn | `string` | n/a | yes |
| <a name="input_rds_master_user_secret_name"></a> [rds\_master\_user\_secret\_name](#input\_rds\_master\_user\_secret\_name) | values of rds master user secret name | `string` | `null` | no |
| <a name="input_rds_port"></a> [rds\_port](#input\_rds\_port) | value of rds port | `string` | n/a | yes |
| <a name="input_rds_user_secret_name"></a> [rds\_user\_secret\_name](#input\_rds\_user\_secret\_name) | value of rds user secret name | `string` | n/a | yes |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | The amount of time your Lambda Function has to run in seconds | `number` | `30` | no |
| <a name="input_vpc_config"></a> [vpc\_config](#input\_vpc\_config) | VPC configuration for Lambda function | <pre>object({<br>    vpc_id             = string<br>    subnet_ids         = list(string)<br>    security_group_ids = list(string)<br>  })</pre> | n/a | yes |

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
