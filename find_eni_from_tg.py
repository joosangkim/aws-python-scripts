import boto3
import os
import datetime
GROUP_ARN=""
def json_default(value):
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    raise TypeError('not JSON serializable')

os.environ['AWS_PROFILE'] = 'service-prod'

elbv2 = boto3.client('elbv2')
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('logs')
instances=[]
enis=[]
tg=elbv2.describe_target_health(
    TargetGroupArn=GROUP_ARN
)

for tgList in tg['TargetHealthDescriptions']:
    instances.append(tgList['Target']['Id'])


ec2List=ec2.describe_instances(
    InstanceIds=instances
)['Reservations']

for e in ec2List :
    for i in e['Instances']:
        for eni in i['NetworkInterfaces']:
            enis.append(eni['NetworkInterfaceId'])

print(enis)
