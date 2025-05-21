import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Evita inicializar o Firebase mais de uma vez
if not firebase_admin._apps:
    # Lê um arquivo .json que contém a chave privada de acesso ao Firebase.
    cred = credentials.Certificate("firebase-credentials.json")
    # Inicializa a aplicação Firebase
    firebase_admin.initialize_app(cred)
    
# Inicializa o cliente de banco de dados Firestore, armazenado na variável db
db = firestore.client()
