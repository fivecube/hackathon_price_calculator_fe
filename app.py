import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from client import get_countries_api_response, send_to_niranjan

category_sub_category_data = []
group_colors = {"control": "light blue", "reference": "red"}

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
ALLOWED_TYPES = ["Small", "Standard", "Large", "X-Large", "Bulky"]

payload_for_pricing = {
    "country_id": 1,
    "num_order_items": 0,
    "size_distribution": {
    }
}
edited = False
total_orders = 0


# App Layout
app.layout = html.Div(
    children=[
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title", children="Pricing Calculator"),
                html.Div(
                    className="div-logo",
                    children=html.Img(
                        className="logo", src=dash.get_asset_url("logo.png")
                    ),
                ),
                html.H2(className="h2-title-mobile", children="Locad Pricing Estimator"),
            ],
        ),
        # Body of the App
        html.Div(
            className="row app-body",
            children=[
                # User Controls
                html.Div(
                    className="four columns card",
                    children=[
                        html.Div(
                            className="bg-white user-control",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        dcc.Dropdown(id="country", placeholder="Choose Country"),
                                    ],
                                ),
                                html.H6("Choose Number of Orders for each size per month"),
                                html.Div(
                                    [dcc.Input(id="input_{}".format(_), placeholder=_, type="number")
                                        for _ in ALLOWED_TYPES]
                                ),
                                html.Div(id="orders_per_month", className="padding-top-bot"),
                                html.H6(),
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6(""),
                                        dcc.Link(html.Button('Calculate', id='calculate'), href="/showcase"),
                                    ],
                                ),
                                html.Div(id="total_cost_id", className="padding-top-bot")
                            ],
                        )
                    ],
                ),
                # Blog Image
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            className="bg-white",
                            children=[
                                html.H5("All you need to know about tiktok shop for your E-commerce Business"),
                                html.Img(className="blog", src=dash.get_asset_url("blog.webp")),
                            ],
                        )
                    ],
                ),
                dcc.Store(id="error", storage_type="memory"),
            ],
        ),
    ]
)

@app.callback(
    Output("orders_per_month", "children"),
    [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
)
def cb_render(*vals):
    global payload_for_pricing
    global total_orders
    return_thing = []
    for size_type, number_of_orders in zip(ALLOWED_TYPES, vals):
        return_thing.append(f"{size_type}={number_of_orders}")
        if number_of_orders:
            total_orders += number_of_orders
            payload_for_pricing["size_distribution"][size_type] = int(number_of_orders)
    total_orders = sum(payload_for_pricing["size_distribution"].values())
    payload_for_pricing["num_order_items"] = total_orders
    return f"Total Number of Orders per month = {total_orders}"


@app.callback(
    [Output("country", "options"),
     Output("country", "value"),],
    [Input("country", "value")],
)
def countries(value):
    global edited
    global payload_for_pricing
    options = []
    country_data = get_countries_api_response()
    for country in country_data:
        options.append(
            {"label": f"{country.get('country_name')}", "value": country.get('id')}
        )
    options.sort(key=lambda item: item["label"])
    if value:
        payload_for_pricing["country_id"] = value
        edited = True
    return options, value



@app.callback(Output("total_cost_id", "children"),
          [Input("calculate", "n_clicks")])
def calculate_button(n_clicks):
    return_thing = ''
    response = send_to_niranjan(payload_for_pricing, edited=edited)
    print(response)
    if response:
        total_bill = response.get("total_bill")
        if total_bill:
            return_thing = "Total Cost = {}".format(total_bill)
    return return_thing


if __name__ == "__main__":
    app.run_server(debug=True)