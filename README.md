# Trade Assignment Project

## Assumptions
1. Trades are being transmitted to local path from where code will pick the trades
2. Trade Store is in CSV format stored locally
3. As this is python code, code deployment only means cloning repository where it needs to be executed
4. Same goes for promotion to higher environment
5. Assumption data is flowing during trade hours
6. Outside trade hours, update_expiry function will be scheduled

## Cloud Integration
1. Input can be assumed from AWS Kinesis and storing in S3
2. Once trades stored in s3, Lambda event is triggered.
3. Lambda will process the trades and update trade store
4. Trade store is stored in S3

## Instructions
1. Create Python environment with requirements.txt file
2. For checking test coverage run below command
    pytest --cov-report term-missing --cov=./