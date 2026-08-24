import json
import os
from google.cloud import secretmanager
from yahoo_oauth import OAuth2
from src.config import settings


def get_authenticated_session() -> OAuth2:
    """Retrieves an authenticated OAuth2 session, persisting tokens via Secret Manager in GCP

    or local oauth2.json during local development.
    """
    # 1. Local development fallback
    if os.path.exists("oauth2.json"):
        sc = OAuth2(None, None, from_file="oauth2.json")
        if not sc.token_is_valid():
            sc.refresh_access_token()
        return sc

    # 2. Cloud Run / Secret Manager flow
    if settings.gcp_project_id:
        client = secretmanager.SecretManagerServiceClient()
        secret_path = (
            f"projects/{settings.gcp_project_id}/secrets/{settings.yahoo_secret_name}/versions/latest"
        )
        response = client.access_secret_version(request={"name": secret_path})
        token_data = json.loads(response.payload.data.decode("UTF-8"))

        # Write temporarily to memory/disk for yahoo_oauth consumption
        with open("/tmp/oauth2.json", "w") as f:
            json.dump(token_data, f)

        sc = OAuth2(None, None, from_file="/tmp/oauth2.json")

        if not sc.token_is_valid():
            sc.refresh_access_token()
            # Persist the refreshed token back to Secret Manager
            with open("/tmp/oauth2.json", "r") as f:
                updated_token_data = f.read()

            parent = f"projects/{settings.gcp_project_id}/secrets/{settings.yahoo_secret_name}"
            client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": {"data": updated_token_data.encode("UTF-8")},
                }
            )

        return sc

    raise RuntimeError(
        "No valid authentication source found. Provide oauth2.json or set GCP_PROJECT_ID."
    )
