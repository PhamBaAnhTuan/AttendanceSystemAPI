import logging
from oauth2_provider.contrib.rest_framework.permissions import TokenMatchesOASRequirements

log = logging.getLogger("oauth2_provider")

class TokenHasActionScope(TokenMatchesOASRequirements):

    def has_permission(self, request, view):
        token  = request.auth

        if not token:
            return False
        
        if hasattr(token, "scope"):
            required_alternate_scopes = self.get_required_alternate_scopes(request, view)
            # print(f"Scope: {required_alternate_scopes}")

            m = view.action.lower()
            if m in required_alternate_scopes:
                log.debug(
                    "Required scopes alternatives to access resource: {0}".format(
                        required_alternate_scopes[m]
                    )
                )
                for alt in required_alternate_scopes[m]:
                    if token.is_valid(alt):
                        return True
                return False
            else:
                log.warning("no scope alternates defined for method {0}".format(m))
                return False
            
        assert False, (
            "TokenHasActionScope requires the"
            "`oauth.rest_framework.OAuth2Authentication` authentication "
            "class to be used."
        )