import boto3


def snsmain(title, body, sns_topic):
    
    sns_client = boto3.client("sns", region_name='ap-southeast-1')
    print("Sending sns")
    response = sns_client.publish(
        TopicArn=sns_topic,
        Message=body,
        Subject=title[:100]
    )
    
def notify_unauthorized_s3_action(event_data ,sns_topic):
    
    # Format the row data into a message
    email_body = (
        f"An Unaothorized Event of : {event_data['eventname']} has detected from source ip  :  {event_data['sourceipaddress']}  \n"
        f"Please check s3 logs for a Detailed View"
       
    )

    title = "Unauthorized {} detected On {}".format(event_data['eventname'] , event_data['bucketName'])
    body = """
    Hi All,

    {}

    Thanks
    """.format(email_body)


    try:
        snsmain(title, body, sns_topic)
    except Exception as e:
        print("An exception occurred" , e)