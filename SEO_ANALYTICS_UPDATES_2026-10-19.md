# MortgageStressScore: SEO and Analytics update — October 19, 2026

## Changes deployed in this release
- New Jersey assistance page: official NJHMFA ERMA closure, current FMAP options, no guaranteed foreclosure timeline, replacement of Homestead Benefits with ANCHOR, official source references, updated structured data.
- FHA content intent separation: `fha-loan-modification-options.html` remains the HUD loss-mitigation comparison; `fha-loan-modification.html` becomes an FHA application checklist. Both URLs remain live because Search Console query history was unavailable. Do not add a 301 redirect until indexing and demand are compared.
- Improved Guides hub, related links from relevant mortgage hardship guides, editor policy and source disclosure.
- Updated sitemap `lastmod` only on modified pages.

## GA4 events (measurement ID G-TJTKS00LW6)
| Event | Trigger | Allowed parameters | Meaning |
| --- | --- | --- | --- |
| `score_start` | First interaction with calculator fields or calculate button | `tool=mortgage_stress_score` | User began tool |
| `score_complete` | Successful calculation and action-plan rendering (once per page load) | `tool=mortgage_stress_score` | Tool completed |
| `premium_click` | Valid click through to Stripe checkout, or direct home premium-pack link | `placement`, `value=9`, `currency=USD` | Checkout intent only |
| `checklist_form_opened` | User opens the external checklist form | `placement=action_plan` | External form click |

**Privacy:** Never send payment amounts, gross income, calculated risk/score, missed-payment count, state, loan type, or Google Form answers to GA4 or Google Ads via event parameters. Browser-only calculator state and explicit Google Form submissions are separate from analytics events. Confirm analytics consent behavior and the site's privacy notices if tracking rules change.

**Purchase tracking is NOT implemented by this static-site update.** `premium_click` is not a sale. To report `purchase` accurately, use a verified Stripe webhook/approved server-side integration, deduplicate by checkout session/payment ID, and only emit the event after payment success. Do not fire `purchase` on a checkout-button click or unverified redirect.

## GA4 configuration to check in the dashboard
1. Verify events appear in DebugView/Realtime after a fresh interaction.
2. Designate `score_complete` as a key event if it is a useful engagement goal.
3. Keep `premium_click` separate from confirmed revenue.
4. Review the prior legacy `conversion_event_submit_lead_form` configuration: calculating an anonymous educational score is **not** submission of a lead form. Update corresponding Google Ads/GA4 conversions manually and compare against the previous baseline.

## Google Search Console validation needed
1. Request inspection for the home page, New Jersey, both FHA URLs and Guides.
2. Compare 3-month Google Search Console query/page performance to verify any cannibalization **before** redirecting one FHA URL.
3. Re-submit the unchanged sitemap URL `https://mortgagestressscore.com/sitemap.xml` only if necessary; file content was refreshed in this release.
4. Recheck NJ program status and HUD policy when official agencies change published guidance.

Do not describe these changes as an SEO traffic increase until clicks and impressions are measured after deployment.
