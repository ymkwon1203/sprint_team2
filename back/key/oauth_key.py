from oauthlib.oauth2 import WebApplicationClient
import os
import requests

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "925008810945-2lkbaaqo92r5hlo2rs4q5cvd0e7vv9eq.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "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")
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
google_client = WebApplicationClient(GOOGLE_CLIENT_ID)

KAKAO_CLIENT_ID ="8f7cdba02b010160f11d763961649db3"
KAKAO_CLIENT_SECRET ="6SEoxBl2SkFhQh52Tn1H5oyWaLJBCzPT"
KAKAO_REDIRECT_URI = "https://localhost:5000/api/login/kakao/callback"
KAKAO_SIGNOUT_REDIRECT_URI ="http://localhost:5000/api/login/kakao/logout"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
