from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://elad:wHNNSNp6lK9HOpmyxAz4dk4b3BkdRKP7@dpg-ciajv8d9aq007t9bqt0g-a.oregon-postgres.render.com/test_d1ni"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Store.db"
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String, nullable=False)
    stock = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)

@app.route("/")
@app.route("/product")
@app.route("/product/<id>")
def get_product(id=None):
    if id is None:
        products = Product.query.all()
    else:
        products = [Product.query.get(id)]
    if not products:
        return render_template("index.html"),404
    return_data = []
    for product in products:
        return_data.append(
            {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "price": product.price,
                "stock": product.stock,
                "picture": product.picture
            }
        )
    if id is not None:
        return jsonify(return_data[0])
    return render_template("index.html", products=products)
    
@app.route("/create_product", methods=["POST"])
@app.route("/create_product/<id>", methods=["POST"])
def create_product(id=None):
    data = request.get_json()
    if id is None:
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully"})
    else:
        product = Product.query.get(id)
        if product is None:
            return jsonify({"message": "Product not found"}), 404
        product.name = data["name"]
        product.category = data["category"]
        product.price = data["price"]
        product.picture = data["picture"]
        db.session.commit()
        return jsonify({"message": "Product updated successfully"})


@app.route("/delete_product", methods=["DELETE"])
@app.route("/delete_product/<id>", methods=["DELETE"])
def delete_product(id=None):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Deleted successfully"})
    else:
        return jsonify({"message": f"Error deleting {id}"})


@app.route("/update_product/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404

    data = request.get_json()
    product.name = data["name"]
    product.category = data["category"]
    product.price = data["price"]
    product.stock = data["stock"]
    product.picture = data["picture"]
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/404")
def notFound_404():
    return render_template("404.html")

@app.route("/about")
def about():
    return render_template("about.html")

with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(port=9000, debug=True)
