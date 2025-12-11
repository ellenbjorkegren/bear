from flask import Flask, render_template

app = Flask(__name__)

PLANS = [
  {"id": "starter", "label": "Starter (3)", "desc": "Three condoms to dial your fit—mix or match sizes."},
  {"id": "10", "label": "Pack of 10", "desc": "Steady stock, discreetly delivered."},
  {"id": "20", "label": "Pack of 20", "desc": "Keep pace with your rhythm."},
]

TYPES = ["bubble", "tight", "slim"]
SIZES = [f"{letter}{num}" for letter in ["A", "B", "C"] for num in range(1, 5)]
INTERVALS = ["Every month", "Every other month", "Every 3 months"]


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/shop")
def shop():
  return render_template("shop.html", plans=PLANS)


@app.route("/product")
def product():
  return render_template("product.html")


@app.route("/subscribe/<plan_id>")
def subscribe(plan_id: str):
  plan = next((p for p in PLANS if p["id"] == plan_id), None)
  if not plan:
    plan = PLANS[0]
  return render_template("subscribe.html", plan=plan, types=TYPES, sizes=SIZES, intervals=INTERVALS)


if __name__ == "__main__":
  import os

  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False)

