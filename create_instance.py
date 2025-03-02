
import boto3
from botocore.exceptions import ClientError
import pprint


def main():

    ec2_client = boto3.client('ec2')

	
    image_id = 'ami-07d0cf3af28718ef8'
    instance_type = 't2.micro'
    keypair_name = 'Imaran-key'
  
  
    try:
        response = ec2_client.run_instances(ImageId=image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            MinCount=1,
                                            MaxCount=1,
											TagSpecifications=[
												{
													'ResourceType': 'instance',
													'Tags': [
														{
															'Key': 'Name',
															'Value': 'Python Instance'
														}
													]
												}
											],
	                                        )
											
        pprint.pprint (response['Instances'][0])
        
    except ClientError as e:
        print (e)

if __name__ == '__main__':
    main()
