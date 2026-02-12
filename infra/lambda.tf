data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_src"
  output_path = "${path.module}/lambda_build/function.zip"
}

resource "aws_lambda_function" "counter" {
  function_name = local.lambda_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "visitor_counter.lambda_handler"
  runtime       = "python3.12"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.counter.name
      PK_VALUE   = var.dynamodb_pk_value
    }
  }
}

resource "aws_lambda_function_url" "counter_url" {
  function_name = aws_lambda_function.counter.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = [
      "https://d2owoibyqwgf10.cloudfront.net",
      "https://www.awsbenshehab.net"
    ]

    allow_methods = ["GET"]
    allow_headers = ["*"]
    max_age       = 86400
  }
}


