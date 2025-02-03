import functions_framework
from markupsafe import escape

@functions_framework.http
def earnings_http(request):
    """Example of an HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_args = request.args
    ticker, year, quarter = request_args["ticker"], request_args["year"], request_args["quarter"]
    paragraphs = '...'
    return f"{paragraphs}"
