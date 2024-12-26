provider "aws" {
  region  = "us-east-1"
}

provider "aws" {
  region  = "us-east-1"
  alias   = "database-region"
}


resource "aws_rds_cluster" "rds_cluster_aurora" {
  provider = aws.database-region
  cluster_identifier = "paymaarttest"
  engine             = "aurora-postgresql"
  engine_mode        = "provisioned"
  engine_version     = "15.4"
  database_name      = "paymaart"
  master_username    = "paymaartAdmin"
  master_password    = "Admin#123"
  storage_encrypted  = true
  serverlessv2_scaling_configuration {
    max_capacity = 3.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster_instance" "rds_cluster_aurora_instance" {
  provider = aws.database-region
  cluster_identifier = aws_rds_cluster.rds_cluster_aurora.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.rds_cluster_aurora.engine
  engine_version     = aws_rds_cluster.rds_cluster_aurora.engine_version
  publicly_accessible = false
}

