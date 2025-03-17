from core.users.users import UsersDB

u_db = UsersDB()

print(u_db.all())

while True:
    query = input("Query: ")
    cond = input("Condition: ")
    value = int(input("Value: "))

    for u in u_db.search_by_tags(query, condition=f"{cond}:{value}"):
        print(u)
