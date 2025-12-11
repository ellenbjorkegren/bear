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


dash_app: Dash = dash.Dash(
  __name__,
  server=app,
  url_base_pathname="/shop/",
  external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap", "/static/styles.css"],
)

dash_app.layout = html.Div(
  className="page",
  children=[
    html.Header(
      className="shell",
      children=html.Nav(
        className="nav",
        children=[
          html.A("BEAR", className="logo", href="/"),
          html.Div(className="nav-actions", children=[html.A("Home", className="nav-link", href="/")]),
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
                html.H1("Choose your batch, set your rhythm."),
                html.P("Custom sizing, premium quality. Select a pack and delivery interval that keeps you ready—without excess.", className="muted"),
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
                        html.Label(
                          className="label",
                          children=[
                            "Size",
                            dcc.Dropdown(
                              id="size",
                              options=[
                                {"label": "Tailored S", "value": "Tailored S"},
                                {"label": "Tailored M", "value": "Tailored M"},
                                {"label": "Tailored L", "value": "Tailored L"},
                                {"label": "Tailored XL", "value": "Tailored XL"},
                              ],
                              placeholder="Select your fit",
                              className="dropdown",
                              clearable=False,
                            ),
                          ],
                        ),
                        html.Label(
                          className="label",
                          children=[
                            "Batch size",
                            dcc.RadioItems(
                              id="pack",
                              options=[{"label": f"{count}", "value": str(count)} for count in [3, 10, 20, 30]],
                              className="pill-radio",
                              inputClassName="pill-radio-input",
                              labelClassName="pill pill-select pill-radio-label",
                              inputStyle={"display": "none"},
                            ),
                          ],
                        ),
                        html.Fieldset(
                          className="fieldset",
                          children=[
                            html.Legend("Delivery interval"),
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
                          ],
                        ),
                        html.Label(
                          className="label",
                          children=[
                            "Email",
                            dcc.Input(id="email", type="email", placeholder="you@bear.com", className="email-input"),
                          ],
                        ),
                        dcc.Store(id="confirmed", data=False),
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
                    html.P("Pick your batch size, interval, and fit to see your plan.", id="summary-subtitle", className="muted"),
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
        html.Div(className="footer-links", children=[html.A("Home", href="/"), html.A("How it works", href="/#how")]),
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
  State("pack", "value"),
  State("interval", "value"),
  State("size", "value"),
  State("email", "value"),
)
def update_summary(n_clicks: int, pack: str, interval: str, size: str, email: str):
  pack_label = f"{pack} pack" if pack else "—"
  interval_label = interval or "—"
  size_label = size or "—"
  email_label = email or "—"

  ready = all([pack, interval, size])
  confirmed = ready and n_clicks and n_clicks > 0

  title = "Reserved. You are set." if confirmed else ("Ready to confirm." if ready else "Choose a pack")
  subtitle = f"{pack_label} • {interval_label} • {size_label}" if ready else "Pick your batch size, interval, and fit to see your plan."
  button_text = "Reserved" if confirmed else "Reserve my subscription"

  return pack_label, interval_label, size_label, email_label, title, subtitle, button_text


if __name__ == "__main__":
  import os

  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False)

