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
  {"label": "Starter (3)", "value": "starter", "copy": "Three condoms to dial your size—mix or match.", "count": "3"},
  {"label": "Pack of 10", "value": "10", "copy": "Steady stock, discreetly delivered.", "count": "10"},
  {"label": "Pack of 20", "value": "20", "copy": "Keep pace with your rhythm.", "count": "20"},
]

dash_app.layout = html.Div(
  className="page",
  children=[
    html.Header(
      className="shell",
      children=html.Nav(
        className="nav",
        children=[
          html.A([html.Span(className="logo-mark"), "BEAR"], className="logo", href="/"),
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
                html.H1("Choose your batch, type, and cadence."),
                html.P("Minimal, darker browns with discreet delivery.", className="muted"),
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
                                html.Div("BEAR", className="pack-shot"),
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
                        html.Label("Type", className="label"),
                        dcc.RadioItems(
                          id="type",
                          options=[{"label": t, "value": t} for t in ["A", "B", "C"]],
                          inputClassName="choice-input",
                          labelClassName="pill pill-select",
                          inputStyle={"display": "none"},
                        ),
                        html.Label("Size", className="label"),
                        dcc.RadioItems(
                          id="size",
                          options=[{"label": str(num), "value": str(num)} for num in range(1, 6)],
                          inputClassName="choice-input",
                          labelClassName="pill pill-select",
                          inputStyle={"display": "none"},
                        ),
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
                        html.Div([html.P("Type", className="muted"), html.P("—", id="summary-type", className="metric")]),
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
        html.Span([html.Span(className="logo-mark"), "BEAR"], className="logo"),
        html.Div(className="footer-links", children=[html.A("Home", href="/"), html.A("Product", href="/product")]),
        html.P("Quiet confidence, delivered.", className="muted"),
      ],
    ),
  ],
)


@dash_app.callback(
  Output("summary-pack", "children"),
  Output("summary-interval", "children"),
  Output("summary-type", "children"),
  Output("summary-size", "children"),
  Output("summary-email", "children"),
  Output("summary-title", "children"),
  Output("summary-subtitle", "children"),
  Output("confirm", "children"),
  Input("confirm", "n_clicks"),
  Input({"type": "plan-card", "index": dash.ALL}, "n_clicks"),
  State("interval", "value"),
  State("type", "value"),
  State("size", "value"),
  State("email", "value"),
  State("plan", "data"),
  prevent_initial_call=False,
)
def update_summary(n_clicks, plan_clicks, interval, type_value, size_value, email, plan_store):
  ctx = dash.callback_context
  plan_value = None

  if ctx.triggered:
    for trig in ctx.triggered:
      if trig["prop_id"].startswith('{"type":"plan-card"'):
        plan_value = trig["prop_id"].split('"index":"')[1].split('"')[0]

  plan_selected = plan_value or plan_store

  interval_label = interval or "—"
  pack_label = plan_selected or "—"
  type_label = type_value or "—"
  size_label = size_value or "—"
  email_label = email or "—"

  ready = all([plan_selected, interval, type_value, size_value])
  confirmed = ready and n_clicks and n_clicks > 0

  title = "Reserved. You are set." if confirmed else ("Ready to confirm." if ready else "Choose a pack")
  subtitle = f"{pack_label} • {interval_label} • {type_label}{size_label}" if ready else "Pick a batch, interval, and size to see your plan."
  button_text = "Reserved" if confirmed else "Reserve my subscription"

  return pack_label, interval_label, type_label, size_label, email_label, title, subtitle, button_text


@dash_app.callback(
  Output("plan", "data"),
  Output({"type": "plan-card", "index": dash.ALL}, "className"),
  Input({"type": "plan-card", "index": dash.ALL}, "n_clicks"),
  State({"type": "plan-card", "index": dash.ALL}, "id"),
  State("plan", "data"),
)
def select_plan(plan_clicks, ids, current_plan):
  selected = current_plan
  ctx = dash.callback_context
  if ctx.triggered:
    trig = ctx.triggered[0]["prop_id"]
    if trig and trig.startswith('{"type":"plan-card"'):
      selected = trig.split('"index":"')[1].split('"')[0]

  classes = []
  for id_obj in ids:
    base = "plan-card"
    if selected and id_obj.get("index") == selected:
      base += " selected"
    classes.append(base)
  return selected, classes


if __name__ == "__main__":
  import os

  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False)

