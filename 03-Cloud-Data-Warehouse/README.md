# Building A Cloud Data Warehouse

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

In this project, an ETL pipeline will be built that extracts data that is in a JSON format from S3. The data is then staged in Redshift and then transformed with into fact/dimension tables using the STAR schema. The data would be transformed (such as converting time recording in miliseconds to TIMESTAMPS) for easy querying for the analysts. 

## Project Structure

```
Cloud Data Warehouse
|____create_tables.py    # Creates the tables
|____etl.py              # Performs ETL
|____sql_queries.py      # Creates the table schema
|____test.ipynb          # To test if the tables are successfully created

```

## Executing the scripts and performing ETL

### Credentials
Proceed to enter the relevent details and crendentials in `dwh.cfg`. 

Unless you have created your own role and have started your own Redshift cluster, `HOST` and `IAM_ROLE`'s ARN would not be available until you run create_delete_cluster.ipynb. 

### Creating and deleting the Redshift cluster in create_delete_cluster.ipynb

When you have completed entering credentials, run PART 1 in its entirety in the `create_delete_cluster.ipynb`. This would instantiate your user role, the Redshift Cluster, and its connection to S3. In the notebook, you will be able to retrieve the Endpoint for the Redshift cluster and the Role ARN that will be added into the `dwh.cfg`.

### Run create_tables.py

This would create staging tables `staging_events` and `staging_songs` that is directly taken and loaded from S3. To prevent the wrong version of the table from being use due to multiple runs, the script will also delete any instance of the tables.

The script additionally creates 5 more tables.
* Fact Table
    * `songplays`
* Dimension Tables
    * `songs`
    * `users`
    * `time`
    * `artists`

The table schema follows the STAR schema

### Run ETL.py

This script would transfer the relevent columns from the staging tables over to the fact and dimension tables. Some processing are filtering for `page` to include `NextSong` only. The timestamp that originally first expressed as miliseconds have been converted to a `TIMESTAMP` format that allows for easier interpretation of dates and time.

### query_text.ipynb

To further verify that the tables are created and inserted correctly, this notebook allows queries to be run to inspect the newly created tables as a sanity check

### Helper script: sql_queries.py

In this script, the schema of the tables are developed and the logic for data transformation appears here

### JSON file for events data

As a note, the json file path file is used because the source data does not have a stable consistent appearence of columns. The JSON file would specifiy the scan of the source file and the corresponding columns in order to ensure that the relevent data is loaded into the correct columns in the staging table.

Good resources about this can be found here:
* https://docs.aws.amazon.com/redshift/latest/dg/r_COPY_command_examples.html#copy-from-json-examples-using-jsonpaths

* https://stackoverflow.com/questions/23835567/copying-json-objects-with-multiple-layouts-from-s3-into-redshift

Sample of the log_data_path.json

```
{
    "jsonpaths": [
        "$.artist",
        "$.auth",
        "$.firstName",
        "$.gender",
		"$.itemInSession",
		"$.lastName",
		"$.length",
		"$.level",
		"$.location",
		"$.method",
		"$.page",
		"$.registration",
		"$.sessionId",
		"$.song",
		"$.status",
		"$.ts",
		"$.userAgent",
		"$.userId"
    ]
}
```



