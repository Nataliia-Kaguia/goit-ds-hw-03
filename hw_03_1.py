import pymongo
from pymongo.errors import ConnectionFailure, OperationFailure
from bson.objectid import ObjectId

# Підключення до MongoDB
try:
    client = pymongo.MongoClient("mongodb+srv://moonkaguia:<db_password>@nataliia-kaguia.qzoizac.mongodb.net/")
    db = client["cat_database"]
    cats_collection = db["cats"]
    print("✅ Connected to MongoDB.")
except ConnectionFailure as e:
    print(f"❌ Connection failed: {e}")
    exit()

# CREATE
def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    try:
        result = cats_collection.insert_one(cat)
        print(f"✅ Cat added with id: {result.inserted_id}")
    except OperationFailure as e:
        print(f"❌ Failed to insert: {e}")

# READ
def read_all_cats():
    for cat in cats_collection.find():
        print(cat)

def read_cat_by_name(name):
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print("😿 Cat not found.")

# UPDATE
def update_cat_age(name, new_age):
    result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count:
        print("✅ Cat age updated.")
    else:
        print("😿 No such cat found or age was the same.")

def add_feature_to_cat(name, feature):
    result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.modified_count:
        print("✅ Feature added.")
    else:
        print("😿 No such cat found.")

# DELETE
def delete_cat_by_name(name):
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count:
        print("✅ Cat deleted.")
    else:
        print("😿 No such cat found.")

def delete_all_cats():
    confirm = input("⚠️ Are you sure you want to delete ALL cats? (yes/no): ")
    if confirm.lower() == "yes":
        result = cats_collection.delete_many({})
        print(f"🗑️ Deleted {result.deleted_count} cats.")
    else:
        print("❌ Deletion cancelled.")

# Демонстрація
if __name__ == "__main__":
    while True:
        print("\n--- CAT DATABASE ---")
        print("1. Create cat")
        print("2. Show all cats")
        print("3. Find cat by name")
        print("4. Update cat age")
        print("5. Add feature to cat")
        print("6. Delete cat by name")
        print("7. Delete ALL cats")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            age = int(input("Age: "))
            features = input("Features (comma separated): ").split(",")
            create_cat(name, age, [f.strip() for f in features])
        elif choice == "2":
            read_all_cats()
        elif choice == "3":
            name = input("Enter cat name: ")
            read_cat_by_name(name)
        elif choice == "4":
            name = input("Enter cat name: ")
            new_age = int(input("New age: "))
            update_cat_age(name, new_age)
        elif choice == "5":
            name = input("Enter cat name: ")
            feature = input("New feature: ")
            add_feature_to_cat(name, feature)
        elif choice == "6":
            name = input("Enter cat name to delete: ")
            delete_cat_by_name(name)
        elif choice == "7":
            delete_all_cats()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice.")
