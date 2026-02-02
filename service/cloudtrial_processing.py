import csv
import io
from s3_client import get_s3_client

def process_cloudtrail_csv(bucket_name: str, file_key: str):
    s3 = get_s3_client()

    response = s3.get_object(
        Bucket=bucket_name,
        Key=file_key
    )

    stream = io.TextIOWrapper(
        response["Body"],
        encoding="utf-8",
        errors="replace"
    )

    reader = csv.reader(stream)
    headers = next(reader)

    processed = 0
    sentences = []

    for row in reader:
        if len(row) != len(headers):
            continue

        data = dict(zip(headers, row))

        sentence = (
            f"At {data.get('eventTime')}, "
            f"user {data.get('userIdentityuserName')} "
            f"performed {data.get('eventName')} "
            f"from IP {data.get('sourceIPAddress')} "
            f"in region {data.get('awsRegion')}."
        )

        sentences.append(sentence)
        processed += 1

    return processed, sentences
