import os
import boto3
import datetime

# Initialize RDS client
rds_client = boto3.client('rds', region_name=os.environ['CLUSTER_REGION'])

# Define the RDS cluster identifier (replace with your cluster ID)
rds_cluster_id = os.environ['RDS_CLUSTER_ID']

def lambda_handler(event, context):
    try:
        # Create a snapshot name based on the current date and time
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        snapshot_id = f'{rds_cluster_id}-snapshot-{timestamp}'
        
        # Create a snapshot for the RDS cluster
        response = rds_client.create_db_cluster_snapshot(
            DBClusterSnapshotIdentifier=snapshot_id,
            DBClusterIdentifier=rds_cluster_id
        )
        print(f"Snapshot {snapshot_id} created successfully.")
        
        # Now call a function to clean up snapshots older than 10 weeks
        delete_old_snapshots(rds_cluster_id)
        
    except Exception as e:
        print(f"Error creating snapshot: {e}")

def delete_old_snapshots(cluster_id):
    try:
        # Fetch all snapshots for the given cluster
        snapshots = rds_client.describe_db_cluster_snapshots(
            DBClusterIdentifier=cluster_id,
            SnapshotType='manual'
        )
        
        # Get the current date
        now = datetime.datetime.now()
        
        # Iterate through the snapshots and delete those older than 10 weeks
        for snapshot in snapshots['DBClusterSnapshots']:
            snapshot_id = snapshot['DBClusterSnapshotIdentifier']
            snapshot_date = snapshot['SnapshotCreateTime'].replace(tzinfo=None)
            
            # Calculate the age of the snapshot
            age_in_weeks = (now - snapshot_date).days // 7
            
            if age_in_weeks > 10:
                # Delete the snapshot
                rds_client.delete_db_cluster_snapshot(
                    DBClusterSnapshotIdentifier=snapshot_id
                )
                print(f"Deleted snapshot: {snapshot_id}, Age: {age_in_weeks} weeks")
            else:
                print(f"Snapshot {snapshot_id} is {age_in_weeks} weeks old and will be retained.")
                
    except Exception as e:
        print(f"Error deleting old snapshots: {e}")

