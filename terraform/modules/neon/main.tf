# Neon DB secrets
variable "env" {
  type = string
}
data "aws_secretsmanager_secret" "neon" {
  name = "natasa/restaurant/dev/neon-db-url"
}
# new name
output "secret_arn" {
  value = data.aws_secretsmanager_secret.neon.arn
  sensitive = true
}
output "secret_name" {
  description = "Name of the Neon connection string secret"
  value = data.aws_secretsmanager_secret.neon.name
}
