# ===============================
# API Gateway HTTP API
# ===============================

resource "aws_apigatewayv2_api" "visitor_api" {
  name          = "visitor-counter-http-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = [
      "https://d2owoibyqwgf10.cloudfront.net"
    ]
    allow_methods = ["GET"]
    allow_headers = ["*"]
  }
}

# ===============================
# Integration with Lambda
# ===============================

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.visitor_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.counter.invoke_arn
}

# ===============================
# Route
# ===============================

resource "aws_apigatewayv2_route" "counter_route" {
  api_id    = aws_apigatewayv2_api.visitor_api.id
  route_key = "GET /counter"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# ===============================
# Stage
# ===============================

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.visitor_api.id
  name        = "prod"
  auto_deploy = true
}
