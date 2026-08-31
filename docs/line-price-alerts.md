# LINE price alerts

Travel Scanner can link one website account to one LINE user through the official LINE Messaging API account-link flow. Users add the official account, send `綁定`, open the one-time link, sign in, and confirm the connection. The website never asks users to type or expose their LINE user ID.

## LINE Console setup

Create a Messaging API channel for the official account and configure its webhook URL as:

```text
https://YOUR_SITE/api/line/webhook
```

Enable webhooks, disable the default greeting if it conflicts with the binding prompt, and set:

```dotenv
LINE_MESSAGING_ENABLED=true
LINE_CHANNEL_SECRET=...
LINE_CHANNEL_ACCESS_TOKEN=...
LINE_OFFICIAL_ACCOUNT_ID=@your-account
LINE_ADD_FRIEND_URL=https://line.me/R/ti/p/@your-account
```

The public webhook proxy preserves the exact request body and `X-Line-Signature`; the API verifies HMAC-SHA256 before parsing JSON. Link nonces expire after ten minutes and are single-use. LINE user IDs are only returned to the website in masked form.

## Price checks and delivery

Run both dedicated processes in addition to the regular search worker:

```text
python -m app.alerts.scheduler
python -m app.alerts.worker
```

The scheduler checks eligible flight and hotel providers every six hours by default. Provider sources that do not permit background repricing remain `manual_only` and are labelled that way in the UI. Background checks do not consume member search uses.

An alert with a target sends once when the price crosses at or below the target, then rearms only after the price rises above it. An alert without a target sends only when a new low is observed. Delivery jobs use unique dedupe keys and retry transient LINE failures with bounded exponential backoff.
