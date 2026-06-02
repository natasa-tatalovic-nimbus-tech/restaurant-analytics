terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Main data lake bucket
resource "aws_s3_bucket" "lake" {
  bucket = "restaurant-analytics-${var.env}"
}

# Enable versioning
resource "aws_s3_bucket_versioning" "lake" {
  bucket = aws_s3_bucket.lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "lake" {
  bucket                  = aws_s3_bucket.lake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Create the 6 prefixes (Tip 2 from documentation)
resource "aws_s3_object" "prefixes" {
  for_each = toset([
    "raw/",
    "processed/",
    "analytics/",
    "glue-script/",
    "glue-temp/",
    "athena/",
  ])

  bucket  = aws_s3_bucket.lake.id
  key     = each.value
  content = ""
}
