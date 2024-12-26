# RDS Snapshot Manager

This project is an AWS Lambda-based solution to manage RDS Cluster snapshots. It automates the creation of weekly snapshots and deletes snapshots older than 10 weeks to ensure efficient snapshot lifecycle management.

## Features

- **Automated Snapshot Creation:** The Lambda function creates a new snapshot for a specified RDS Cluster on a weekly schedule.
- **Snapshot Cleanup:** Automatically deletes manual snapshots older than 10 weeks to manage storage costs.
- **Configurable Scheduling:** Uses AWS EventBridge (CloudWatch Events) to trigger the function based on a cron expression.
- **IAM Role Permissions:** Ensures the function has the required permissions to interact with RDS, CloudWatch, and Lambda logs.

---

## Requirements

- AWS CLI configured with appropriate access.
- Python 3.8 or higher.
- Serverless Framework installed.
- AWS RDS Cluster to manage snapshots.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the required environment variables:
   ```dotenv
   CLUSTER_REGION=your-cluster-region
   RDS_CLUSTER_ID=your-rds-cluster-id
   AWS_ACCOUNT_ID=your-aws-account-id
   ```

---

## Deployment

Deploy the service using the Serverless Framework:
```bash
sls deploy --stage <stage>
```

This will deploy the Lambda function and set up the EventBridge rule to trigger it weekly.

---

## Configuration

### Cron Schedule
The function is scheduled to run weekly using the following cron expression:
```yaml
rate: cron(0 0 ? * 3 *)
```
- This triggers the function at midnight every Wednesday.
- Adjust the schedule as needed in `serverless.yml` under the `functions.rdsSnapshotManager.events` section.

### IAM Permissions
The function requires the following IAM permissions:
- `rds:CreateDBClusterSnapshot`
- `rds:DeleteDBClusterSnapshot`
- `rds:DescribeDBClusterSnapshots`
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`
- `lambda:InvokeFunction`

These permissions are pre-configured in the `serverless.yml` file.

---

## How It Works

1. The Lambda function is triggered by an EventBridge rule.
2. It creates a snapshot of the specified RDS Cluster with a timestamp-based identifier.
3. The function then checks for all manual snapshots of the cluster.
4. Snapshots older than 10 weeks are deleted to free up storage.

---

## File Structure

```
|-- handler.py          # Lambda function logic
|-- serverless.yml      # Serverless Framework configuration
|-- requirements.txt    # Python dependencies
|-- .gitignore          # Files and folders to ignore in Git
|-- .env                # Environment variables (excluded from Git)
```

---

## Testing

### Local Testing

1. Run the Lambda function locally using the Serverless Framework:
   ```bash
   sls invoke local --function rdsSnapshotManager --stage <stage>
   ```

2. Pass mock event data if required.

### Deployment Testing
After deployment, monitor the function's execution in AWS CloudWatch Logs to verify it:
1. Successfully creates snapshots.
2. Deletes old snapshots older than 10 weeks.

---

## Plugins Used

1. **serverless-python-requirements:** Packages Python dependencies for the Lambda function.
2. **serverless-dotenv-plugin:** Loads environment variables from the `.env` file.

---

## Troubleshooting

- Ensure the RDS Cluster exists and is accessible in the specified region.
- Verify the IAM role has sufficient permissions.
- Check AWS CloudWatch Logs for detailed error messages in case of failures.
- Ensure the `CLUSTER_REGION` and `RDS_CLUSTER_ID` environment variables are set correctly.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

