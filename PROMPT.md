# Prompt: LA County Health Alert — Full MVP Build

## What This Is

A simple product that sends LA County restaurant health violation data to pest control and commercial cleaning companies. They pay $200/month to get alerts when restaurants get shut down or score poorly on inspections.

This is NOT a platform. This is a list that gets sent to people. Keep it simple.

## What I Need You to Build (All of It)

### Part 1: Scrape the Data

**Source 1: Facility Closures**
- URL: http://publichealth.lacounty.gov/eh/i-want-to/view-inspection-results.htm
- Navigate to the "Facility Closures" tab
- Scrape the table. For each row, grab: Facility Name, Address, City, Closed Date, Reopened Date, Reason
- **Filter OUT** anything that already has a Reopened Date — we only want restaurants that are STILL CLOSED right now
- **Filter OUT** non-restaurant facilities (swimming pools, apartments, motels, schools, hotels, recovery centers, etc.) — keep only restaurants, food markets, bakeries, bars, cafeterias, food trucks
- Save to a CSV: `closures.csv`

**Source 2: Low Inspection Scores (B/C Grades)**
- Same site, "Inspection Results" tab
- Search for restaurants inspected in the last 7 days
- Filter to only entries that have a score below 90
- Grab: Facility Name, Address, City, Inspection Date, Score
- Filter OUT non-restaurant facilities (same as above)
- Save to a CSV: `low_scores.csv`

**Technical notes for scraping:**
- This is likely a JavaScript-rendered site — use Playwright
- Be respectful: 3-5 second delays between page loads
- If the site blocks you or requires CAPTCHA, STOP and tell me. We'll do it manually.
- If the data is also available as a bulk download at data.lacounty.gov, try that first — it's easier

### Part 2: Enrich the Data

For every facility in both CSVs:
- **Google Maps link**: Construct a URL: `https://www.google.com/maps/search/{name}+{address}+{city}+CA`
  - URL-encode the name and address
  - This is Phase 1 enrichment — no API key needed, subscribers click through to see phone number
- Add a column `google_maps_link` to both CSVs
- That's it for now. No phone number extraction, no geocoding, no Places API. Keep it simple.

### Part 3: Build the Landing Page

A single HTML file that I can deploy on Cloudflare Pages. This is the entire "website."

**Structure:**

