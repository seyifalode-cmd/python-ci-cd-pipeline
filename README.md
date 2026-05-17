# Python CI/CD Pipeline

A full continuous integration and continuous deployment pipeline for a Python grading application — from linting and unit testing in Jenkins, through artifact packaging, to automated deployment on a remote application server via Ansible.

---

## Project at a Glance

| | |
|---|---|
| **Tools Used** | Jenkins · Ansible · Terraform · MariaDB · Python · Pylint · Pytest |
| **Platform** | AWS EC2 (Jenkins node, Python app server, DB server) |
| **Languages** | Python · Groovy (Jenkinsfile) · YAML (Ansible) · HCL (Terraform) · SQL |
| **What It Does** | Lints, tests, packages, and deploys a Python grades management application across a multi-server AWS environment |

## The Problem This Project Solves

A Python application that works locally is not a deployed application. Getting code from a developer's machine into a running production environment involves a chain of steps: check code quality, run tests, package the artifact, transfer it to the right server, set up the database, start the application. Done manually, this chain is slow, inconsistent, and error-prone. A missed step — forgetting to run tests, deploying the wrong version, skipping database migration — can take down the system.

A CI/CD pipeline encodes every step of this chain into code. Jenkins triggers automatically on commit. Every run lints the code, runs all tests, and only packages the artifact if both pass. Deployment to the application server is handled by Ansible — idempotent, auditable, and repeatable. The database is provisioned by Terraform as part of the infrastructure layer.

This project covers a realistic three-tier deployment: infrastructure provisioning (Terraform), application CI (Jenkins integration pipeline), and application CD (Jenkins deployment pipeline with Ansible).

## Pipeline Architecture

```
DEVELOPER COMMIT
       |
       v
JENKINS INTEGRATION PIPELINE (Jenkinsfile_Integration)
  Runs on: Python-Node
  ├── Stage: Lint
  │     pip3 install -r requirements.txt
  │     pylint *.py --exit-zero
  ├── Stage: Test
  │     pytest  (runs test_GradingHelper.py, test_Enrollments.py, test_Enrollment.py)
  └── Stage: Package
        removes test files
        zip -r gradesApp.zip Python/
        copies artifact to ~/python_deployment/
               |
               | artifact ready
               v
JENKINS DEPLOYMENT PIPELINE (Jenkinsfile_Deployment)
  Parameters: APP_NODE_IP, DB_NODE_IP
  ├── Stage: SCP copy
  │     SSH into app server
  │     scp gradesApp.zip to ~/deployments/
  └── Stage: Ansible Playbook
        ansiblePlaybook: python_deployment.yml
        extra-vars: database_ip=${DB_NODE_IP}
               |
               v
  Stage: Run Application
        SSH into app server
        cd deployments/Python; ./start.sh &
               |
               v
LIVE PYTHON GRADES APPLICATION
  Connected to MariaDB (provisioned via Terraform)
```

## Repository Structure

```
python-ci-cd-pipeline/
├── Jenkinsfile_Integration     # CI: lint, test, package
├── Jenkinsfile_Deployment      # CD: SCP, Ansible deploy, start app
├── python_deployment.yml       # Ansible playbook for deployment
├── hosts.ini                   # Ansible inventory
├── Python/
│   ├── Grades.py               # Core grades logic
│   ├── GradingHelper.py        # Grade calculation helpers
│   ├── Enrollments.py          # Enrollment management
│   ├── EnrollmentHelper.py     # Enrollment helpers
│   ├── Course.py               # Course data model
│   ├── MariaDBConnect.py       # Database connection layer
│   ├── test_GradingHelper.py   # Unit tests
│   ├── test_Enrollments.py     # Unit tests
│   ├── test_Enrollment.py      # Unit tests
│   └── requirements.txt        # Python dependencies
├── Database/
│   └── Sample*.xlsx            # Sample data (courses, students, grades, enrollment)
├── TestData/
│   └── Sample*.csv             # CSV test data for unit tests
└── Terraform/
    ├── main.tf                 # AWS infrastructure
    ├── variables.tf
    ├── outputs.tf
    ├── install_mariadb.yaml    # Ansible: provision MariaDB server
    └── database.sql            # Schema and seed data
```

## Application Overview

The Python application manages a student grading system with four data entities:

| Module | Purpose |
|---|---|
| `Course.py` | Course data model |
| `Enrollments.py` | Student-to-course enrollment tracking |
| `Grades.py` | Grade records |
| `GradingHelper.py` | Grade calculation and aggregation logic |
| `MariaDBConnect.py` | MariaDB connection management |

## How to Reproduce

**Prerequisites:** Jenkins with Python and Ansible nodes configured, AWS credentials, Terraform installed

```bash
# 1. Provision infrastructure (MariaDB server)
cd Terraform
terraform init && terraform apply

# 2. Configure Jenkins pipelines
# - Create Pipeline job: "integration" → Jenkinsfile_Integration
# - Create Pipeline job: "deployment" → Jenkinsfile_Deployment

# 3. Run integration pipeline
# Jenkins: Build Now on integration job
# → lints → tests → packages gradesApp.zip

# 4. Run deployment pipeline
# Jenkins: Build with Parameters
#   APP_NODE_IP = <your app server IP>
#   DB_NODE_IP  = <your db server IP>
# → SCP artifact → Ansible deploy → app starts
```

## What This Demonstrates

- Two-pipeline CI/CD pattern: integration separated from deployment
- Pylint static analysis and Pytest unit testing in Jenkins
- Artifact packaging and transfer via SCP with SSH credentials management
- Ansible deployment from Jenkins using the `ansiblePlaybook` step
- Three-tier architecture: Jenkins orchestration, Python app tier, MariaDB data tier

---

*Oluwaseyi Michael Falode · Cybersecurity & Cloud Security Engineer · Toronto, ON*
