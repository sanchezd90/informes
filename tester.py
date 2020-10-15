from datetime import datetime
from flask import Flask

app = Flask(__name__)


class Tiempo():
    def mostrar(self):
        t=datetime.now()
        return t

@app.route("/")
def home():
    tiempo=Tiempo()
    t=tiempo.mostrar()
    return f"""<h1>{t}</h1>"""

app.run(host="localhost", port=8080, debug=True)


            
            
