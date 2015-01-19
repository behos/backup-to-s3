# backup-to-s3
An incremental backup to s3 service

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