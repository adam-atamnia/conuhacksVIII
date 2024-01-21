from api import create_app
from firebase_functions import https_fn

app = create_app()

if __name__ == '__main__':
  app.run(debug = True)


@https_fn.on_request()
def httpsflask(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()

#https://stackoverflow.com/questions/76450609/firebase-functions-gen2-python-init-does-not-work
#https://stackoverflow.com/questions/47511677/firebase-cloud-function-your-client-does-not-have-permission-to-get-url-200-fr