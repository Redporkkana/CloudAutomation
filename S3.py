import boto3
import os

class S3:
    def __init__(self, access_key, secret_key, region='eu-west-1'):
       self.s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

    def create_bucket(self, bucket_name):
        try:
            response = self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.s3.meta.region_name}
            )
            print(f"Bucket '{bucket_name}' created successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            buckets = response['Buckets']

            if not buckets:
                print("No buckets")
                return

            print("All Buckets:")
            for bucket in buckets:
                print(bucket['Name'])

        except Exception as e:
            print(f"Error: {e}")

    def list_objects_in_bucket(self, bucket_name):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            objects = response.get('Contents', [])
            print(f"Objects in Bucket '{bucket_name}':")
            for obj in objects:
                print(obj['Key'])

        except Exception as e:
            print(f"Error: {e}")

    def upload_an_object(self, bucket_name, file_path, object_key):
        try:
            with open(file_path, 'rb') as data:
                self.s3.upload_fileobj(data, bucket_name, object_key)
            print(f"Object '{object_key}' uploaded to '{bucket_name}'.")

        except Exception as e:
            print(f"Error: {e}")

    def download_an_object(self, bucket_name, object_key):
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read()
            with open(object_key, 'wb') as file:
                file.write(content)
            print(f"Object '{object_key}' downloaded from '{bucket_name}'.")

        except Exception as e:
            print(f"Error: {e}")

    def delete_bucket(self, bucket_name):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            objects = response.get('Contents', [])
            
            if objects:
                print(f"The bucket '{bucket_name}' is not empty.")
                confirmation = input("Do you really want to delete it? (yes/no): ").lower()
                if confirmation != 'yes':
                    print("Deletion aborted.")
                    return

            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' deleted successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def menu(key, secret):
        s3manager = S3(key, secret, 'eu-west-1')

        while True:
            print("-------- S3 ---------")
            print("0. Back")
            print("1. List buckets")
            print("2. List objects in a bucket")
            print("3. Upload an object")
            print("4. Download an object")
            print("5. Delete bucket")
            print("6. Create a bucket")

            choice = input("Enter choice: ")

            if choice == '0':
                break
            elif choice == '1':
                s3manager.list_buckets()
            elif choice == '2':
                s3manager.list_buckets()
                bucket_name = input("Give bucket name: ")
                s3manager.list_objects_in_bucket(bucket_name)

            elif choice == '3':
                s3manager.list_buckets()
                file_path = input("Enter the path of the file to upload: ")
                bucket_name = input("Give bucket name to upload to: ")
                object_key = input("Give file name: ") # should really get from the file itself
                s3manager.upload_an_object(bucket_name, file_path, object_key)

            elif choice == '4':
                s3manager.list_buckets()
                bucket_name = input("Give bucket name to list objects from: ")
                s3manager.list_objects_in_bucket(bucket_name)

                object_key = input("Give file name to download: ")
                s3manager.download_an_object(bucket_name, object_key)

            elif choice == '5':
                s3manager.list_buckets()
                bucket_name = input("Give bucket ID to delete: ")
                s3manager.delete_bucket(bucket_name)

            elif choice == '6':
                new_bucket_name = input("Enter the new bucket name: ")
                s3manager.create_bucket(new_bucket_name)
            else:
                print("Invalid choice, please enter a valid option.")