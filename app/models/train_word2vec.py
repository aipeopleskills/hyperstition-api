import gensim
import os

# Datos de entrenamiento (puedes ampliarlo con más textos)
corpus = [
    ["control", "poder", "narrativa", "manipulación", "colapso", "historia", "orden", "total"],
    ["manipulación", "mediática", "control", "total", "poder", "conspiración"],
    ["tecnología", "cambio", "sociedad", "futuro", "apocalipsis", "utopía"],
    ["nueva", "era", "iluminación", "despertar", "conciencia"],
]

# Entrenar el modelo Word2Vec
model = gensim.models.Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=4)

# Guardar el modelo en `app/models/word2vec.model`
model_path = "app/models/word2vec.model"
model.save(model_path)

print(f"✅ Modelo entrenado y guardado en {model_path}")

