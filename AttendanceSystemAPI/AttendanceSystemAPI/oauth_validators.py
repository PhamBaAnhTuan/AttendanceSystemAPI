from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    def get_additional_claims(self, request):
        user = request.user
        if user and user.role:
            return {"scope": user.role.scope}
        return {}