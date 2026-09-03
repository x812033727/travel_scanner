# Google, LINE, and Apple login

Mokaair supports password login and optional Google, LINE, and Apple OpenID
Connect login. Provider credentials stay behind the FastAPI service and are
stored with the existing encrypted provider-settings mechanism. The browser BFF
receives the provider callback and only stores the resulting Mokaair access
token in the existing HTTP-only cookie.

## Account rules

- Provider identity is keyed by the provider's stable subject identifier, never
  by a display name.
- An existing email is never merged automatically. The member signs in with an
  existing method and links the provider from Account.
- A first-time provider registration requires a provider-verified email. This
  means LINE's Email permission must be approved before LINE can create a new
  Mokaair account.
- A member may link more than one identity from the same provider, but cannot
  remove the final working login method.
- Only Apple refresh tokens are retained, encrypted, so Apple authorization can
  be revoked when an identity is disconnected. Google and LINE access tokens are
  not retained.

## Callback URLs

The callback origin comes from `NEXT_PUBLIC_SITE_URL`; provider-console values
must match it exactly. Production uses:

```text
https://mokaair.com/api/auth/oauth/google/callback
https://mokaair.com/api/auth/oauth/line/callback
https://mokaair.com/api/auth/oauth/apple/callback
```

For local Google and LINE testing, add the matching
`http://localhost:3000/api/auth/oauth/{provider}/callback` URL. Sign in with
Apple for web requires an HTTPS return URL, so use a controlled HTTPS development
domain when testing Apple.

## Provider console setup

### Google

Create an OAuth web client, configure the consent screen, and add the exact
authorized redirect URI. Mokaair requests only `openid email`, validates the ID
token issuer, audience, signature, expiry, nonce, and verified-email claim, and
uses PKCE. Google requires an exact redirect URI match.

### LINE

Create a LINE Login channel whose app type includes Web app, add the exact
callback URL, and apply for OpenID Connect Email address permission. Mokaair uses
LINE Login v2.1 with `openid email`, PKCE S256, state, nonce, and the official ID
token verification endpoint. Without Email permission, an already-linked LINE
identity can still be recognized, but it cannot create a first-time account.

### Apple

Create a Services ID, associate the web domain and return URL, and create a Sign
in with Apple key. Enter the Services ID, Team ID, Key ID, and complete `.p8`
private key in the admin page. The private key accepts normal PEM line breaks or
escaped `\n`. Apple returns the authorization response with `form_post`; the
production callback cookie is therefore `SameSite=None; Secure`. Mokaair creates
a short-lived ES256 client secret, validates Apple's ID token, and uses Apple's
token revocation endpoint when disconnecting.

## Mokaair configuration

Open `/{locale}/admin/settings`, select each login provider, enter its public
identifier and secret, enable it, save, then run Test connection. The public
login and registration screens only render providers that report fully
configured. Environment variables remain a fallback:

```text
AUTH_GOOGLE_ENABLED
AUTH_GOOGLE_CLIENT_ID
AUTH_GOOGLE_CLIENT_SECRET
AUTH_LINE_ENABLED
AUTH_LINE_CHANNEL_ID
AUTH_LINE_CHANNEL_SECRET
AUTH_APPLE_ENABLED
AUTH_APPLE_SERVICES_ID
AUTH_APPLE_TEAM_ID
AUTH_APPLE_KEY_ID
AUTH_APPLE_PRIVATE_KEY
AUTH_OAUTH_FLOW_TTL_SECONDS
AUTH_OAUTH_IP_LIMIT
```

Keep `SETTINGS_ENCRYPTION_KEY` stable. Rotate a provider secret by saving its new
value and testing the connection before removing the old credential in the
provider console.

## Security notes

OAuth flows expire after ten minutes by default, are single-use in Redis, and
bind state, nonce, provider, intent, user session, and a browser-only random
value. Google and LINE use PKCE. Callback destinations accept only local paths.
Errors shown to the browser use a fixed allowlist and do not expose provider
responses or credentials.

Provider references:

- [Google OAuth web-server flow](https://developers.google.com/identity/protocols/oauth2/web-server)
- [LINE Login web integration](https://developers.line.biz/en/docs/line-login/integrate-line-login/)
- [Apple web configuration](https://developer.apple.com/documentation/signinwithapple/configuring-your-webpage-for-sign-in-with-apple)
- [Apple token revocation](https://developer.apple.com/documentation/signinwithapplerestapi/revoke-tokens)
