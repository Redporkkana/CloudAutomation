import boto3

class EC2:
    def list_instances(client):

        try:
            response = client.describe_instances()

            if not response['Reservations']:
                print("No instances found")
                return
        
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    print(f"Instance ID: {instance['InstanceId']}, State:{instance['State']['Name']}")

        except Exception as e:
            print(f"Error {e}")

    def start_instance(client, instance_id):
        try:
            client.start_instances(InstanceIds=[instance_id])
            print(f"Instance with ID {instance_id} has been started.")

        except Exception as e:
            print(f"Error {e}")

    def stop_instance(client, instance_id):
        try:
            client.stop_instances(InstanceIds=[instance_id])
            print(f"Instance with ID {instance_id} has been stopped.")

        except Exception as e:
            print(f"Error {e}")

    def instance_launch(client):
        try:
            operating_system = input("Enter 'Windows' or 'Linux' for the operating system: ")
            if( operating_system.lower() not in ['windows', 'linux']):
                print("Invalid operating system selection.")
                return

            # Linux AMI, choice available on 18th of November 2023
            ami_id = "ami-07355fe79b493752d"
            if( operating_system.lower == 'windows'):
                ami_id = "ami-0b3a63a48e767cc82"

            instance_type = 't2.micro'
            key_name = 'lecture7-2023'
            security_group_ids = ['sg-08d0098535c6f1c22']
            subnet_id = 'subnet-0d9bf6b9d43647b44'

            response = client.run_instances(
                ImageId=ami_id,
                InstanceType=instance_type,
                KeyName=key_name,
                SecurityGroupIds=security_group_ids,
                SubnetId=subnet_id,
                MinCount=1,
                MaxCount=1
            )

            instance_id = response['Instances'][0]['InstanceId']
            print(f"New instance launched with ID: {instance_id}")

            # waiter for waiting until instance is running
            waiter = client.get_waiter("instance_running")

            print("Waiting for the instance to reach the running state...")
            waiter.wait(
                InstanceIds=[instance_id],
                WaiterConfig={
                    'Delay': 15,
                    'MaxAttempts': 50
                }
            )
            print(f"Instance {instance_id} is now running.")

        except Exception as e:
            print(f"Error {e}")

    def terminate_instance(client, instance_id):
        try:
            client.terminate_instances(InstanceIds=[instance_id])
            print(f"Instance with ID {instance_id} has been terminated.")

        except Exception as e:
            print(f"Error {e}")

    def menu(key, secret):
        ec2 = boto3.client('ec2', aws_access_key_id=key, aws_secret_access_key=secret, region_name='eu-west-1')

        while True:
            print("-------- EC2 ---------")
            print("0. Back")
            print("1. List all AWS instances")
            print("2. Start instance")
            print("3. Stop instance")
            print("4. Launch a new instance")
            print("5. Terminate instance")
            
            choice = input("Enter choice (1-6): ")

            if choice == "1":
                EC2.list_instances(ec2)

            elif choice == "2":
                EC2.list_instances(ec2)
                instance_id = input("Give instance id to start: ")
                EC2.start_instance(ec2, instance_id)

            elif choice == "3":
                EC2.list_instances(ec2)
                instance_id = input("Give instance id to stop: ")
                EC2.stop_instance(ec2, instance_id)

            elif choice == "4":
                EC2.instance_launch(ec2)

            elif choice == "5":
                EC2.list_instances(ec2)
                instance_id = input("Give instance id to terminate: ")
                EC2.terminate_instance(ec2, instance_id)

            elif choice == "0":
                break
            else:
                print("Invalid choice, please enter a valid option.")
