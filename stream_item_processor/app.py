import json


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

    print(json.dumps(event, indent=2))
    return None
