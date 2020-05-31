import json
from googletrans import Translator
import csv

translator = Translator()

with open("data.json") as json_file:
    data = json.load(json_file)

newData = {}
idx = 0
for key in data["products"]:
    product = data["products"][key]
    img = product["imageUrl"]
    if len(img) > 4:
        if img[:4] == "data":
            img = "default.png"
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
    item = "-".join(product["subCategory"].split(" "))

    # item="-".join(product["subCategory"].split(" "))
    temp = {
        "brand": product["name"],
        "displayImg": img,
        "packed": (product["productType"] == "packed"),
        "item": item,
    }
    if item not in newData:
        newData[item] = {"prices": {}, "unit": set(), "quantifier": set()}
    newData[item]["prices"][str(product["name"])] = price
    newData[item]["unit"].add(unit)
    newData[item]["quantifier"].add(product["quantifier"])
# print(newData)

# with open("Test.json", "w") as json_file:
#     json.dump(newData, json_file)

newData2 = {}
for key in data["products"]:
    product = data["products"][key]
    category = "-".join(product["category"].strip().split(" "))
    subCategory = "-".join(product["subCategory"].strip().split(" "))
    category = category.replace(",", "")
    if category in newData2:
        newData2[category].add(subCategory)
    else:
        newData2[category] = set()

# print(newData2.keys)
globalItemDb = []
for gCategory in newData2.keys():
    for gItem in newData2[gCategory]:
        hindiName = translator.translate(str(gItem), dest="hi").text
        print(hindiName)
        temp = {
            "item": gItem,
            "itemInHindi": hindiName,
            "category": gCategory,
            "unit": "/".join(list(newData[gItem]["unit"])),
            "quantifier": "/".join(list(newData[gItem]["quantifier"])),
            "Prices": newData[gItem]["prices"],
        }
        globalItemDb.append(temp)


with open("GlobalItem.json", "w", encoding="utf-8") as json_file:
    json.dump(globalItemDb, json_file)
categoryDb = []
for gCategory in newData2.keys():
    temp = {
        "category": gCategory,
        "categoryInHindi": translator.translate(str(gCategory), dest="hi").text,
    }
    categoryDb.append(temp)

with open("GlobalCategory.json", "w", encoding="utf-8") as json_file:
    json.dump(categoryDb, json_file)
