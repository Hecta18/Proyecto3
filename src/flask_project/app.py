from flask import Flask, render_template, request, redirect, url_for, session
from lista_restaurantes import todos_restaurantes

#Anotaciones:
# Implementar home especifico para el usuario

app = Flask(__name__)

app.secret_key = "clave_secreta"
# Configuración de la clave secreta para la sesión

@app.route("/") # Ruta para la página de inicio
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
# Ruta para la pagina principal del usuario
def home():
    tipo = request.form.get("tipo_comida")
    buscar = request.form.get("busqueda")
    # Obtener los parámetros 

    restaurantes_filtrados = todos_restaurantes

    if tipo and tipo != "Todos":
        restaurantes_filtrados = [r for r in restaurantes_filtrados if r.get("tipo") == tipo]
    # Filtrar por tipo de comida 

    if buscar:
        buscar_lower = buscar.lower()
        restaurantes_filtrados = [r for r in restaurantes_filtrados if buscar_lower in r["nombre"].lower()]
    # Filtrar por texto de búsqueda

    return render_template("home.html", restaurantes=restaurantes_filtrados, tipo_seleccionado=tipo or "Todos", texto_busqueda=buscar or "")

@app.route("/restaurante/<nombre>")
def restaurante(nombre):
    restaurante = next((r for r in todos_restaurantes if r["nombre"] == nombre), None)
    # Buscar el restaurante por nombre
    if not restaurante:
        return "Restaurante no encontrado", 404
    return render_template("restaurante.html", restaurante=restaurante)

@app.route("/agregar_pedido", methods=["POST"])
def agregar_pedido():
    plato = request.form["plato"]
    precio = float(request.form["precio"])

    if "carrito" not in session:
        session["carrito"] = []
    # Inicializar el carrito si no existe

    session["carrito"].append({"plato": plato, "precio": precio})
    session.modified = True

    return redirect(url_for("pedido"))

@app.route("/pedido")
def pedido():
    carrito = session.get("carrito", [])
    total = sum(item["precio"] for item in carrito)
    return render_template("pedido.html", carrito=carrito, total=total)

@app.route("/eliminar_pedido/<int:index>", methods=["POST"])
def eliminar_pedido(index):
    if "carrito" in session and 0 <= index < len(session["carrito"]):
        del session["carrito"][index]
        session.modified = True
    # Eliminar un plato del carrito por índice
    return redirect(url_for("pedido"))

@app.route("/crear_cuenta", methods=["GET", "POST"])
def crear_cuenta():
    error = ""
    if request.method == "POST":
        correo = request.form["correo"]
        nombre = request.form["nombre"]
        password = request.form["password"]
        confirmar = request.form["confirmar"]

        if password != confirmar:
            error = "La contraseña no coincide"
        else:
            return redirect(url_for("home"))

    return render_template("crear_cuenta.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form["correo"] and request.form["password"] != None:
            return redirect(url_for("home"))
        error = "Por favor, ingresa tus credenciales"
    return render_template("login.html", error=error)

@app.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("cuenta.html")

if __name__ == "__main__":
    app.run(debug=True)