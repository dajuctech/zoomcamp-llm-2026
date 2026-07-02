from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

q1 = "I just discovered the course, can I still join?"
q2 = "I just found out about the program, can I still enroll?"

v1 = model.encode(q1)
v2 = model.encode(q2)

print(v1.shape)
print(v1.dot(v2))