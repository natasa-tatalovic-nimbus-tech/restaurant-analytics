output "bucket_name" {
  description = "Data lake bucket name"
  value       = module.s3.bucket_name
}

output "bucket_arn" {
  description = "Data lake bucket ARN"
  value       = module.s3.bucket_arn
}
