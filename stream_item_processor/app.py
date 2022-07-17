import json
from datetime import datetime, timezone


PK_NAME = "PK"


def lambda_handler(event, context):
    """Lambda function to process DynamoDB stream items

    Parameters
    ----------
    event: dict, required
    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    None
    """

    records = event["Records"]
    for record in records:
        event_type = record["eventName"]
        pk_val = record["dynamodb"]["Keys"][PK_NAME]["S"]
        approx_creation_datetime = datetime.fromtimestamp(
            record["dynamodb"]["ApproximateCreationDateTime"],
            timezone.utc
        )

        flat_new_image = {}

        if event_type in ["INSERT", "MODIFY"]:
            new_image = record["dynamodb"]["NewImage"]
            for key, data in new_image.items():
                flat_new_image[key] = list(data.values())[0]
        elif event_type == "REMOVE":
            flat_new_image[PK_NAME] = pk_val
        else:
            continue

        flat_new_image["DynamoDbOperation"] = event_type
        flat_new_image["DynamoDbOperationTime"] = approx_creation_datetime.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        print(json.dumps(flat_new_image))

    return None
