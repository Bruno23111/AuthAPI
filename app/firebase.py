import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Evita inicializar o Firebase mais de uma vez
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
