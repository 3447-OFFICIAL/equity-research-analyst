provider "aws" {
  region = "us-east-1"
}

# EKS Cluster
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "equity-research-cluster"
  cluster_version = "1.30"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 1
      max_size     = 5
      instance_types = ["m5.large"]
    }
    compute_heavy = {
      desired_size = 2
      min_size     = 2
      max_size     = 10
      instance_types = ["c5.xlarge"] # For Monte Carlo & Quant engines
    }
  }
}

# RDS Postgres
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  identifier = "equity-research-db"
  engine     = "postgres"
  engine_version = "16.1"
  instance_class = "db.m5.large"
  allocated_storage = 100
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "equity-research-redis"
  engine               = "redis"
  node_type            = "cache.m5.large"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
}
