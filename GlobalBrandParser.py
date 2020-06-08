import json

with open("data.json") as json_file:
    data = json.load(json_file)
newData = []
idx = 0
for key in data["products"]:
    product = data["products"][key]
    img = product["imageUrl"]
    if len(img) > 4:
        if img[:4] == "data":
            img = "default.png"
    if(product['name']=='Unpackaged'):
        img="https://i.imgur.com/1myQPDG.png"
    unit = product["unit"]
    if unit == "1":
        unit = "kg"
    elif unit == "2":
        unit = "piece"
    elif unit == "3":
        unit = "ltr"
    elif unit == "4":
        unit = "ml"
    elif unit == "5":
        unit = "gm"

    price = product["mrp"]
    print(price)
    if "{" in price:
        fprice = {}
        unwanted = ["{", "}", " "]
        for un in unwanted:
            price = price.replace(un, "")
            arr = price.split(",")
        for itm in arr:
            temp = itm.split(":")
            fprice[str(temp[0]) + " " + str(unit)] = int(temp[1])
        price = fprice
    elif "[" in price:
        price = price.replace("[", "")
        price = price.replace("]", "")
        price = price.replace(" ", "")
        fprice = {"price": list(map(int, price.split(",")))}
        price = fprice
    else:
        fprice = {"price": int(price.replace(" ", ""))}
        price = fprice
    # print(price)
    temp = {
        "brand": product["name"],
        "displayImg": img,
        "packed": (product["productType"] == "packed"),
        "item": "-".join(product["subCategory"].split(" ")),
    }
    newData.append(temp)

# print(newData)
with open("GlobalBrand.json", "w") as json_file:
    json.dump(newData, json_file)
