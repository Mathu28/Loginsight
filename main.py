from fastapi import FastAPI
from cloudtrail_processor import process_cloudtrail_csv

app = FastAPI(title="CloudTrail Log Processing API")

@app.get("/process-cloudtrail")
def process_cloudtrail():
    bucket_name = "cloudtrail-log-details-storage-bucket"
    file_key = "archive/dec12_18features.csv"

    processed, sentences = process_cloudtrail_csv(
        bucket_name,
        file_key
    )

    return {
        "status": "success",
        "processed_logs": processed,
        "sample_output": sentences[:5]
    }
