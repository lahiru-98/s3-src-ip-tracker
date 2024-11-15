import time
import boto3
from sns_scripts import notify_unauthorized_s3_action
from athena_scripts import read_sql_from_file  , run_athena_query


athena_client = boto3.client('athena')
s3_client = boto3.client('s3')

RESULT_BUCKET = 'athena-query-results-dlg-lahiru'
DATABASE_NAME = '"aws:cloudtrail"'
OUTPUT_LOCATION = f's3://{RESULT_BUCKET}/results/'

SRC_IP_TRACK_QUERY = "./queries/ip_track.sql"
ALERT_SNS_TOPIC_ARN = 'arn:aws:sns:ap-southeast-1:027516672101:s3-unauthorized-access-topic'




def analyze_results(results):
    """Analyze Athena query results."""
    if not results:
        print("No results to analyze.")
        return
    
    column_names = [column['Name'] for column in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
    print(f"Column Names: {column_names}")
    

    if len(results['ResultSet']['Rows']) > 1:  
    
        first_row = results['ResultSet']['Rows'][1]  # 1 because 0th is the header
        row_data = {column_names[i]: first_row['Data'][i].get('VarCharValue', None) 
                    for i in range(len(column_names))}
        
        
        notify_unauthorized_s3_action(row_data , ALERT_SNS_TOPIC_ARN)
        
    else:
        print("No data rows found.")
        
    


def lambda_handler(event, context):
    
    query = read_sql_from_file(SRC_IP_TRACK_QUERY) 
    
    print("Running Athena query...", query)

    results = run_athena_query(query , DATABASE_NAME , OUTPUT_LOCATION )
    
    if results:
        analyze_results(results)
    else:
        print("No results to analyze.")

