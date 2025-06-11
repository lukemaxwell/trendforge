import stripe
from fastapi import FastAPI, Request, HTTPException
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase Admin
cred = credentials.ApplicationDefault()
initialize_app(cred)
db = firestore.Client()

# Stripe secret (you'll inject this via env var)
import os
stripe.api_key = os.getenv("STRIPE_API_KEY")
endpoint_secret = os.getenv("STRIPE_ENDPOINT_SECRET")  # Your webhook signing secret

app = FastAPI()

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail="Invalid webhook")

    # Handle checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get("customer_email")
        stripe_customer_id = session.get("customer")
        
        # Here you'd look up the Firebase user linked to this email
        # For demo, assume user_id == email (you'll map this properly)
        user_id = customer_email

        doc_ref = db.collection("users").document(user_id)
        doc_ref.set({
            "email": customer_email,
            "stripe_customer_id": stripe_customer_id,
            "subscription_status": "active",
            "subscription_plan": "pro"
        }, merge=True)

        print(f"Updated subscription for {customer_email}")

    return {"status": "success"}
