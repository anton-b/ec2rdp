import boto3
import dotenv
dotenv.load_dotenv()
import os

def verify_credentials():
    try:
        boto3.client('sts').get_caller_identity()
        print_green("AWS credentials are valid.")
        return True
    except Exception as e:
        print_red(f"Error verifying AWS credentials: {e}")
        exit(1)

def list_ec2_instances():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'State': instance['State']['Name'],
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A')
                })
        if instances:
            print_blue("EC2 Instances:")
            for instance in instances:
                print(f"ID: {instance['InstanceId']}, State: {instance['State']}, Public IP: {instance['PublicIpAddress']}")
        else:
            print_yellow("No EC2 instances found.")
    except Exception as e:
        print_red(f"Error listing EC2 instances: {e}")

def start_ec2_instance(instance_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        print_green(f"Starting instance {instance_id}...")
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        print_green(f"Instance {instance_id} is now running.")
    except Exception as e:
        print_red(f"Error starting instance {instance_id}: {e}")

def stop_ec2_instance(instance_id, wait=True):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print_green(f"Stopping instance {instance_id}...")
        if wait:
            waiter = ec2.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[instance_id])
            print_green(f"Instance {instance_id} is now stopped.")
        else:
            print_yellow(f"Instance {instance_id} is stopping, but not waiting for it to stop.")
    except Exception as e:
        print_red(f"Error stopping instance {instance_id}: {e}")

def connect_rdp(instance_id, username='Administrator', password=''):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        public_ip = instance.get('PublicIpAddress')
        if public_ip:
            print_blue(f"Connecting to {instance_id} via RDP at {public_ip}...")
            os.system(f"remmina -c rdp://{username}@{public_ip}")
        else:
            print_yellow(f"No public IP found for instance {instance_id}.")
    except Exception as e:
        print_red(f"Error connecting to instance {instance_id}: {e}")

def decrypt_windows_password(pkey_pem, instance_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.get_password_data(InstanceId=instance_id)
        breakpoint()
        if response['PasswordData']:
            password = response['PasswordData']
            
            return password
        else:
            print_yellow(f"No password data available for instance {instance_id}.")
            return None
    except Exception as e:
        print_red(f"Error decrypting password for instance {instance_id}: {e}")
        return None
        
def colour_print(text, colour):
    colours = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'end': '\033[0m'
    }
    print(f"{colours.get(colour, colours['end'])}{text}{colours['end']}")

def print_blue(text):
    colour_print(text, 'blue')

def print_red(text):
    colour_print(text, 'red')
    
def print_green(text):
    colour_print(text, 'green')
    
def print_yellow(text):
    colour_print(text, 'yellow')
