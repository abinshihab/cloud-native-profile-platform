output "s3_bucket_name" {
  value = aws_s3_bucket.site.bucket
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.cdn.id
}

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.cdn.domain_name
}

output "lambda_function_name" {
  value = aws_lambda_function.counter.function_name
}

output "lambda_function_url" {
  value = aws_lambda_function_url.counter_url.function_url
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.counter.name
}
output "visitor_api_url" {
  value = "${aws_apigatewayv2_api.visitor_api.api_endpoint}/prod/counter"
}
output "visitor_api_id" {
  value = aws_apigatewayv2_api.visitor_api.id
}
