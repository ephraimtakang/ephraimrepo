provider "aws" {
  region = "us-east-1"  # Update this to your desired AWS region
}

# EC2 Instance
resource "aws_instance" "ec2_instance" {
  ami           = "ami-0c55b159cbfafe1f0"  # Ubuntu 20.04 LTS AMI in us-east-1. You can update this for your desired region.
  instance_type = "t2.micro"  # Update to a suitable instance type based on your needs.

  tags = {
    Name = "Python-API-EC2-Instance"
  }

  user_data = <<-EOT
              #!/bin/bash
              apt update
              apt install -y python3-pip
              pip3 install flask
              git clone https://github.com/your_username/your_repo.git  # Replace with your actual GitHub repository URL
              cd your_repo
              nohup python3 acme_api.py &
              EOT
}

# Security Group for EC2 instance
resource "aws_security_group" "ec2_security_group" {
  name        = "Python-API-SG"
  description = "Security group for Python API EC2 instance"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Python-API-SG"
  }
}

# Security Group Rule to allow SSH access (Optional)
resource "aws_security_group_rule" "ssh_rule" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ec2_security_group.id
}

# Associate Security Group with EC2 instance
resource "aws_instance_security_group_association" "instance_sg_association" {
  security_group_id = aws_security_group.ec2_security_group.id
  instance_id       = aws_instance.ec2_instance.id
}

# Output the public IP address of the EC2 instance
output "public_ip" {
  value = aws_instance.ec2_instance.public_ip
}
