output "bucket_name" {
  description = "Data lake bucket name"
  value = aws_s3_bucket.lake.id
}

output "bucket_arn" {
  description = "Data lake bucket ARN"
  value = aws_s3_bucket.lake.arn
}
