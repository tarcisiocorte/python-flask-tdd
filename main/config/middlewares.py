from flask import Flask


def setup_middlewares(app: Flask) -> None:
    @app.before_request
    def before_request():
        pass

    @app.after_request
    def after_request(response):
        if response.get_json() is not None:
            response.headers['Content-Type'] = 'application/json'
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,x-access-token"
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
