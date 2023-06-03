import json

f = open('metadata.json')

data = json.load(f)

# for i in data['data']:
#     if


def multiplyEmissionFactor(num, id):

    f = open('metadata.json')
    data = json.load(f)
    total = 0

    for i in data['plasticType']:
        if i['id'] == id:
            total = num * i['emission']

    return total


print(multiplyEmissionFactor(5.475, 2))
