from google.cloud import firestore

db = firestore.Client()

# Example: read subscription status
def get_subscription_status(user_id):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return data.get("subscription_status", "free")
    else:
        return "free"
