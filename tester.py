import json
from usuarios import users

with open("usuarios.json","w") as f:
    json.dump(users,f,indent=4)