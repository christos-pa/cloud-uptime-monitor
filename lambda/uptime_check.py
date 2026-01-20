import os
import json
import urllib.request
import urllib.error
import boto3
import time

sns = boto3.client("sns")

TARGET_URL = os.environ.get("TARGET_URL", "http://18.169.182.53")
TOPIC_ARN = os.environ.get("TOPIC_ARN", "")
TIMEOUT_SECONDS = int(os.environ.get("TIMEOUT_SECONDS", "6"))

def lambda_handler(event, context):
    start = time.time()
    status = None
    ok = False
    error = None

    try:
        req = urllib.request.Request(
            TARGET_URL,
            headers={"User-Agent": "uptime-monitor/1.0"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            status = resp.getcode()
            ok = 200 <= status < 400

    except urllib.error.HTTPError as e:
        status = e.code
        ok = False
        error = f"HTTPError: {e}"

    except Exception as e:
        ok = False
        error = f"{type(e).__name__}: {e}"

    latency_ms = int((time.time() - start) * 1000)

    summary = {
        "target": TARGET_URL,
        "ok": ok,
        "status": status,
        "latency_ms": latency_ms,
        "error": error,
    }
    print(json.dumps(summary))

    if (not ok) and TOPIC_ARN:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"[ALERT] Uptime check failed ({status})",
            Message=json.dumps(summary, indent=2),
        )

    return summary
