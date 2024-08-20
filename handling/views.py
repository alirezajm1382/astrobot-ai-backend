# Importing the necessary libraries for the views
from django.http import HttpResponse
from django.shortcuts import render

# Importing the necessary libraries for authentication
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode


# Initializing the OAuth object
oauth = OAuth()

# Registering the Auth0 application
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

# Index view just returning the method of the api
# For testing purposes
def index(request):
    if request.method == 'GET':
        if request.session.get('user'):
            return HttpResponse(request.session.get('user')['userinfo']['email'])
        else:
            return HttpResponse("No user found")
    elif request.method == 'POST':
        return HttpResponse("Posting data?!")

# Login view redirecting to the Auth0 authorization page
def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

# Logout view redirecting to the Auth0 logout page
def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )

# Callback view handling the Auth0 callback
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))
