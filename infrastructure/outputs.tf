output "bucket_name" {
    value = aws_s3_bucket.website.bucket
}

output "cloudfront_distribution_id" {
    value = aws_cloudfront_distribution.website.id
}

output "cloudfront_distribution_domain_name" {
    value = aws_cloudfront_distribution.website.domain_name
}

output "custom_domain" {
  value = "https://aws.rafasanchez.dev"
}

output "certificate_arn" {
  value = aws_acm_certificate.website.arn
}