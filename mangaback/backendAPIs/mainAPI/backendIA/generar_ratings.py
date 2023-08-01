from firebase_admin import credentials, firestore, initialize_app

def generar_ratings(uid):
    # Inicializar la conexión con Firestore
    cred = credentials.Certificate('firebase-credentials.json')
    initialize_app(cred)
    db = firestore.client()

    # Consultar la colección "ratings" filtrando por el uid
    query = db.collection('ratings').where('uid', '==', uid).get()

    # Lista para almacenar los datos
    data = []

    # Iterar sobre los documentos obtenidos y extraer los campos
    for doc in query:
        title = doc.get('title')
        rating = float(doc.get('ratings'))

        # Agregar los datos a la lista
        data.append({
            'name': title,
            'rating': rating
        })
    return data