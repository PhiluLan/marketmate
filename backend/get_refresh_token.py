#!/usr/bin/env python3
"""
Kurzes Script, um per OAuth2 einen Refresh-Token
für die Google Ads API zu generieren.
"""

from google_auth_oauthlib.flow import InstalledAppFlow

# 1) Trage hier deine OAuth2-Client-ID und dein Secret ein:
CLIENT_ID = "637213930037-v68db61mt97o9q8at0dkg0hd2321kj9n.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# 2) Definiere die OAuth-Konfiguration
client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        # urn:ietf:wg:oauth:2.0:oob sorgt dafür, dass du den Code direkt im Terminal eingibst
        "redirect_uris": ["http://localhost:8080/"],
    }
}

def main():
    # 3) Starte den lokalen OAuth-Flow im Konsolenmodus
    flow = InstalledAppFlow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/adwords"],
    )
    creds = flow.run_local_server(port=8080)
    print("\n=== Fertig! Dein Refresh-Token lautet: ===")
    print(creds.refresh_token)
    print("==========================================")

if __name__ == "__main__":
    main()
