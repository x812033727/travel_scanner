# Mokaair contact channels

Two owner-confirmed mailboxes. They are not interchangeable: one is read by a person
and published, the other only sends and is never offered as a reply address.

| Address | Direction | Used for |
| --- | --- | --- |
| `support@mokaair.com` | receives and replies | The public contact address in the privacy, terms, about and contact documents; account questions, data access and correction, deletion and other privacy requests, content reports and appeals; the contact address given to app-store and provider reviewers |
| `support-noreply@mokaair.com` | sends only | `COMMUNITY_MAIL_FROM` for automated account mail: email verification, password reset and account-deletion confirmation |

## Where the public address appears

The four information documents carry it as a confirmed fact (`requirements.contact`) in
all five locales, and `/privacy` and `/contact` also render a `mailto:` link so a
request is one tap away. The other two pages point at the same address through their
confirmed facts rather than repeating the link. Nothing invites a reader to write to
the send-only sender; `apps/api/tests/test_site_pages.py` holds both rules.

Requests that arrive here have statutory deadlines under Taiwan's Personal Data
Protection Act, and the published documents state them: 15 days to answer an access or
review request (extendable by 15), 30 days for correction, suspension of processing or
deletion (extendable by 30). The mailbox therefore needs a person watching it, not just
a forwarding rule.

## Where the sending address belongs

`COMMUNITY_MAIL_FROM` is the only place the sender is configured, and
`apps/api/app/community/jobs.py` uses it for every account mail. Set it to a display
name plus the send-only address, for example `Mokaair <support-noreply@mokaair.com>`.
Alongside it, `COMMUNITY_SMTP_HOST`, `COMMUNITY_SMTP_PORT`, `COMMUNITY_SMTP_STARTTLS`
and the SMTP credentials must be configured and verified before password recovery,
email verification or account deletion can work in production; production additionally
refuses to send without STARTTLS.

Outside the repository the domain still needs SPF, DKIM and DMARC records that
authorize whichever SMTP service sends the mail. Without them, verification and
password-reset mail lands in spam and the account flows look broken rather than
unconfigured.

Every link in that mail is valid for 30 minutes and single use, so a delayed delivery
is indistinguishable from an expired link. Treat a delivery-delay report as an
authentication problem first.

### The reply gap, still open

`send_mail` sets `From` and `To` only. A user who replies to an automated mail is
replying to the send-only address, and nobody reads it. Until
[`2026-09-10-account-mail-reply-to`](../tasks/open/2026-09-10-account-mail-reply-to.md)
adds a configurable `Reply-To: support@mokaair.com`, either point the send-only
mailbox's auto-reply at `support@mokaair.com` or have the mail service rewrite replies
to it — the published documents already tell readers to write to `support@` instead.

## Publishing the documents that carry these facts

The documents are drafts in source control
(`apps/api/app/site_pages/drafts/<locale>.json`); they become public only through an
explicit admin publication, one slug and locale at a time, in `/admin/site-pages`:

1. **Create missing drafts in five languages** — initializes only missing slug/locale
   pairs and overwrites nothing that exists.
2. Read the document in the language you are publishing. The owner's confirmed facts
   are already filled in; the effective date is deliberately empty, because it is the
   date a person decides to publish.
3. Set that effective date — it may not be in the future — then publish with an
   explicit confirmation and a reason. Repeat for all five locales of a page, so no
   language is left without a policy it is pointed at.

Google and Apple sign-in review need a publicly reachable privacy URL
(`/zh-TW/privacy` and its four siblings), so that review cannot start until
step 3 has happened at least for the locale submitted.

`effective_date` staying empty in source control is the gate, not an oversight: a
fresh install cannot serve a policy that no person has approved.
