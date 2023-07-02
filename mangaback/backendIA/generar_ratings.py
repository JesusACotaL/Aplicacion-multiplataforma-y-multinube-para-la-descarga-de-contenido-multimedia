import firebase_admin
from firebase_admin import credentials, firestore
import csv

def export_ratings_to_csv(uid):
    # Inicializar la conexión con Firestore
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Consultar la colección "ratings" filtrando por el uid
    query = db.collection('ratings').where('uid', '==', uid).get()

    # Lista para almacenar los datos
    data = []

    # Iterar sobre los documentos obtenidos y extraer los campos
    for doc in query:
        rating = doc.get('ratings')
        title = doc.get('title')

        # Agregar los datos a la lista
        data.append([uid, title, rating])

    # Escribir los datos en un archivo CSV
    with open('ratings2.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['uid', 'title', 'rating'])
        writer.writerows(data)

    print("Archivo CSV generado con éxito.")
