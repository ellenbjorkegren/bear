from flask import Flask, redirect, render_template, url_for
import dash
from dash import Dash, Input, Output, State, dcc, html


app = Flask(__name__)


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/shop")
def shop_redirect():
  # Redirect to the Dash-powered shop experience
  return redirect("/shop/")

@app.route("/product")
def product():
  return render_template("product.html")

dash_app: Dash = dash.Dash(
  __name__,
  server=app,
  url_base_pathname="/shop/",
  external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap", "/static/styles.css"],
)

plans = [
  {"label": "Start (3)", "value": "3", "copy": "Light, discreet top-up.", "image": "https://images.unsplash.com/photo-1506617420156-8e4536971650?auto=format&fit=crop&w=600&q=80"},
  {"label": "10 Pack", "value": "10", "copy": "Stay stocked without excess.", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80"},
  {"label": "20 Pack", "value": "20", "copy": "Your steady monthly cadence.", "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=600&q=80"},
  {"label": "30 Pack", "value": "30", "copy": "For frequent use, set-and-forget.", "image": "https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=600&q=80"},
]

size_options = [f"{letter}{num}" for letter in ["A", "B", "C"] for num in range(1, 6)]

dash_app.layout = html.Div(
  className="page",
  children=[
    html.Header(
      className="shell",
      children=html.Nav(
        className="nav",
        children=[
          html.A("BEAR", className="logo", href="/"),
          html.Div(className="nav-actions", children=[
            html.A("Home", className="nav-link", href="/"),
            html.A("Product", className="nav-link", href="/product"),
          ]),
        ],
      ),
    ),
    html.Main(
      children=[
        html.Section(
          className="section shell",
          children=[
            html.Div(
              className="section-head",
              children=[
                html.P("Subscriptions", className="eyebrow"),
                html.H1("Choose your batch, shade, and rhythm."),
                html.P("Deep brown aesthetic, quality latex, discreet delivery.", className="muted"),
              ],
            ),
            html.Div(
              className="grid two stack-gap",
              children=[
                html.Div(
                  className="card form-card",
                  children=[
                    html.Div(
                      className="form",
                      children=[
                        html.Label("Select your pack", className="label"),
                        html.Div(
                          className="plan-grid",
                          children=[
                            html.Div(
                              className="plan-card",
                              id={"type": "plan-card", "index": plan["value"]},
                              children=[
                                html.Img(src=plan["image"], alt=plan["label"]),
                                html.P(plan["label"], className="plan-title"),
                                html.P(plan["copy"], className="muted"),
                              ],
                            )
                            for plan in plans
                          ],
                        ),
                        dcc.Store(id="plan"),
                        html.Label("Delivery interval", className="label"),
                        dcc.RadioItems(
                          id="interval",
                          options=[
                            {"label": "Every month", "value": "Every month"},
                            {"label": "Every other month", "value": "Every other month"},
                            {"label": "Every 3 months", "value": "Every 3 months"},
                          ],
                          inputClassName="choice-input",
                          labelClassName="choice",
                        ),
                        html.Label("Shade + size", className="label"),
                        html.Div(
                          className="size-grid",
                          children=[
                            html.Div(option, className="size-chip", id={"type": "size-chip", "index": option}) for option in size_options
                          ],
                        ),
                        dcc.Store(id="size"),
                        html.Label("Email", className="label"),
                        dcc.Input(id="email", type="email", placeholder="you@bear.com", className="email-input"),
                        html.Button("Reserve my subscription", id="confirm", className="button primary block", n_clicks=0),
                        html.P("No charge yet—we’ll confirm your fit and schedule.", className="form-note muted"),
                      ],
                    ),
                  ],
                ),
                html.Div(
                  className="card summary-card",
                  children=[
                    html.P("Your selection", className="card-label"),
                    html.H3("Choose a pack", id="summary-title"),
                    html.P("Pick a batch, interval, and size to see your plan.", id="summary-subtitle", className="muted"),
                    html.Div(
                      className="summary-grid",
                      children=[
                        html.Div([html.P("Batch", className="muted"), html.P("—", id="summary-pack", className="metric")]),
                        html.Div([html.P("Interval", className="muted"), html.P("—", id="summary-interval", className="metric")]),
                        html.Div([html.P("Size", className="muted"), html.P("—", id="summary-size", className="metric")]),
                        html.Div([html.P("Email", className="muted"), html.P("—", id="summary-email", className="metric")]),
                      ],
                    ),
                    html.Div(className="pill-row muted-row", children=[html.Span("Premium latex", className="pill"), html.Span("Discreet delivery", className="pill"), html.Span("Flexible pauses", className="pill")]),
                    html.A("Back to home", className="button ghost block", href="/"),
                  ],
                ),
              ],
            ),
          ],
        )
      ]
    ),
    html.Footer(
      className="shell footer",
      children=[
        html.Span("BEAR", className="logo"),
        html.Div(className="footer-links", children=[html.A("Home", href="/"), html.A("Product", href="/product")]),
        html.P("Quiet confidence, delivered.", className="muted"),
      ],
    ),
  ],
)


@dash_app.callback(
  Output("summary-pack", "children"),
  Output("summary-interval", "children"),
  Output("summary-size", "children"),
  Output("summary-email", "children"),
  Output("summary-title", "children"),
  Output("summary-subtitle", "children"),
  Output("confirm", "children"),
  Input("confirm", "n_clicks"),
  Input({"type": "plan-card", "index": dash.ALL}, "n_clicks"),
  Input({"type": "size-chip", "index": dash.ALL}, "n_clicks"),
  State("interval", "value"),
  State("email", "value"),
  State("plan", "data"),
  State("size", "data"),
  prevent_initial_call=False,
)
def update_summary(n_clicks, plan_clicks, size_clicks, interval, email, plan_store, size_store):
  ctx = dash.callback_context
  plan_value = None
  size_value = None

  if ctx.triggered:
    for trig in ctx.triggered:
      if trig["prop_id"].startswith('{"type":"plan-card"'):
        plan_value = trig["prop_id"].split('"index":"')[1].split('"')[0]
      if trig["prop_id"].startswith('{"type":"size-chip"'):
        size_value = trig["prop_id"].split('"index":"')[1].split('"')[0]

  plan_selected = plan_value or plan_store
  size_selected = size_value or size_store

  interval_label = interval or "—"
  pack_label = f"{plan_selected} pack" if plan_selected else "—"
  size_label = size_selected or "—"
  email_label = email or "—"

  ready = all([plan_selected, interval, size_selected])
  confirmed = ready and n_clicks and n_clicks > 0

  title = "Reserved. You are set." if confirmed else ("Ready to confirm." if ready else "Choose a pack")
  subtitle = f"{pack_label} • {interval_label} • {size_label}" if ready else "Pick a batch, interval, and size to see your plan."
  button_text = "Reserved" if confirmed else "Reserve my subscription"

  return pack_label, interval_label, size_label, email_label, title, subtitle, button_text


if __name__ == "__main__":
  import os

  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False)

