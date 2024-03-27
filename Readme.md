# Using AWS SAM CLI for Serverless Development

## Overview

[AWS SAM (Serverless Application Model)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) is an open-source framework for building serverless applications. It provides a simplified way to define serverless applications, allowing you to define AWS resources such as AWS Lambda functions, Amazon API Gateway APIs, and Amazon DynamoDB tables using a simple YAML syntax.

This README.md guide provides instructions on how to use AWS SAM CLI for local development, building, and deploying serverless applications.

## Prerequisites

Before you begin, make sure you have the following installed on your local machine:

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Docker](https://www.docker.com/get-started)
- [AWS CLI](https://aws.amazon.com/cli/)
- [Python](https://www.python.org/downloads/) (optional, depending on your use case)

## Usage

### 1. Local Development

To start a local development server and test your serverless application locally, use the `sam local start-api` command:

```bash
sam local start-api
