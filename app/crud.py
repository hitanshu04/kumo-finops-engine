from sqlalchemy.orm import Session
from . import models, schemas
import requests
import json
import os

# --- SECURITY FIX: Read from Environment Variable ---
# If the variable is missing, it returns None (safe)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(service: str, amount: float, average: float):
    if not SLACK_WEBHOOK_URL:
        print("⚠️ SLACK ALERT SKIPPED: No Webhook URL found in environment.")
        return

    payload = {
        "text": f"🚨 *FINOPS ALERT: High Spending Detected!*",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚨 *High Cost Detected!* \n\n*Service:* {service}\n*Cost:* ${amount}\n*Normal Average:* ${average:.2f}"
                }
            }
        ]
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")


def create_cost(db: Session, cost: schemas.CloudCostCreate):
    # 1. Fetch History
    last_costs = db.query(models.CloudCost)\
        .filter(models.CloudCost.service == cost.service)\
        .order_by(models.CloudCost.timestamp.desc())\
        .limit(5)\
        .all()

    is_anomaly = False
    average = 0.0

    # 2. Logic
    if last_costs:
        total = sum(c.amount for c in last_costs)
        average = total / len(last_costs)

        if cost.amount > (average * 2):
            is_anomaly = True
            print(f"🚨 ANOMALY! Sending to Slack...")
            send_slack_alert(cost.service, cost.amount, average)

    # 3. Save
    db_cost = models.CloudCost(
        service=cost.service,
        amount=cost.amount,
        is_anomaly=is_anomaly
    )
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost


def get_costs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CloudCost).offset(skip).limit(limit).all()
