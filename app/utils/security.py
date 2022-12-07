from fastapi.param_functions import Form


class OAuth2RefreshRequestForm:
    def __init__(
        self,
        grant_type: str = Form(None, regex="refresh_token"),
        refresh_token: str = Form(...),
    ):
        self.grant_type = grant_type
        self.refresh_token = refresh_token