**Hero section:**
- Headline: "Know When LA Restaurants Get Shut Down — Before Your Competitors Do"
- Subheadline: "Twice-weekly alerts when restaurants fail health inspections or get closed. Name, address, violation type, and Google Maps link. Delivered however you want."
- CTA button: "Start Getting Alerts — $200/month" → links to `[STRIPE_CHECKOUT_URL]` (I'll fill this in later)

**Live data preview section:**
- Headline: "This Week's Closures (Preview)"
- Show a table with the REAL closure data from Part 1, but **only show Facility Name, City, and Violation Reason**
- Do NOT show address, phone, or Google Maps link in the preview — that's what they pay for
- Below the table: "Subscribers get full addresses, Google Maps links, and map view for every closure."
- If we have B/C grade data, show a count: "Plus [X] restaurants scored below 90 this week"

**How You Get It section:**
- "Pick the format that fits your workflow:"
- Four options displayed as cards or icons:
  1. 📧 **Email** — "Clean summary in your inbox every Monday and Thursday at 7am"
  2. 📱 **Text Alerts** — "SMS with restaurant name, violation, and map link"
  3. 📊 **Live Spreadsheet** — "Google Sheet you can bookmark, sort, and filter — always current"
  4. 🗺️ **Map View** — "See all closures on a map. Plan your route. Tap for directions."
- Note: "All four channels included. Pick one or all of them. Same data, same timing."

**Pricing section:**
- Keep it dead simple:
- "$200/month — Standard" — Twice weekly (Monday + Thursday)
- "$400/month — Priority" — Daily updates
- "Cancel anytime. Try one week free — just reply to your first alert if it's not worth it."
- CTA button: same Stripe Checkout link

**Signup form (below pricing):**
- Name
- Company Name
- Email
- Phone (optional — for SMS alerts)
- Checkboxes: "How do you want to receive alerts?" → Email / Text / Spreadsheet / Map (can select multiple)
- Submit → this can go to Formspree (free) or Airtable or just mailto: for now
- Note: the Stripe payment is separate from this form. They fill out the form for preferences, click the Stripe link to pay. I match them up manually.

**Footer:**
- "Data sourced from LA County Department of Public Health public records"
- Contact email
- One line about who you are

**Design notes:**
- Mobile-first. These people will look at this on their phone.
- Clean, professional, but not corporate. No SaaS aesthetic. Think "useful tool for tradespeople."
- Fast loading. Single HTML file, inline CSS, no frameworks. Maybe Tailwind via CDN if it helps.
- Red/orange accent colors for urgency. The data should feel time-sensitive.
- The preview data table is the star — it does the selling. Make it prominent.

### Part 4: Set Up the Four Delivery Channels

Build simple templates/scripts for each channel so I can deliver on day one:

**Channel 1: Email Template**
- An HTML email template (inline CSS for email client compatibility)
- Section 1: "🚨 Still Closed — Act Now"
  - Table: Facility Name | Address | City | Violation | Google Maps Link
- Section 2: "⚠️ At Risk (B/C Grades)"
  - Table: Facility Name | Address | City | Score | Grade | Google Maps Link
- Section 3: Links to the map view and spreadsheet
- Header: "LA County Restaurant Health Alert — [DATE]"
- Footer: "Reply to unsubscribe" (manual unsubscribe is fine for <50 subscribers)
- Output this as an HTML file I can copy-paste into Gmail or any email tool

**Channel 2: SMS Template**
- A plain text file with one message per closure, formatted:
  `🚨 CLOSED: [Name], [City] - [Violation Reason] - Maps: [short Google Maps link]`
- Keep under 160 characters per message if possible
- Also include a summary message for B/C grades:
  `⚠️ [X] LA restaurants scored below 90 this week. Details: [link to Google Sheet]`
- Output as a text file I can copy-paste into Google Voice or SimpleTexting

**Channel 3: Google Sheet**
- Create a CSV formatted for easy import into Google Sheets
- Two sections (can be two CSVs or one with a "Type" column):
  - Active Closures: Facility Name, Address, City, Closed Date, Violation, Google Maps Link, Status ("STILL CLOSED")
  - B/C Grades: Facility Name, Address, City, Inspection Date, Score, Grade, Google Maps Link
- I'll manually import this into a Google Sheet and share the link with subscribers
- Include instructions for how to set up the Google Sheet (formatting, color coding, sharing settings)

**Channel 4: Map**
- Generate a KML file that I can import into Google My Maps
- One pin per facility (closures + B/C grades combined)
- Each pin should have:
  - Name: Facility Name
  - Description: Violation reason (or score/grade), address, Google Maps directions link
- Color coding: Red pins for closures, Yellow pins for B grades, Orange pins for C grades
- Include instructions for how to import KML into Google My Maps and share the link

### Part 5: Buyer Lead List

**Goal:** Build a list of pest control and commercial cleaning companies in LA County with enough info that I can send them a cold email pointing to the landing page. The landing page does the selling — I just need to get them there.

**Ideal Customer Profile (ICP):**

Primary: **Small/independent pest control companies in LA County**
- 1-20 employees
- Already serves commercial accounts (restaurants, food service)
- Mentions "commercial," "restaurant," or "food service" on their website or Google listing
- Independent operators, NOT national chains (Terminix, Orkin, Rentokil) — chains have corporate lead gen, they don't buy from you

Secondary: **Commercial cleaning companies in LA County**
- Same size range (1-20 employees)
- Specializes in or mentions restaurant/kitchen cleaning
- NOT residential cleaning companies — they don't serve this market

**What to capture for each lead:**
- Company Name
- Owner/Manager Name (if visible on website or Google listing)
- Phone Number
- Email Address (check website contact page, about page, footer, or Google listing)
- Website URL
- Google Maps listing URL
- Specialty description (from their Google listing or website)
- Priority flag: HIGH if they mention "commercial," "restaurant," or "food service" anywhere

**How to find them:**

Scrape or search Google Maps for these queries in Los Angeles County:
- "pest control" — top 50
- "commercial pest control" — top 30
- "restaurant pest control" — top 20
- "commercial cleaning" — top 50
- "restaurant cleaning" — top 30
- "kitchen deep cleaning" — top 20
- Deduplicate by company name / phone number

Also check:
- Yelp search for same queries — sometimes surfaces different companies
- Thumbtack / Angi listings for commercial pest control and cleaning in LA

Save to: `buyer_leads.csv`
Columns: Company Name | Contact Name | Phone | Email | Website | Google Maps URL | Specialty | Priority

**Target: 150+ leads total**

**How I use this list:**
- Round 1: Cold email to all 150 with a link to the landing page. Subject line references real data: "8 LA restaurants shut down for health violations this week." Body is 2-3 sentences max + landing page link. That's it — no pitch, no explanation, just get them to the page.
- Round 2 (if needed): Text follow-up to non-openers 2-3 days later. One sentence + link.
- Round 3 (if needed): Call the top 20-30 high-priority leads. "Hey, sent you something about restaurant health violation leads, worth checking out: [URL]." Get off the phone in 30 seconds.

The landing page does the converting. The outreach just gets them there.

**Technical notes:**
- Google Maps scraping might hit rate limits — go slow, 5-10 second delays
- If Google blocks automated scraping, I'll collect leads manually. Don't spend more than 30 minutes trying.
- For email addresses: scrape the company's website contact page, about page, and footer. Many small businesses list email on their Google Business profile too.
- If you can't find an email, just get the phone number — I can text them the link.

### Part 6: Live Operations Dashboard

A single HTML page that auto-refreshes every 60 seconds, showing me the current state of everything. This is my internal tool — subscribers never see this.

**What it shows:**

**Section 1: Data Status**
- Last scrape timestamp (when did I last pull closure/score data?)
- Number of active closures right now (still closed, no reopened date)
- Number of B/C grades from the last 7 days
- A mini table of the 5 most recent closures with name, city, date, status

**Section 2: Subscriber Status**
- Total paying subscribers
- Breakdown by channel preference (how many want email, SMS, spreadsheet, map)
- List of all subscribers: name, company, email, channel preference, signup date
- This reads from a simple JSON file (`subscribers.json`) that I update manually when someone signs up

**Section 3: Delivery Status**
- Last delivery date (when did I last send alerts?)
- What was sent: number of closures, number of B/C grades
- Next scheduled delivery (Monday or Thursday)

**Section 4: Outreach Status**
- Total buyer leads collected
- Emails sent (I update this manually in a JSON file)
- Responses / signups (I update manually)
- Conversion rate

**How it works:**
- Single HTML file: `dashboard.html`
- Reads from local JSON data files that the scraper and I update:
  - `data/closures.json` — current closure data (output by scraper)
  - `data/low_scores.json` — current B/C grade data (output by scraper)
  - `data/subscribers.json` — subscriber list (I edit manually)
  - `data/outreach.json` — outreach stats (I edit manually)
  - `data/deliveries.json` — delivery log (I update after each send)
- Auto-refreshes every 60 seconds via meta refresh or JavaScript setInterval
- Runs locally — I just open the HTML file in my browser
- No server needed. It reads the JSON files via fetch from a local directory.
- If running locally via file:// doesn't work with fetch, include a tiny Python HTTP server command in the README: `python -m http.server 8000`

**Design:**
- Dark mode, dense layout — this is an ops tool, not a customer-facing page
- Green/red status indicators (green = fresh data, red = stale or overdue)
- Flag anything that needs attention: "Data is 4 days old — time to scrape" or "3 subscribers haven't received this week's alert yet"
- Minimal — no charts, no graphs, just numbers and status indicators

Output as: `dashboard.html` (plus the JSON file templates with example data)

- No database (SQLite, Postgres, or otherwise)
- No backend server
- No user authentication
- No Stripe webhook integration (I'll use a payment link and match subscribers manually)
- No scoring engine (every closure is a good lead, period)
- No automated scheduling (I run the scraper manually twice a week for now)
- No fancy frameworks (no React, no Next.js, no TypeScript)

## Tech Stack

- Python 3 for scraping and data processing
- Playwright for the county health site (if it needs JS rendering)
- Plain HTML/CSS for the landing page (Tailwind via CDN is fine)
- Output files: CSVs, HTML email template, SMS text file, KML map file
- That's it.

## Output Files I Expect

When this is done, I should have these files ready to use:

```
output/
├── closures.csv                    # Active closures with Google Maps links
├── low_scores.csv                  # B/C grades with Google Maps links
├── landing_page.html               # Deploy to Cloudflare Pages
├── email_template.html             # Copy into Gmail for sending
├── sms_messages.txt                # Copy into Google Voice / SimpleTexting
├── google_sheet_import.csv         # Import into Google Sheets
├── map_pins.kml                    # Import into Google My Maps
├── buyer_leads.csv                 # Pest control + cleaning company contacts
├── dashboard.html                  # Local ops dashboard (auto-refreshes every 60s)
├── data/
│   ├── closures.json               # Closure data for dashboard (scraper outputs this)
│   ├── low_scores.json             # B/C grade data for dashboard (scraper outputs this)
│   ├── subscribers.json            # Subscriber list (I edit manually)
│   ├── outreach.json               # Outreach stats (I edit manually)
│   └── deliveries.json             # Delivery log (I update after each send)
└── README.md                       # Instructions for deploying and running everything
```

## My Workflow After This Build

1. Deploy landing page to Cloudflare Pages (free)
2. Set up Stripe payment link ($200/month recurring), paste URL into landing page
3. Import google_sheet_import.csv into Google Sheets, share link
4. Import map_pins.kml into Google My Maps, share link
5. Paste email_template.html into Gmail, send to paying subscribers
6. Paste sms_messages.txt into Google Voice, send to SMS subscribers
7. Send cold emails to buyer_leads.csv driving them to the landing page
8. Wait for signups
9. Repeat twice a week: Monday and Thursday mornings
   - Run the scraper
   - Review the data for 15-20 minutes
   - Update all four channels
   - Send

Total weekly time commitment: ~1 hour
Total monthly cost: $0 (until I need to upgrade email/SMS tools)
Revenue per subscriber: $200/month
Break-even: 1 subscriber (I'm already profitable)

## Priority

Get the scraper working and the landing page built FIRST. Those are the two things I need to start selling. The email template, SMS messages, KML file, and Google Sheet CSV are important but secondary — I can format those manually for the first few subscribers if needed.
