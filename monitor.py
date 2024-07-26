import boto3
import time
import EC2

class Monitor:
    def __init__(self, access_key, secret_key, region='eu-west-1'):
        self.ec2 = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
    
    def get_metrics(self, instance_id):
        try:
            response = self.cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'm1',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EC2',
                                'MetricName': 'DiskWriteBytes',
                                'Dimensions': [
                                    {
                                        'Name': 'InstanceId',
                                        'Value': instance_id
                                    },
                                ]
                            },
                            'Period': 300,
                            'Stat': 'Sum',
                        },
                        'ReturnData': True,
                    },
                    {
                        'Id': 'm2',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EC2',
                                'MetricName': 'DiskReadOps',
                                'Dimensions': [
                                    {
                                        'Name': 'InstanceId',
                                        'Value': instance_id
                                    },
                                ]
                            },
                            'Period': 300,
                            'Stat': 'Sum',
                        },
                        'ReturnData': True,
                    },
                    {
                        'Id': 'm3',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EC2',
                                'MetricName': 'CPUCreditUsage',
                                'Dimensions': [
                                    {
                                        'Name': 'InstanceId',
                                        'Value': instance_id
                                    },
                                ]
                            },
                            'Period': 300,
                            'Stat': 'Sum',
                        },
                        'ReturnData': True,
                    },
                ],
                StartTime=time.time() - 3600,
                EndTime=time.time(),
            )

            # Display metrics
            for result in response['MetricDataResults']:
                label = result['Id']
                values = result['Values']
                print(f"{label}: {values}")

            return response

        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def set_alarm(self, instance_id, region):
        try:
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=f'DiskWriteBytes_Alarm_{instance_id}',
                AlarmDescription='Alarm for DiskWriteBytes greater than or equal to 9000',
                ActionsEnabled=True,
                MetricName='DiskWriteBytes',
                Namespace='AWS/EC2',
                Statistic='Sum',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    },
                ],
                Period=300,
                EvaluationPeriods=1,
                Threshold=9000.0,
                ComparisonOperator='GreaterThanOrEqualToThreshold',
                AlarmActions=[
                    f'arn:aws:automate:{region}:ec2:stop'
                ],
            )
            print(f"Alarm set successfully for DiskWriteBytes on instance {instance_id}.")

        except Exception as e:
            print(f"Error: {e}")

    def menu(key, secret):
        monitor = Monitor(key, secret, 'eu-west-1')

        while True:
            print("-------- Monitor ---------")
            print("0. Back")
            print("1. Metrics")
            print("2. Set alarm")

            choice = input("Enter choice: ")

            if choice == '0':
                break
            elif choice == '1':
                EC2.EC2.list_instances(monitor.ec2)
                instance_id = input("Give instance ID to list metrics for: ")
                monitor.get_metrics(instance_id)

            elif choice == '2':
                EC2.EC2.list_instances(monitor.ec2)
                instance_id = input("Give instance ID to set alarm for: ")
                monitor.set_alarm(instance_id, 'eu-west-1')
            else:
                print("Invalid choice, please enter a valid option.")