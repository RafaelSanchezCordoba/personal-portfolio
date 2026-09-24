resource "aws_acm_certificate" "website" {
  provider          = aws.us_east_1
  domain_name       = "aws.rafasanchez.dev"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}