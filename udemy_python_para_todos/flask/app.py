from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    return Response("Olá Mundo")


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)
