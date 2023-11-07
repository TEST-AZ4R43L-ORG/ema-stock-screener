import json
import boto3
import datetime
def publish_to_sns(table):
    HTML_EMAIL_CONTENT = """Today's Stock Eval: "{}""".format(table)


    topic_arn = "arn:aws:sns:us-east-1:123456789124:StockNotifier"
    sns = boto3.client("sns", region_name="us-east-1")
    response = sns.publish(TargetArn=topic_arn,Message=HTML_EMAIL_CONTENT,Subject="Recent Stock Flags - "+datetime.datetime.now().strftime('%d-%m-%Y'))
    
def lambda_handler(event, context):
    # TODO implement
    # print(event)
    # event=json.loads(event)
    # print(event)
    # base64_bytes=event.get("html")
    # html=base64_bytes.decode("ascii")
    # html=json.loads(event["Payload"])["html"]
    html=event.get("html")
    with open("/tmp/StockHistory3.html", "w") as f:
        f.write(html)
        f.close()
    random_string=datetime.datetime.now().strftime('%f')
    s3_ = boto3.resource('s3', region_name="us-east-1")
    print("got s3 resource")
    file_path="https://sins3bucektvalue-ue.s3.us-east-1.amazonaws.com/"
    file_name=datetime.datetime.now().strftime('%Y-%m-%d')+'-'+random_string+'z'
    file_path+=file_name+'.html'
    
    print("creating s3 object")
    object = s3_.Object('sins3bucektvalue-ue', file_name+'.html')
    print("going to put object")
    result = object.put(Body=open('/tmp/StockHistory3.html', 'rb'),ContentType='xml')
    print(file_path)
    publish_to_sns(file_path)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
