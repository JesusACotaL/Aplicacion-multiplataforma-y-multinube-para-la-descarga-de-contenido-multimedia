from generar_ratings import generar_ratings
import recomendaciones

# userInput = [
#         {'title': 'Slam Dunk', 'rating': 5},
#         {'title': 'Oyasumi Punpun', 'rating': 3.5},
#         {'title': 'Houseki no Kuni', 'rating': 2},
#         {'title': "Berserk", 'rating': 1},
#         {'title': 'Ashita no Joe', 'rating': 4.5}
#     ]

userInput = generar_ratings('mwF5DVD0KXN7tVwygzjQRtQvNtj2')
print(userInput)
# reco = recomendaciones.obtener_recomendaciones(userInput)
# generos = recomendaciones.obtener_generos(userInput)

# print(generos)
# print(reco)