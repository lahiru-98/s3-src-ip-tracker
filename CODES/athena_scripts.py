import time
import boto3






def read_sql_from_file(file_path):
    """read sql string in the file path"""
     
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', ' ')

    return data


def run_athena_query(query , DATABASE_NAME , OUTPUT_LOCATION):
    """Runs an Athena query and returns the result."""
    
    athena_client = boto3.client('athena')

    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE_NAME},
        ResultConfiguration={'OutputLocation': OUTPUT_LOCATION}
    )
    
    query_execution_id = response['QueryExecutionId']

    print(f"Running query with execution ID: {query_execution_id}")
    
    while True:
        result = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']
        
        if status == 'SUCCEEDED':
            print("Query succeeded.")
            break
        elif status == 'FAILED' or status == 'CANCELLED':
            print("Query failed or was cancelled.")
            return None
        else:
            print("Query is still running...")
            time.sleep(5)  # Wait before polling again
    
    result = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    return result

