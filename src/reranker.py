from sentence_transformers import CrossEncoder


model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


pairs = [

    (
        "What is a process?",
        "A process is a running program."
    ),

    (
        "What is a process?",
        "Operating systems have projects."
    )

]


scores = model.predict(pairs)


for score in scores:
    print(score)