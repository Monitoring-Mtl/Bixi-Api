import json


def lambda_handler(event, context):
    route_key = f"{event['httpMethod']} {event['resource']}"

    # Set default response
    response_body = {"Message": "Unsupported route"}
    status_code = 400
    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

    try:
        # Handle average trip duration query
        if route_key == "GET /trip-durations/average":
            # Extract query parameters
            startTime = event["queryStringParameters"]["startTime"]
            endTime = event["queryStringParameters"]["endTime"]
            # Optional: Handle filtering by start and end stations and arrondissements

            # Logic to calculate average trip duration based on the parameters
            # Placeholder
            average_duration = "15 minutes"
            total_trips = 320

            response_body = {
                "averageDuration": average_duration,
                "totalTrips": total_trips,
                "queryParameters": {
                    "startTime": startTime,
                    "endTime": endTime,
                },
            }
            status_code = 200

    except Exception as e:
        status_code = 500
        response_body = {"Error": str(e)}
        print(str(e))

    return {
        "statusCode": status_code,
        "body": json.dumps(response_body),
        "headers": headers,
    }
