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

### The site must answer on exactly one origin

`NEXT_PUBLIC_SITE_URL` is the single source of the `redirect_uri`, while the flow
cookie written by `/api/auth/oauth/{provider}/start` is host-only: it carries no
`Domain` attribute. If the site also answers on a second host, a sign-in started
on the non-canonical host leaves its cookie there, the provider returns the
browser to the canonical host, and the callback finds no cookie. Every attempt
then fails with `oauth_state_invalid`, and retrying never helps.

Registering both hosts in the provider console does not fix this, because the API
only ever generates one `redirect_uri`. Every host that answers must redirect to
the canonical one. `www.mokaair.com` already does, path-preserving, at the edge
proxy; keep it that way and re-check after any proxy change.

Check an OAuth path rather than `/`: a redirect that covers only the site root
would still break sign-in, and testing `/` alone cannot tell the two apart.

```bash
curl -sSI https://www.mokaair.com/api/auth/oauth/google/start | grep -iE '^HTTP|^location'
# expect: HTTP/1.1 301 ...
#         location: https://mokaair.com/api/auth/oauth/google/start
```

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

Apple verifies the web domain before it accepts the return URL. It issues an
`apple-developer-domain-association.txt` that must answer at
`https://mokaair.com/.well-known/apple-developer-domain-association.txt`. Commit
it to `apps/web/public/.well-known/`; the file is meant to be served publicly and
is not a secret. The proxy matcher in `apps/web/proxy.ts` excludes paths that
contain a dot, so the file is served as a static asset without a locale prefix.
Check that it is actually reachable before returning to Apple to press Verify:

```bash
curl -s https://mokaair.com/.well-known/apple-developer-domain-association.txt
```

If a future Next.js version stops serving dot-directories out of `public/`, serve
that single path from the edge proxy instead.

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

Test connection reaches only the provider's public OpenID metadata for Google and
LINE, so it passes even with a wrong client identifier or secret. For Apple it
additionally signs a real ES256 client secret, so it does catch a malformed
`.p8`. A completed interactive sign-in is the only proof that credentials work.

A saved provider row that is switched off nulls its secret fields at runtime,
including a value set in the environment, so an unused disabled row makes
environment credentials look broken. The stored ciphertext is kept and returns
when the row is enabled again.

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
