# Skyscanner partnership application

Travel Scanner should request access to Flights Live Prices and Flights Indicative Prices only
after a public HTTPS preview is available. Do not include API keys, test credentials, personal
data, or provider responses in the application materials.

## Product description

Travel Scanner is a Traditional Chinese travel comparison product for Taiwan. A user supplies
their route, exact dates, travellers, cabin and preferences. The product displays normalized
flight choices alongside lodging and trip costs, then sends the user to the airline or OTA to
complete the booking. Travel Scanner does not issue tickets, take payment, manage PNRs or provide
post-booking servicing.

Flexible-date discovery uses indicative prices. A Live Prices search is created only after a user
chooses exact dates and explicitly starts a search. Results include a visible booking action for
each eligible offer. The booking link is requested or followed only after that user action.

## Application checklist

- Public HTTPS URL with registration, search, result and pricing pages.
- Screenshots for one-way, return and multi-city searches in desktop and mobile layouts.
- A result card showing carrier, operating carrier, agent, total price, baggage, freshness and a
  visible `前往訂票` action.
- `Powered by Skyscanner` attribution linked to `https://www.skyscanner.net`.
- An explanation of the create/poll flow and short-lived offer handling.
- Confirmation that API calls originate from the backend and the API key never reaches browsers.
- Confirmation that scheduled alerts and AI exploration do not call Live Prices.
- Expected monthly active users, searches, clickouts and target markets.
- Primary market `TW`, locale `zh-TW`, currency `TWD`.

Apply through the official partnership form linked from
<https://developers.skyscanner.net/docs/getting-started/authentication>.

## Approval smoke test

Use a non-production key and test TPE routes to Tokyo, Osaka, Seoul and Bangkok. Verify that
create returns an initial batch, poll reaches `RESULT_STATUS_COMPLETE`, every displayed itinerary
can be refreshed, and every booking action resolves to an HTTPS airline or OTA URL. Record actual
carriers returned by the account; never advertise a carrier based only on public marketing pages.
