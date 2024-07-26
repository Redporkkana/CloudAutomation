import boto3
import EC2

class EBSStorage:
    def __init__(self, access_key, secret_key, region='eu-west-1'):
       self.ec2 = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

    def list_volumes(self):
        try:
            response = self.ec2.describe_volumes()
            volumes = response['Volumes']

            if not volumes: 
                print("No volumes found.")
                return
            
            for volume in volumes:
                print(f"Volume ID: {volume['VolumeId']}, Size: {volume['Size']} GiB, Status: {volume['State']}")
        except Exception as e:
            print(f"Error {e}")

    def create_volume(self, size_str, availability_zone):
        try:
            size = int(size_str)
            response = self.ec2.create_volume(
                Size=size,
                AvailabilityZone=availability_zone
            )
            print(f"Volume ID: {response['VolumeId']} created successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def attach_existing_volume_to_instance(self, volume_id, instance_id, device):
        try:
            response = self.ec2.attach_volume(
                VolumeId=volume_id,
                InstanceId=instance_id,
                Device=device
            )
            print(f"Volume ID: {volume_id} attached to Instance ID: {instance_id} on device: {device}.")

        except Exception as e:
            print(f"Error: {e}")

    def detatch_volume_from_instance(self, volume_id):
        try:
            response = self.ec2.detach_volume(
                VolumeId=volume_id
            )
            print(f"Volume ID: {volume_id} detached successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def modify_volume(self, volume_id, new_size_str):
        try:
            new_size = int(new_size_str)
            response = self.ec2.modify_volume(
                VolumeId=volume_id,
                Size=new_size
            )
            print(f"Volume ID: {volume_id} modified successfully. New size: {new_size} GiBs.")

        except Exception as e:
            print(f"Error: {e}")

    def list_snapshots(self):
        try:
            response = self.ec2.describe_snapshots()
            snapshots = response['Snapshots']
            for snapshot in snapshots:
                print(f"Snapshot ID: {snapshot['SnapshotId']}, Volume ID: {snapshot['VolumeId']}, State: {snapshot['State']}")

        except Exception as e:
            print(f"Error: {e}")

    def take_snapshot(self, volume_id, description):
        try:
            response = self.ec2.create_snapshot(
                VolumeId=volume_id,
                Description=description
            )
            print(f"Snapshot ID: {response['SnapshotId']} created successfully for Volume ID: {volume_id}.")

        except Exception as e:
            print(f"Error: {e}")

    def create_volume_from_snapshot(self, snapshot_id, availability_zone):
        try:
            response = self.ec2.create_volume(
                SnapshotId=snapshot_id,
                AvailabilityZone=availability_zone
            )
            print(f"Volume ID: {response['VolumeId']} created successfully from Snapshot ID: {snapshot_id}.")

        except Exception as e:
            print(f"Error: {e}")

    def menu(key, secret):
        ebsstorage = EBSStorage(key, secret, 'eu-west-1')

        while True:
            print("-------- EBS Volumes ---------")
            print("1. List all volumes")
            print("2. Create a new volume")
            print("3. Attach existing volume to an instance")
            print("4. Detach a volume from an instance")
            print("5. Modify volume size")
            print("6. List all snapshots")
            print("7. Take a snapshot of a volume")
            print("8. Create volume from a snapshot")
            print("9. Back ")

            choice = input("Enter choice (1-9): ")

            if choice == '1':
                ebsstorage.list_volumes()
            elif choice == '2':
                size = input("Give size of new volume in GiBs (1-1024): ")
                ebsstorage.create_volume(size, 'eu-west-1c')

            elif choice == '3':
                ebsstorage.list_volumes()
                EC2.EC2.list_instances(ebsstorage.ec2)

                volume_id = input("Give volume ID of volume: ")
                instance_id = input("Give instance ID to attach volume to: ")

                ebsstorage.attach_existing_volume_to_instance(volume_id, instance_id, '/dev/sdf')

            elif choice == '4':
                ebsstorage.list_volumes()
                volume_id = input("Give volume ID to detach from: ")
                ebsstorage.detatch_volume_from_instance(volume_id)

            elif choice == '5':
                ebsstorage.list_volumes()
                volume_id = input("Give volume ID which size to modify: ")
                size = input("Give new size in GB: ")
                ebsstorage.modify_volume(volume_id, size)

            elif choice == '6':
                ebsstorage.list_snapshots()

            elif choice == '7':
                ebsstorage.list_volumes()
                volume_id = input("Give volume ID to take snapshot from: ")
                description = input("Give description for the snapshot: ")
                ebsstorage.take_snapshot(volume_id, description)

            elif choice == '8':
                ebsstorage.list_snapshots()
                snapshot_id = input("Give snapshot ID to create volume from: ")
                ebsstorage.create_volume_from_snapshot(snapshot_id, 'eu-west-1c')

            elif choice == '9':
                break
            else:
                print("Invalid choice, please enter a valid option.")