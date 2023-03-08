# AWS easy dash

An easy way to generate Cloudwatch dashboards from within your cloudformation template.

![Alt text](img/sam-squirrel.png?raw=true "SAM squirrel looking amazed at the easy dashboard")
###### The SAM squirrel is amazed by your easy dashboards!

## Description

This is a custom resource that will enable you to generate a Cloudwatch dashboard based on a list of resources you attach to the custom resource.
Currently supported resource types are:

- ApiGateway
- Lambda

## Requirements
- aws cli
- aws sam
- docker
- aws vault (optional)
- python 3.9 (optional)

## Documentation

### Deploy
To deploy this custom resource to your account, first build the SAM package using the build command (see commands).
Next deploy it to your account using the deploy command (see commands), you can change the deploy properties in de config file 'config/deploy.toml'.

### Using the custom resource in a cloudformation template

You can use the resource using the following yaml example

```yaml
  DashboardFactoryCustomResource:
    Type: Custom::DashboardFactory
    Properties:
      ServiceToken:
       Fn::ImportValue:
        !Sub "cr-aws-easy-dash-${AWS::Region}"
      DashboardName: "test-dashboard"
      Region: !Ref "AWS::Region"
      Resources:
        - MetricResourceType: ApiGateway
          ResourceReference: ApiGatewayName
        - MetricResourceType: Lambda
          ResourceReference: !Ref HelloWorldFunction
```

### Modifications
When you make changes to this custom resource and want to test locally, you can use the local invoke commands (see commands).

You can add supported aws resources in the 'code/awsresources' folder, files need to be in json containing a dictionary with the resource type as a leading key.

For example:
If you want to add support for let's say S3 you create a json file called s3.json and use S3 as leading key. When you want to use an S3 resource in the dashboard the value for 'MetricResourceType' will be 'S3'.

The json file needs to be provided in the aws defined json structure. 
See: https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html

### References:
aws sam:
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html

aws cli:
https://docs.aws.amazon.com/cli/index.html

aws vault:
https://github.com/99designs/aws-vault

boto3:
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

docker:
https://docs.docker.com/

## Commands

### Local invoke dashboardFactory create event:
#### This command will locally invoke the lambda and simulate a create dashboard event
```bash
sam local invoke --event local/events/cfnCreate.json DashboardFactory
```

### Local invoke dashboardFactory delete event:
#### This command will locally invoke the lambda and simulate a delete dashboard event
```bash
sam local invoke --event local/events/cfnDelete.json DashboardFactory
```

### Build cmd:
```bash
sam build --parallel --use-container --build-image amazon/aws-sam-cli-build-image-python3.9
```

### Deploy dev cmd:
```bash
sam deploy --resolve-s3 --config-file 'config/deploy.toml'
```