import requests

BASE = "http://127.0.0.1:5000/"

image_to_insert = {"x_pos": 0.2, "y_pos": 0.3}
i = 0

response = requests.get(BASE + "image/" + str(i))
print(response.json())
response = requests.post(BASE + "image/" + str(i), image_to_insert)
print(response.json())
response = requests.put(BASE + "image/" + str(i), image_to_insert)
print(response.json())
response = requests.delete(BASE + "image/" + str(i))
print(response)


# Before
data = [{"x_pos": 0.3, "y_pos": 0.1},
        {"x_pos": 0.7, "y_pos": 0.2},
        {"x_pos": 0.1, "y_pos": 0.1}]

for i in range(len(data)):
    response = requests.post(BASE + "image/" + str(i), data[i])
    print(response.json())


val = data[0]
val["x_pos"] = 0.5

input()
response = requests.put(BASE + "image/0", val)
print(response.json())

input()
response = requests.delete(BASE + "image/0")
print(response)

input()
response = requests.get(BASE + "image/2")
print(response.json())
