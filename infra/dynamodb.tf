resource "aws_dynamodb_table" "counter" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }
}
resource "aws_dynamodb_table" "visitors" {
  name = "${var.project_name}-visitors"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
}

resource "aws_dynamodb_table_item" "seed" {
  table_name = aws_dynamodb_table.counter.name
  hash_key   = aws_dynamodb_table.counter.hash_key

  item = jsonencode({
    pk    = { S = var.dynamodb_pk_value }
    count = { N = tostring(var.initial_visitor_count) }
  })
}
