import csv
from multiprocessing.sharedctypes import Value
import boto3
PROFILES='default'
HEADER = ['ec2 name', 'ID', 'Type', 'Key name', 'Launch time', 'Instance status', 'EBS size','EBS status','EBS ID', 'EBS Name']

def init_csv():
    with open('ec2_dev.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(HEADER)
def write_csv_data(data):
    with open('ec2_dev.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

init_csv()

session = boto3.Session(profile_name=PROFILES)
ec2 = session.client('ec2')
response = ec2.describe_instances()

for reserves in response['Reservations']:

    for instance in reserves['Instances']:
        # ec2 name
        name='-'
        try:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name=tag['Value']
        except ValueError:
            pass
        id=instance['InstanceId']
        ec2_type=instance['InstanceType']
        key_name='-'
        try:
            key_name=instance['KeyName']
        except KeyError:
            pass
        launch_time=instance['LaunchTime']
        status=instance['State']['Name']


        for blockDevice in instance['BlockDeviceMappings']:
            response_volumes=ec2.describe_volumes(
                VolumeIds=[blockDevice['Ebs']['VolumeId']]
            )
            volume=response_volumes['Volumes'][0]
            # break
            volume['Size']
            volume['State']
            volume['VolumeId']

            volName='-'
            try:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        volName=tag['Value']
            except KeyError:
                pass
            except ValueError:
                pass
            write_csv_data([name,id,ec2_type,key_name,launch_time,status,
                volume['Size'],volume['State'],volume['VolumeId'],volName])
