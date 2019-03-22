print("This is a tool to generate sample routes data.")
print("How long do a trip do you want to take?")
length = int(input("> "))

print("How many subroutes do you want? (n >= 1)")
subroutes = int(input("> "))
subroutes_length = int(length/subroutes + 0.5)
route = ""


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


lst = chunks(range(length), subroutes_length)

for i in lst:
    for j in i:
        if j == i[-1]:
            next = i[0]
        else:
            next = j + 1
        route += "({cur},{next}) ".format(cur=j, next=next)

print(route)

routes_file = open('route.txt', 'w')
routes_file.write(route)
routes_file.close()
