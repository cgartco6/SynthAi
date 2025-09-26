terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {
    bucket = "synthai-terraform-state"
    key    = "production/terraform.tfstate"
    region = "af-south-1"
  }
}

provider "aws" {
  region = "af-south-1"
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "synthai-vpc"
  }
}

# ECS Cluster for container orchestration
resource "aws_ecs_cluster" "synthai_cluster" {
  name = "synthai-cluster"
}

# RDS PostgreSQL Database
resource "aws_db_instance" "synthai_db" {
  identifier             = "synthai-db"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "13.7"
  username               = "synthai_user"
  password               = var.database_password
  db_name                = "synthai"
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  skip_final_snapshot    = true
}

# Elasticache Redis
resource "aws_elasticache_cluster" "synthai_redis" {
  cluster_id           = "synthai-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  port                 = 6379
  security_group_ids   = [aws_security_group.redis.id]
}

# Application Load Balancer
resource "aws_lb" "synthai_alb" {
  name               = "synthai-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public.*.id
}

# Security Groups
resource "aws_security_group" "alb" {
  name        = "synthai-alb-sg"
  description = "Allow HTTP/HTTPS traffic"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
