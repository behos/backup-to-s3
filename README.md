# backup-to-s3
An incremental backup to s3 service

## Introduction

A tool which will help you backup a directory incrementally in an s3 bucket which offers the option to recover snapshots

### Configuration

Create a file called config.yml in your ~/.backup-to-s3 directory and add the following

    database_path: ~/.backup-to-s3/snapshot.db

    source:
        type: local
            base_path: /path/to/backup

    destination:
        type: s3
            bucket_name: backup-bucket
	        access_key_id: [Amazon S3 Access key Id]
	            secret_access_key: [Amazon S3 Secret access key]

This is a basic configuration which will search you backup folder for changes and upload any changes to the S3 bucket.

At the moment you need to make sure that the database is in a safe place. In the future it will be uploaded to S3 along with the backups so that it's always recoverable.

### Performing the backups

If you have this package globally installed you can run it using

   python -m backup_to_s3

This will perform the backup according to the configuration

### Restoring a backup

    python -m backup_to_s3 --restore

This will show you a list of all the taken snapshots ordered by most recent. You can choose a snapshot to restore by entering its id

## Development

### virtualenv

Create and activate a virtualenv by running

    . activate

### Testing

Run the tests by running

    ./test

This will run all the tests and flake8 for the whole project.

Some tests require an s3 bucket and the credentials to be available in a configuration file

Edit ~/.backup-to-s3/config.yml and add the following lines

    s3_tests:
        bucket_name: [name of the bucket to use for testing]
        access_key_id: [the access key id]
        secret_access_key: [the secret access key]

These settings will then be detected when running the tests and be used if able.