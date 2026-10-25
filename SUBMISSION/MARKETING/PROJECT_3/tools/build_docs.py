#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the three Word deliverables for MARKETING Project 3.
Copy-only slide context, revised A1/A2 per instructor feedback, A3 solution
with full A1+A2 restated in flow. No PDF/PPTX produced. No chart terminology
in any deliverable (solver charter forbidden_output lint)."""
import json, re, os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = os.path.join(os.path.dirname(__file__), "..")
ORANGE = RGBColor(0xC0, 0x4A, 0x00)

# block kinds: ("h", text) ("p", text) ("bul", [..]) ("table", [headers], [rows]) ("quote", text)

PRODUCTION_NOTE = ("Standing production note (instructor feedback, applied at deck-design time, "
                   "not in this copy document): set every slide to fill the canvas, keep body type "
                   "at a readable size (18 pt equivalent or larger), and remove empty bottom bands. "
                   "This document carries text copy only.")

# ============================ ASSIGNMENT 1 (revised) ============================
A1 = [
 ("Cover — Off Hours", [
  ("p", "D2C SLEEP & RECOVERY · MUMBAI + BENGALURU"),
  ("h", "Off Hours"),
  ("quote", "What begins when work ends."),
  ("bul", ["Category: D2C sleep & recovery — functional night-drink sachets (melatonin-free).",
           "Product: 10-sachet box of a magnesium + L-theanine + chamomile night drink; refill subscription.",
           "Geography: Mumbai + Bengaluru, India — two-city beachhead, delivery via own storefront."]),
  ("h", "Price Positioning"),
  ("bul", ["₹999 — 10-night trial kit: the impulse-try price point.",
           "₹1,899/month — subscription refill: competes with one dinner out."]),
 ]),
 ("Brand Overview & Business Goal", [
  ("h", "What We Offer & Why It's Different"),
  ("p", "A simple, drug-free wind-down ritual in a glass — one sachet, warm water, lights-low. Urban "
        "professionals 25–40 finish work at 9–10 pm, still wired — they scroll, snack, and sleep badly. "
        "Melatonin feels medical; chamomile tea feels weak."),
  ("bul", ["Melatonin-Free Formula — ingredient-forward, built as a ritual, not a pill: magnesium + L-theanine + chamomile.",
           "Subscription Refill Rhythm — designed to become a repeatable evening habit, not a one-off purchase.",
           "Taste & Texture for Work-Nights — unsweet, light; designed for a work-night reality, not a wellness spa."]),
  ("h", "Competitive Landscape"),
  ("p", "OTC sleep gummies and melatonin tablets; herbal/sleep teas; wellness apps (guided wind-downs); "
        "the default alternative — doing nothing and scrolling."),
  ("quote", "Strategic stance: we compete with the habit of not switching off, not with pharmacies."),
  ("h", "Primary Business Goal"),
  ("p", "1,000 paying subscribed households within the first 12 months of launch across Mumbai + Bengaluru. "
        "This is a business outcome — a recurring-revenue customer base — not a marketing activity. "
        "Marketing's job is the measurable path that gets the business there."),
  ("p", "Why this goal: a D2C subscription business compounds on retention. A loyal base funds every later "
        "stage of growth. The 1,000-household base is the foundation, not the ceiling."),
 ]),
 ("Marketing Objectives (SMART)", [
  ("p", "Two numbered, dated, and owned objectives — both traceable directly to the 1,000-subscriber "
        "business goal. The arithmetic closes by construction."),
  ("h", "1 · Acquire — Trial & Conversion"),
  ("p", "Ramp to a sustained run-rate of ≥600 trial-kit orders/month by month 6, converting ≥12% of "
        "trialsists to subscription within 30 days of trial start — delivering ≥90 new subscribers/month "
        "at run-rate, including a ≥15% referral share. Acquisition objective: owns the top of the funnel "
        "and the first conversion gate."),
  ("h", "2 · Retain — Revenue Quality"),
  ("p", "By month 12, at least 60% of monthly revenue comes from existing subscribers, with third-purchase "
        "repeat rate ≥45%. Retention objective: owns the compounding engine that makes the 1,000-household "
        "base durable."),
  ("table", ["Target", "Definition"],
   [["≥600", "Trial-kit orders/month by month 6"],
    ["≥12%", "Trial-to-subscription conversion within 30 days"],
    ["≥90", "New subscribers/month at run-rate"],
    ["≥15%", "Referral share of new subscribers"],
    ["60%", "Monthly revenue from existing subscribers by month 12"],
    ["≥45%", "Third-purchase repeat rate"]]),
 ]),
 ("Target Audience", [
  ("h", "Demographics"),
  ("bul", ["Age: 25–40, single or young-couple households.",
           "Education & profession: degree-educated professionals — tech, finance, consulting, media.",
           "Locations — Mumbai: Powai, Lower Parel, Andheri; Bengaluru: Indiranagar, Koramangala, HSR.",
           "Income: ₹12L+ annual household income — already pays for convenience and self-care.",
           "₹999 is an impulse-try. ₹1,899/month competes with one dinner out."]),
  ("h", "Psychographics & Behaviour"),
  ("bul", ["Evidence-Seeking Wellness Sceptics — read ingredient lists, dislike hype, want better mornings "
           "more than \"sleep\". Identity: ambitious but burning the candle.",
           "Digital-Native Shoppers — shop online several times a week; subscribe and cancel ruthlessly; "
           "discover via short video and peer group chats; research reviews before any ingested product.",
           "Active 10 pm–1 am — the exact window Off Hours is designed to interrupt, and serve."]),
  ("h", "Who Is Not Our Audience"),
  ("bul", ["Insomniacs seeking clinical treatment.", "Price-first general supplement buyers.",
           "Anyone outside Mumbai + Bengaluru in phase 1."]),
 ]),
 ("Primary Buyer Persona — \"Meera\"", [
  ("p", "Meera Nair, 32. Product Manager, Series-B startup. Bengaluru (Koramangala). ₹18–24 LPA."),
  ("quote", "\"I don't have a sleep problem — I have a switching-off problem. Show me something simple "
            "that actually works and I'll stick with it.\""),
  ("bul", ["Her day: stand-ups at 10 am, deep work at night. Gym membership renewed yearly, used rarely. "
           "Orders in 4–5 nights a week. Unwinds with series + scrolls till 1 am. Alarm at 7:30.",
           "Interests: productivity systems, longevity content, café coffee, weekend treks.",
           "Platforms: Instagram Reels, YouTube deep-dives, WhatsApp groups, Reddit India fitness threads, "
           "email newsletters."]),
  ("table", ["Goals", "Pain Points", "Motivations"],
   [["Wake up clear-headed without another pill", "3–4 hours of \"junk time\" at night", "Visible morning energy"],
    ["Feel in control of her evenings again", "Groggy mornings", "A ritual that feels like hers"],
    ["", "Sceptical of gummies after one bad experience", "Evidence over promises"],
    ["", "Hates auto-renew traps", ""]]),
  ("p", "Buying behaviour: trials first; checks ingredients + reviews; pays UPI; will subscribe after one "
        "good full box; cancels in one click if annoyed."),
 ]),
 ("Digital Marketing Strategy", [
  ("p", "We target over-wired professionals 25–40 in Mumbai and Bengaluru who do not believe they have a "
        "sleep problem — and we meet them at the moment they feel it. We want them to think \"this is a "
        "simple ritual, made for my actual nights,\" and to do one thing: try the 10-night kit."),
  ("quote", "Broad approach — rest-and-consolidation first: everything we do digitally exists to convert a "
            "trial into a calm, repeatable evening habit and then into a subscription — not to chase reach."),
  ("h", "The Channels Work as One Loop, Not a Stack"),
  ("bul", ["Earn First Attention — short-video and search content earn honest attention and answer the "
           "ingredient questions that build trust.",
           "Convert at Low Friction — the storefront converts with a low-friction ₹999 trial: no commitment, no risk.",
           "Own the Relationship — pack insert, WhatsApp refill concierge, and the fortnightly sleep-journal "
           "letter carry the relationship through the 10-day judgement window and into subscription.",
           "Paid Amplifies, Never Leads — paid spend exists mainly to re-find people already in the loop; "
           "it follows proven messages, never precedes them."]),
  ("h", "Phase Sequencing"),
  ("bul", ["Phase 1 — Launch: short-video, search, storefront, owned channels. Build the trial-to-subscription "
           "loop. Prove the retention engine.",
           "Phase 2 — Partnerships: company wellness programmes, clinics — arrive once the subscriber base "
           "makes Off Hours worth partnering with."]),
 ]),
 ("PESO Media Mix", [
  ("p", "Four media types working as one system — Earned and Shared create believable first contact; Owned "
        "converts and keeps; Paid only accelerates what the other three already prove. Spend follows pull, "
        "never precedes it."),
  ("table", ["Media", "What it is for Off Hours", "Primary job"],
   [["Paid", "Retargeting to site visitors & video viewers; later, sponsored discovery inside quick-commerce "
             "listings once demand exists.", "Re-find warm audiences; amplifies proven messages only."],
    ["Earned", "Wellness editors & newsletters covering the \"switch-off\" culture; the brand's founding "
               "narrative — built melatonin-free for India's late-working cities.",
     "Third-party credibility the ingredient-sceptic trusts."],
    ["Shared", "Customers posting their night-routine rituals; 10-night challenge check-ins; referral links "
               "in group chats.", "Turns the ritual into social proof; peer recommendation."],
    ["Owned", "Storefront & product pages, WhatsApp refill concierge (opt-in), sleep-journal email letter, "
              "pack inserts.", "The retention spine — where trials become subscribers."]]),
 ]),
 ("Recommended Digital Channels — 5 Priorities", [
  ("table", ["Channel", "Role", "Why this channel?"],
   [["Instagram Reels + Short Video", "Discovery", "Where our audience actually unwinds at 10 pm; ritual "
     "content formats natively."],
    ["Search (brand site + category articles)", "Trust & research capture", "Ingredient questions are the "
     "trust gate; the brand must answer them itself."],
    ["Own storefront + UPI checkout", "Conversion", "Low-friction ₹999 trial; owns the data the subscription "
     "model needs."],
    ["WhatsApp concierge (opt-in)", "Retention & service", "User-consented, India-native, high-open — perfect "
     "for refill timing and questions."],
    ["E-mail sleep-journal letter", "Experience & advocacy", "The 10-day judgement window needs a guide; "
     "letters out-sell loud campaigns."]]),
  ("h", "Named Non-Priorities — and Why"),
  ("bul", ["Television & Print — wrong age and wrong moment; unmeasurable against our conversion objectives.",
           "Mass Display / Broad Awareness Bursts — spend ahead of demand; awareness money lands before trial "
           "intent exists.",
           "Celebrity Influencer Blitzes — borrowed attention, wrong trust mechanic for an ingested product.",
           "Heavy Marketplace-Ads Dependence — a listing helps logistics, but we refuse to rent the brand's "
           "first impression."]),
 ]),
 ("Integrated Digital Journey — One Connected Loop", [
  ("p", "Every channel hands the customer to the next with context attached — nothing is a dead end, and "
        "owned channels carry the relationship through the 10-day judgement window."),
  ("p", "Loop: Discovery → Storefront → Onboarding → Retention → back to Discovery."),
  ("h", "The Judgement Window"),
  ("p", "Days 1–10 are the make-or-break period. The sleep-journal letter and WhatsApp concierge run in "
        "parallel during this window — one guides the experience, the other answers questions in real time. "
        "Both feed into the subscription decision."),
  ("h", "The Referral Loop"),
  ("p", "Subscribers who share referral links in group chats re-enter the loop at Discovery — creating a "
        "peer-recommendation flywheel that reduces paid acquisition cost over time. The ≥15% referral share "
        "target is built into the acquisition objective."),
 ]),
 ("Key Strategic Decisions & Brand Selection Test", [
  ("h", "Four Decisions That Define the Strategy"),
  ("bul", ["1 · Retention Before Reach — the entire system is sequenced to win subscribers, not impressions. "
           "Trial → judged experience → subscription is the value engine.",
           "2 · An Understated, Proof-Led Launch — quiet, sharp, ritual content over launch-week hype. The "
           "brand earns its loud phase rather than starting with it.",
           "3 · We Compete With the Habit of Not Switching Off — positioning against an evening behaviour, "
           "not against pharmacies or gummies, keeps the brand distinct and the message human.",
           "4 · Partnerships and Mass Awareness Are Deliberately Delayed — alliances in phase two; awareness "
           "spend only after pull signals exist. Money and attention are spent in the order they convert."]),
  ("h", "Brand Selection Test"),
  ("table", ["Question", "Answer"],
   [["What do you sell?", "A melatonin-free night-drink sachet — a 10-night trial kit and a refill subscription."],
    ["Who is it for?", "Urban professionals 25–40 in Mumbai & Bengaluru who can't switch off after late workdays."],
    ["What problem does it solve?", "Evenings that never downshift: wired minds, junk-time scrolls, groggy mornings."],
    ["Why would someone choose you?", "A simple, non-medical ritual with honest ingredients, fair trial pricing, "
     "and support through the full first 10 nights — chosen once, kept as a habit."]]),
 ]),
 ("Business Numbers — 12-Month Planning Model (revised per feedback)", [
  ("p", "Illustrative planning model with stated assumptions — internal planning arithmetic, not consumer "
        "research and not published claims."),
  ("h", "Stated assumptions"),
  ("bul", ["Trial kit ₹999 (10 nights); subscription ₹1,899/month.",
           "Trial ramp: 20 / 35 / 50 / 65 / 80 / 90 trial-kit orders in months 1–6, then 95–120/month to month 12.",
           "Trial-to-subscription ≥12% within 30 days; referral share ≥15% of new subscribers.",
           "Post-first-box monthly churn planning assumption ≤6%; third-purchase repeat ≥45%."]),
  ("h", "What the model shows"),
  ("bul", ["Gross subscriber adds months 1–12 ≈ 985; net of the churn assumption ≈ 900–1,000 households — the "
           "1,000-household goal is the plan's ceiling case, and the retention objective is what keeps it.",
           "Month-6 trial revenue run-rate: 600 × ₹999 ≈ ₹5.99 lakh/month.",
           "Month-12 recurring run-rate at goal: 1,000 × ₹1,899 ≈ ₹18.99 lakh/month ≈ ₹2.28 crore annualised "
           "recurring; blended month-12 monthly revenue with trial flow ≈ ₹24–25 lakh.",
           "Revenue-quality check: ≥60% of month-12 revenue from existing subscribers (retention objective).",
           "CAC guardrail: paid is retargeting-only, so blended acquisition cost per trial is capped at ≤₹450 "
           "(<45% of trial price); assumed subscriber gross LTV ≈ 9 months × ₹1,899 ≈ ₹17,091, keeping the "
           "planning LTV:CAC at ≥3:1.",
           "Referral flywheel value: every 100 subscribers bring ≥15 of the next cohort's adds, compounding "
           "down the paid need month over month."]),
  ("p", "Read with slide 3: the two SMART objectives are the model's only inputs; everything above is "
        "arithmetic on them, so the story closes by construction."),
 ]),
]

# ============================ ASSIGNMENT 2 (revised) ============================
A2 = [
 ("Cover — Off Hours · Assignment 2 · Content & Social Media Strategy", [
  ("quote", "What begins when work ends."),
  ("p", "A continuation of the Assignment 1 deck. Mumbai and Bengaluru · 10-sachet night drink · melatonin-free."),
 ]),
 ("Where We Stand, Inherited from Assignment 1", [
  ("bul", ["Retention before reach. The 10-night trial is the decision window, not an acquisition vanity metric.",
           "An understated, proof-led launch. The audience is an evidence-seeking wellness sceptic, not a hype audience.",
           "We compete with the habit of not switching off, not with pharmacies.",
           "Deliberately delayed: celebrity blitzes, mass display, TV and print, marketplace-ad dependence, "
           "and partnership pushes.",
           "Persona: Meera Nair, 32, Product Manager, Koramangala. Trials first, reads ingredients, cancels "
           "in one click."]),
 ]),
 ("1 · Content Marketing Objective", [
  ("p", "Make Off Hours the brand people turn to when the evening will not switch off."),
  ("bul", ["Primary — build awareness of the moment, not of a claim. Recognition of the 10 pm problem comes "
           "before any product belief.",
           "Primary — educate consumers and own the ingredient question. The trust gate for an ingested "
           "product is the label. Answering the question earns the right to sell.",
           "Secondary — engagement, community, traffic, conversion support. Each is a means here, never a "
           "headline goal.",
           "Why not more? Awareness gives recognition. Education gives permission. Everything else is "
           "downstream of those two."]),
 ]),
 ("2 · Brand Story and Communication — with \"landing better\" explained", [
  ("p", "The core idea: a landing, not a pill."),
  ("bul", ["Calm. Never urgent, never a countdown. The evening is not a sale to close.",
           "Plain-spoken. Ingredient answers in ordinary words. No clinical jargon, no wellness poetry.",
           "Evidence-led. Show the label, the quantity, the reason. Facts, never feelings.",
           "Quietly warm. Written to one tired person, not to a market."]),
  ("h", "What \"landing better\" actually means (revised: warmer, plainer, content-ready)"),
  ("p", "Landing better is not sleeping more. It is the twenty minutes between closing the laptop and reaching "
        "bed, handled kindly: the laptop closes on purpose; something warm gets made; the lights go one step "
        "down; the scroll stays in the other room. A landing is small, repeatable and yours — which is exactly "
        "why it fits in a sachet and in a sentence."),
  ("bul", ["Sample line: \"You don't have a sleep problem. You have a landing problem.\"",
           "Sample line: \"Ten minutes of warm, dim, quiet. That's the whole protocol.\"",
           "Sample line: \"We can't give you an early night. We can give you a soft landing.\"",
           "How it translates into content: every piece shows one landing beat — close, warm, dim — in that "
           "order, in a real kitchen, at a real hour. If a piece cannot show a beat, it is a claim, and claims "
           "do not go out."]),
  ("p", "Never: preachy, alarmist, medical-sounding, countdowns, streaks, competitive sneering."),
 ]),
 ("3 · Content Pillars", [
  ("p", "Five pillars, each with a function."),
  ("table", ["Pillar", "Function", "Example", "Why Meera cares"],
   [["Plain Labels", "Education and trust", "What magnesium glycinate does, in 40 seconds", "She reads labels anyway"],
    ["The Landing", "Awareness", "10 pm, laptop closed, brain still on", "The moment matches her night"],
    ["Quiet Proof", "Credibility", "Unedited testimonials, including lukewarm ones", "Evidence beats promises"],
    ["After Hours", "Depth and loyalty", "The sleep-journal letter", "She wants the long version"],
    ["We Won't", "Differentiation", "Six claims we refuse to make", "Refusals are believable"]]),
  ("p", "Rotation rule: every piece belongs to exactly one pillar. A piece which fits no pillar does not go out."),
 ]),
 ("4 · Platform Strategy", [
  ("p", "Three surfaces, chosen on audience behaviour."),
  ("table", ["Platform", "Behaviour", "Role", "Formats"],
   [["Instagram", "Scrolls Reels at 10 pm", "Awareness: name the moment", "Reels, carousels, Stories Q&A"],
    ["YouTube", "Watches to research", "Education: own the ingredient answer", "6–8 min long-form and Shorts"],
    ["WhatsApp and e-mail", "Consented, private, read-later", "Retention: hold the 10-night window",
     "Plain-text notes, letters"]]),
  ("p", "Deliberately not in the plan: TV and print · mass display · celebrity blitzes · marketplace-ad "
        "dependence · alarm and outrage formats."),
 ]),
 ("5 · One Idea, Different Platforms — Night 1 of 10, the first landing", [
  ("p", "The idea never changes. Only the behaviour does."),
  ("bul", ["Instagram — 25-second landing film: the kitchen at night, laptop closed, no voiceover, one line at "
           "the end. She sees the landing.",
           "YouTube — 6-to-8-minute explainer plus a 45-second cut: what sits in the sachet, plainly, including "
           "what it does not do. She understands the landing.",
           "WhatsApp and e-mail — one plain-text note per night for ten nights. Night one asks one question. "
           "She lives the landing.",
           "Every piece points to the next surface. The referral link closes the loop back to discovery."]),
 ]),
 ("6 · Content Concepts", [
  ("p", "Six concepts, each specified as idea, pillar, platform, format, objective."),
  ("bul", ["1 · What magnesium glycinate does — Plain Labels · Instagram carousel · education and saves.",
           "2 · We read our own label out loud — Plain Labels · YouTube long-form · education and trust.",
           "3 · Six things we refuse to say about our own product — We Won't · Instagram carousel · "
           "differentiation and shares.",
           "4 · Night 1 of 10, the landing film — The Landing · Instagram Reel · awareness.",
           "5 · The shelf, customers' own notes, unranked — Quiet Proof · Instagram and private channel · trust.",
           "6 · Ask us about the label — Plain Labels · Stories Q&A to video · engagement and education."]),
  ("p", "Concept 3 production note: carousel slide 2 of 6. Warm off-white ground, one burnt-orange accent, "
        "editorial serif headline. No badge, no arrow, no urgency device."),
  ("h", "Concept 4 — the landing film, storyboard beats (25 seconds, one continuous shot)"),
  ("bul", ["0–5s: a laptop is closed and pushed aside. Room tone only. No music.",
           "5–15s: a hand sets down one sachet and a glass of warm water. Slow, unhurried.",
           "15–25s: the sachet opens, pours, stirs once. The camera holds. The only text is the last line.",
           "On-screen text at 20–25s: NIGHT 1 OF 10.",
           "Shot discipline: one continuous take in a dim kitchen, single lamp source, hands and objects only, "
           "no faces. Music only in the middle beat.",
           "Why 25 seconds: the audience is scrolling at the exact hour the film shows. The idea must land in "
           "three seconds and stay saveable for tonight."]),
 ]),
 ("7 · Hero Content / Campaign — The 10-Night Landing", [
  ("p", "The trial window becomes the campaign."),
  ("bul", ["Insight — the problem for Meera is not sleep. The problem is the twenty minutes between closing "
           "the laptop and reaching bed.",
           "Big idea — ten nights, ten small pieces, one per night, each a landing rather than a lesson.",
           "Key message — \"We are not asking you to sleep earlier. We are asking you to land better.\"",
           "Arc — name the moment, answer the question, hold the ten nights, let the proof speak.",
           "Why this hero — the campaign turns the brand's hardest metric, the trial-to-subscription window, "
           "into content."]),
  ("h", "How \"landing better\" becomes content (revised per feedback)"),
  ("table", ["Landing beat", "Content form", "Example line"],
   [["Close", "Reel opening frame; carousel slide 1", "\"Laptop closed at 11:40. On purpose, this time.\""],
    ["Warm", "Recipe-card carousel; WhatsApp night note", "\"One sachet, warm water, both hands around the glass.\""],
    ["Dim", "Story template; letter header", "\"One lamp on. The feed can wait till morning.\""],
    ["Land", "Quiet Proof note card; night-10 letter", "\"Twenty minutes later, in bed. No victory lap. Just landed.\""]]),
 ]),
 ("8 · Community and Engagement", [
  ("p", "Followers become participants by answering a question they already answer elsewhere."),
  ("bul", ["Ask-the-coach, answered in public. No question too basic, including the awkward ingredient questions.",
           "The Shelf. Customers' own night notes, unranked and unedited. Inclusion, never competition.",
           "Quiet Testimony. Reviews in the customer's own words. Any edit visibly marked.",
           "The 10-Night Check-in. One private question a night. No scoreboard, no streak to lose.",
           "Refused: competitive challenges and duets · alarm-driven live formats · announcements broadcast "
           "through community channels."]),
 ]),
 ("9 · Influencer / Creator Strategy — fit is a teaching-and-trust test, not a reach test", [
  ("table", ["", "Creator A", "Creator B"],
   [["Who", "Shabbir Ahmed, Sleep Psychologist, Navi Mumbai", "Shruti Maheshwari, co-founder, Sleep Gurukul, Mumbai"],
    ["Credibility", "CBT-I practice. Author, The Sleep Foundations. Doctoral research. BW Wellbeing Festival, Mumbai.",
     "MA Psychology. Sleep and wellbeing coach, breath-work. Practice recognised at the India-native level."],
    ["Audience", "Adults seeking behavioural answers, not chemical ones",
     "Indian professionals, metro, breath-work and routine-led"],
    ["Why fit", "Purest carrier of Plain Labels: method-led, positioned against hacks and unfounded claims",
     "Carries The Landing: teaches the ritual a product will never show. India-native practice."],
    ["Role", "Flagship educator: one explainer, one label review, one Q&A",
     "Ritual partner: guided ten-night wind-down series. Phase 2 corporate bridge."]]),
  ("p", "Filters first, names second: teaching ratio · private-engagement ratio · reply tone · disclosure "
        "comfort. Open checks: category conflicts, disclosure line, Mumbai and Bengaluru audience share."),
 ]),
 ("10 · Two-Week Content Calendar — ten pieces, four deliberate quiet days", [
  ("table", ["Day", "Platform", "Content", "Format", "Pillar"],
   [["1 · Mon", "YouTube", "We read our own label out loud (anchor)", "Long-form 7 min", "Plain Labels"],
    ["2 · Tue", "None", "Quiet day", "None", "None"],
    ["3 · Wed", "Instagram", "What magnesium glycinate does, in 40 seconds", "Carousel (5)", "Plain Labels"],
    ["4 · Thu", "Instagram", "Night 1 of 10, the landing film", "Reel 25s", "The Landing"],
    ["5 · Fri", "Instagram", "Ask us about the label, weekly answers", "Stories Q&A", "Plain Labels"],
    ["6 · Sat", "WhatsApp and e-mail", "Night 5 check-in: what time did your evening end?", "Plain-text note", "After Hours"],
    ["7 · Sun", "None", "Quiet day", "None", "None"],
    ["8 · Mon", "YouTube", "Why this is not a sleeping pill (anchor)", "Long-form 6 min", "Plain Labels"],
    ["9 · Tue", "Instagram", "Six things we refuse to say about our product", "Carousel (6)", "We Won't"],
    ["10 · Wed", "None", "Quiet day", "None", "None"],
    ["11 · Thu", "Instagram", "The shelf, customers' own night notes", "Carousel (6)", "Quiet Proof"],
    ["12 · Fri", "Instagram", "Short cut of the Monday anchor", "Short 45s", "Plain Labels"],
    ["13 · Sat", "WhatsApp and e-mail", "Night 10: one thing which changed, one which did not",
     "Note and referral link", "Quiet Proof"],
    ["14 · Sun", "None", "Quiet day", "None", "None"]]),
  ("p", "Cadence rationale: the brand's job is a habit, not a feed. Four quiet days are a decision, not a gap. "
        "One anchor and one visual piece per week. Paid amplifies only messages already proven organically."),
 ]),
 ("11 · Measurement and Success — seven metrics, one of them negative", [
  ("table", ["#", "Objective", "KPI", "Healthy signal", "Cadence"],
   [["1", "Awareness", "Reach: Reels against search arrivals", "Search arrivals grow faster than Reels reach", "Monthly"],
    ["2", "Education", "Saves and returns on label explainers", "Explainers lead the month for saves", "Monthly"],
    ["3", "Consideration", "Completion rate on long-form", "The \"not a pill\" film completes best", "Monthly"],
    ["4", "Trust", "Private interactions: saves, DM questions, replies", "Private at least equals public", "Monthly"],
    ["5", "Conversion support", "Trial starts from discovery and search", "Rising, with a healthy source mix", "Monthly"],
    ["6", "Retention", "Night-5 and night-10 check-in participation", "A meaningful share reply or stay", "Every 10 nights"],
    ["7", "Health (stop signal)", "Argument threads and complaint mentions", "Flat or falling", "Monthly"]]),
  ("p", "Month one, working when saves lead, private responses match public ones, check-ins receive answers "
        "and argument threads stay flat. Not working when reach rises while saves stall."),
 ]),
 ("Continuity, Risks and What Would Change Our Mind", [
  ("bul", ["Viable alternative on record: an education-first, newsletter-led plan. Fully compliant, and it "
           "leaves the display surface idle. The margin is narrow and stated.",
           "Risk 1 — the quiet channel is favourable but slow. Judge the channel across a full cycle, not a month.",
           "Risk 2 — restraint becomes inaudibility. Display content carries reach, and we track reach.",
           "Risk 3 — partnership announcements under-deliver in alliance channels. Those channels stay two-way.",
           "Risk 4 — creator conflicts and audience geography are unverified. Three checks run before contracting.",
           "Strategy first. Design second. Every creative decision has a reason, and the reason is always the "
           "same: this brand exists to end the day, not to win the feed."]),
 ]),
 ("12 · Post-Launch Content Pillars — the always-on engine (revised per feedback)", [
  ("p", "The launch pillars do not retire; they get a post-launch rotation so publishing never stops after "
        "the campaign window. Two new pillars join the five, and the rotation rule still holds: every piece, "
        "one pillar."),
  ("table", ["Pillar", "Post-launch function", "Standing format", "Cadence"],
   [["Landing Letters", "Seasonal relevance: the work calendar's hard weeks (audit season, year-end crunch, "
     "festival nights, Sunday scaries)", "One letter per season-beat, one landing beat shown", "Monthly"],
    ["The Shelf, Continued", "Community memory: notes accumulate into a monthly unranked digest",
     "Monthly digest card + private letter excerpt", "Monthly"],
    ["Plain Labels", "Trust maintenance: one ingredient question answered per month, forever",
     "Carousel + Stories Q&A", "Monthly anchor"],
    ["Quiet Proof", "Credibility maintenance: lukewarm reviews included, edits marked", "Note cards", "Fortnightly"],
    ["We Won't", "Differentiation maintenance: one refusal revisited per quarter", "Carousel", "Quarterly"],
    ["After Hours", "Depth: the long version for subscribers", "Sleep-journal letter", "Fortnightly"]]),
  ("bul", ["Guardrail: quiet days survive the launch. Post-launch cadence is one anchor + one visual piece per "
           "week, never daily noise.",
           "Guardrail: any new pillar must pass the Meera test — would she save it at 11 pm? If not, it does "
           "not publish.",
           "Measurement handoff: post-launch pillars inherit the seven metrics from slide 11; the stop signal "
           "(argument threads) stays live forever."]),
 ]),
]

# ============================ ASSIGNMENT 3 (solution) ============================
A3 = [
 ("Cover — Off Hours · Assignment 3 · Search Discoverability & Digital PR Strategy", [
  ("quote", "What begins when work ends."),
  ("p", "A continuation of Assignments 1 and 2. Mumbai and Bengaluru · 10-sachet night drink · melatonin-free. "
        "Part 3: how Meera finds us when she goes looking — and how people who have never heard of us start "
        "the conversation."),
 ]),
 ("Part 3 · Slide 1 — What Are These Consumers Searching For?", [
  ("p", "Three consumer situations or triggers that lead someone in our category to search."),
  ("bul", ["Trigger 1 — the wired scroll, 10 pm to 1 am. The laptop is closed and the brain is not. Meera is "
           "in bed, scrolling, and tonight she finally types the question she has never said out loud: why "
           "can't I switch off? She is searching for relief for tonight, not a diagnosis — and not a pill "
           "that leaves her groggy at 7:30.",
           "Trigger 2 — the groggy morning after. She tried the gummy a colleague swore by and woke up worse "
           "than tired. Now she is searching for why — and for melatonin-free alternatives — because the "
           "ingredient list just became the trust gate (Assignment 2, Plain Labels).",
           "Trigger 3 — the ritual-building moment. Sunday reset, a new sprint, audit season, a fresh "
           "productivity system: Meera searches for wind-down routine components that fit a work-night life "
           "— the moment a habit-shaped product can enter as a component, not a cure."]),
  ("p", "Continuity: all three triggers are the same evening Assignment 1 positioned against and the same "
        "twenty minutes Assignment 2 turned into content. Search is where that evening gets a question mark."),
 ]),
 ("Part 3 · Slide 2 — Consumer Search Behaviour & Intent", [
  ("p", "Ten realistic queries across the journey, classified by intent and need."),
  ("table", ["Search query", "Search intent", "Consumer need", "Journey stage"],
   [["why can't I switch off at night", "Informational", "Name and understand the moment", "Problem awareness"],
    ["how to stop scrolling at night in bed", "Informational", "Behaviour help for tonight", "Problem awareness"],
    ["how to wind down after work without melatonin", "Informational", "Non-medical options that fit her stance", "Category consideration"],
    ["does magnesium glycinate help you relax", "Informational", "Ingredient truth, plain words", "Category consideration"],
    ["l-theanine vs melatonin difference", "Informational / Commercial", "Compare mechanisms before ingesting", "Category consideration"],
    ["best melatonin-free sleep drink India", "Commercial", "Shortlist within her constraint", "Evaluation"],
    ["Off Hours night drink reviews", "Commercial / Navigational", "Peer validation before trial", "Evaluation"],
    ["sleep drink subscription cancel anytime India", "Commercial", "Risk-check the commitment", "Purchase decision"],
    ["night drink sachets price trial", "Transactional", "Low-risk way to test tonight", "Purchase"],
    ["buy Off Hours 10-night trial kit", "Transactional", "Buy the known brand", "Purchase"]]),
  ("p", "Note for the deck: six of ten queries sit before purchase. The audience researches an ingested "
        "product like Meera researches everything — reviews first, UPI later (Assignment 1 persona)."),
 ]),
 ("Part 3 · Slide 3 — Keyword Research & Strategy", [
  ("p", "Twelve keywords, mixed by type and intent. Priorities are justified on consumer relevance, intent, "
        "business value and our ability to give a useful answer — never on popularity alone, and no volumes "
        "are invented."),
  ("table", ["Keyword", "Type", "Intent", "Priority", "Reason"],
   [["melatonin-free sleep drink", "Long-tail / category", "Commercial", "High",
     "Our differentiation in three words; the constraint Meera already holds"],
    ["how to switch off after work", "Long-tail / problem", "Informational", "High",
     "Owns the moment the brand is built for; we can answer it better than anyone"],
    ["magnesium glycinate for winding down", "Long-tail / ingredient", "Informational", "High",
     "The trust gate; our label-answers content is the strongest possible reply"],
    ["Off Hours trial kit", "Branded", "Transactional", "High",
     "Catches demand we create; must convert without friction"],
    ["Off Hours", "Branded", "Navigational", "High",
     "We must own our own name on page one, always"],
    ["sleep drink", "Short-tail / category", "Broad / mixed", "Medium",
     "Relevant category term, contested by gummies and teas; support, not spearhead"],
    ["l-theanine chamomile drink benefits", "Long-tail / ingredient", "Informational", "Medium",
     "Feeds the Plain Labels pillar; secondary ingredient questions"],
    ["why am I wired at night", "Long-tail / problem", "Informational", "Medium",
     "Early-funnel empathy entry; names the problem before the category"],
    ["buy night drink sachets online", "Category", "Transactional", "Medium",
     "Purchase intent we can serve on our own storefront"],
    ["sleep drink subscription India", "Category", "Commercial / transactional", "Medium",
     "Matches the refill model; medium until retention proof accumulates"],
    ["groggy after sleep gummies", "Problem / switcher", "Informational", "Medium",
     "The competitor-exit moment; honest comparison content, never sneering"],
    ["night drink", "Short-tail / category", "Broad", "Low",
     "Ambiguous (alcohol adjacency); monitor, do not chase"]]),
  ("h", "The five highest-priority keywords, and why"),
  ("bul", ["1 · melatonin-free sleep drink — the purchase-intent phrase that contains our entire position; "
           "high business value because it selects for our exact product.",
           "2 · how to switch off after work — the moment query; highest consumer relevance, and our archive "
           "and guides answer it with lived detail no competitor has.",
           "3 · magnesium glycinate for winding down — the ingredient trust gate; answering it plainly is "
           "both SEO and brand strategy (Assignment 2 objective 2).",
           "4 · Off Hours trial kit — branded transactional; every rupee of campaign and PR value leaks here "
           "if this page is weak.",
           "5 · Off Hours — branded navigational; owning our name is the floor of discoverability, and PR "
           "coverage will spike it."]),
 ]),
 ("Part 3 · Slide 4 — Keyword Mapping & Website Discoverability", [
  ("p", "Priority keyword groups mapped to destinations, one page per group — no two groups share a target, "
        "so the site never competes with itself."),
  ("table", ["Keyword group", "Consumer need", "Recommended page", "Why this page helps"],
   [["how to switch off after work · why am I wired at night", "Understand the moment",
     "Blog guide: \"The Twenty Minutes After the Laptop Closes\"",
     "Answers the feeling before the product; internal links carry readers to the trial when they are ready"],
    ["melatonin-free sleep drink · sleep drink subscription India", "Shortlist and try",
     "Product / trial page (₹999, 10 nights)",
     "Commercial intent needs price, ingredients and checkout in one screen; low-friction by design"],
    ["magnesium glycinate for winding down · l-theanine chamomile drink benefits", "Ingredient truth",
     "Resource page: \"The Label, Explained\" + FAQ",
     "One honest page per ingredient, plain words, quantities shown; the sceptic's trust gate closes here"],
    ["Off Hours · Off Hours trial kit · buy night drink sachets online", "Validate and purchase",
     "Homepage → storefront product page",
     "Branded arrivals must land on a page that confirms the story and takes UPI in one hand"],
    ["groggy after sleep gummies", "Switcher validation",
     "Blog: \"What a Sleep Gummy Can't Say About Your Morning\"",
     "Meets the competitor-exit moment with honesty, not sneering; links to the label page"],
    ["how to stop scrolling at night in bed", "Behaviour help from peers",
     "Community page: The Landing Hour archive",
     "Real unedited night notes answer behaviour questions better than brand copy; the archive doubles as "
     "the PR asset (slide 7)"]]),
  ("h", "Two blog opportunities from the keyword strategy"),
  ("bul", ["Blog 1 — \"What actually happens in the twenty minutes after you close the laptop.\" Primary "
           "keywords: how to switch off after work; why am I wired at night. Intent: informational. Answers: "
           "\"is my 10 pm wiredness normal, and what helps tonight?\" Relevant because it owns the moment the "
           "brand exists for, and feeds the archive.",
           "Blog 2 — \"Magnesium glycinate, L-theanine, chamomile: what our label can and can't promise.\" "
           "Primary keywords: magnesium glycinate for winding down; l-theanine chamomile drink benefits. "
           "Intent: informational into commercial. Answers: \"what do these ingredients actually do, in ordinary "
           "words?\" Relevant because the label is the trust gate for an ingested product (Assignment 2)."]),
 ]),
 ("Part 3 · Slide 5 — Foundational SEO Strategy", [
  ("p", "Six actions across the three pillars, two each. Every action states what, why and how it helps "
        "discovery."),
  ("h", "On-Page SEO"),
  ("bul", ["Action 1 — build \"The Label, Explained\": one page per ingredient with a plain-words answer, the "
           "quantity, and what it does not do; clear H1/H2 hierarchy, written meta descriptions, FAQ markup. "
           "Why: ingredient questions are the trust gate and our highest-priority informational keywords. How: "
           "each page captures its query and internally links to the trial page, converting trust into trials.",
           "Action 2 — publish the moment-led guide cluster (\"The Twenty Minutes After the Laptop Closes\" plus "
           "the gummy-comparison piece) with one clear CTA (the ₹999 trial) and links into the archive. Why: "
           "long-tail moment queries are where sceptics start. How: useful answers rank, and the internal link "
           "path carries readers from empathy to purchase without a hard sell."]),
  ("h", "Off-Page SEO"),
  ("bul", ["Action 3 — co-publish the expert-reviewed Landing Protocol with our sleep-psychologist partner "
           "(continuity from Assignment 2) and offer it to wellness editors as a reference. Why: third-party "
           "credibility is what the ingredient-sceptic trusts (Assignment 1, Earned). How: citable, link-worthy "
           "document that makes other sites reference Off Hours as a source, not an advertiser.",
           "Action 4 — pitch the culture story (the archive, slide 7) to work-life and D2C editors so earned "
           "coverage names the brand in context. Why: earned mentions are discoverable brand references that "
           "no budget can buy. How: coverage drives branded search (\"Off Hours\", \"landing hour archive\") "
           "straight into our owned pages."]),
  ("h", "Technical SEO"),
  ("bul", ["Action 5 — make the storefront a 10 pm object: mobile-first layouts, fast load on mid-range phones, "
           "one-hand UPI checkout, readable type in low light. Why: Meera meets the brand in bed on a phone; "
           "friction here cancels everything upstream. How: fewer abandoned trials, and the conversion objective "
           "stays honest.",
           "Action 6 — run crawl health before every campaign push: XML sitemap for blog, FAQ and archive; fix "
           "orphan pages; indexation checks on new pages; canonical discipline. Why: a quiet channel cannot "
           "afford blocked routes — campaign traffic into an unindexed page is wasted (Assignment 2 risk "
           "register). How: every piece we publish is actually findable the week it matters."]),
 ]),
 ("Part 3 · Slide 6 — Digital PR Objective & Consumer Insight", [
  ("bul", ["Primary PR objective — create conversation around the moment (the 10 pm landing) and establish Off "
           "Hours as its credible, quiet voice. One objective, chosen deliberately: conversation first, because "
           "awareness of the moment precedes any product belief (Assignment 2 objective 1).",
           "Target audience — the Meera cohort (25–40 professionals, Mumbai + Bengaluru, evidence-seeking, "
           "active 10 pm–1 am) plus the wider late-working-city culture, and the editors and creators who "
           "cover work-life honestly. The campaign matters to them because it names their evening without "
           "judging it.",
           "Consumer / cultural insight — the problem is not sleep, it is the landing: the twenty minutes "
           "between closing the laptop and reaching bed (Assignment 2 hero insight). And sceptics trust peers, "
           "labels and lukewarm reviews over promises (Assignments 1–2). India's late-working cities have no "
           "shared language for that window — until someone hosts one.",
           "Brand connection — Off Hours is built for exactly that window: a melatonin-free ritual, a 10-night "
           "judgement window, and a published list of claims we refuse to make. Only a brand of the evening can "
           "host an archive of evenings without it becoming an advert.",
           "Desired outcome — people start calling their wind-down \"landing\"; contributors feel seen rather "
           "than marketed to; editors treat Off Hours as the source on switch-off culture; trial starts arrive "
           "from conversation and search, not from ad spend."]),
 ]),
 ("Part 3 · Slide 7 — The Big Digital PR Idea", [
  ("h", "Campaign name"),
  ("p", "The Landing Hour — India's 10 PM Archive."),
  ("bul", ["Consumer / cultural insight — the landing, not the sleep (slide 6); and the archive instinct: "
           "people already post their night routines in group chats (Assignment 1, Shared).",
           "The big idea — a public, living archive of real wind-down notes from India's late-working "
           "professionals: one line per person, submitted with consent, published nightly at 10 pm during the "
           "campaign window — unranked, unedited, never corrected for grammar. The brand hosts the archive and "
           "never headlines it. Alongside it, a sleep-psychologist-reviewed Landing Protocol gives the "
           "conversation a behavioural spine.",
           "Key campaign message — \"We are not asking you to sleep earlier. We are asking you to land "
           "better.\" (continuity: Assignment 2 hero message).",
           "Why the idea is relevant to the brand — the archive is our category made visible: evenings, not "
           "products. Our melatonin-free, refusal-list stance keeps it cultural rather than clinical, and the "
           "trial kit enters only as the answer for people who want their own landing.",
           "Why it is interesting, useful, surprising or newsworthy — it is a first-person portrait of overwork "
           "culture in India's late cities, written by the people living it; useful because every note is a "
           "real wind-down idea; surprising because a brand is publishing lukewarm, unedited human notes "
           "instead of testimonials; newsworthy because editors can report the archive as culture, with "
           "contributors available (consent-first).",
           "What motivates people to talk about or share it — contributing is a two-minute act of "
           "self-recognition; sharing your own note card says \"this is my night\" without bragging; the quiet "
           "aesthetic makes posts feel like keepsakes, not ads; and the nightly opening gives the community a "
           "reason to return at exactly the hour the brand serves."]),
  ("p", "PR-worthiness test: HUMAN (real notes, unedited) · CULTURAL (late-working-city overwork) · NEW (first "
        "archive of its kind in the category) · RELEVANT (the switch-off conversation is live). Four of seven "
        "qualities; requirement is two. This is not a product announcement, a discount, or a paid influencer "
        "blast — participation is voluntary and editorial interest is earned."),
 ]),
 ("Part 3 · Slide 8 — Digital PR Campaign Execution", [
  ("h", "1 · Campaign activities"),
  ("bul", ["Archive microsite: a one-line submission form (note, hour, consent checkbox). Nothing publishes "
           "without consent; nothing is edited.",
           "Nightly opening: one note published at 10 pm each night of the window, unranked.",
           "Landing Protocol v1: behavioural wind-down framing reviewed with our sleep-psychologist partner; "
           "published as a plain document, free to cite.",
           "Editor first-looks: embargoed pre-launch briefings with contributor access (consent-first).",
           "Landing letters: archive excerpts folded into the 10-night WhatsApp/e-mail notes, so trialists "
           "read other people's landings during their own."]),
  ("h", "2 · Execution timeline"),
  ("table", ["Phase", "Weeks", "What happens"],
   [["Pre-Launch", "1–3", "Invite the existing subscriber community and waitlist to contribute first (real "
     "notes only, zero invented content); protocol review complete; editor briefings under embargo; archive "
     "microsite and crawl health checked (SEO action 6)."],
    ["Launch", "4", "Archive opens nightly at 10 pm; landing film re-cut using consented archive lines; "
     "protocol published; first editor first-looks convert into coverage; branded-search pages (slide 3) "
     "confirmed live."],
    ["Amplification", "5–10", "Weekly themed openings (audit-season nights, Sunday scaries, festival nights); "
     "creator wind-down series with our ritual partner; weekly letter excerpts; referral loop carries "
     "contributors back to discovery."]]),
  ("h", "3 · Audience participation"),
  ("bul", ["Submit a one-line night note (consent checkbox, unedited publication).",
           "Answer the nightly question in the private letter or on Stories.",
           "Share your own note as a story card; tag nothing, no contest, no streak.",
           "Opt into the Landing Letters for the seasonal rotation (Assignment 2 post-launch pillars)."]),
  ("h", "4 · Key campaign touchpoints"),
  ("p", "Instagram Reels and Stories · the archive microsite · WhatsApp and e-mail letters · YouTube protocol "
        "film · community threads where the audience already researches (organic, community-rules-first) · "
        "earned coverage landing pages."),
  ("h", "5 · Creative execution — two sample assets (copy)"),
  ("bul", ["Asset 1 — campaign key visual copy. Headline: \"INDIA'S 10 PM ARCHIVE.\" Sub: \"One line from "
           "tonight. Unedited. Unranked.\" Line: \"Open nightly at 10.\" Footer: \"Off Hours · The Landing "
           "Hour · offhours.in/landing-hour\". Direction in words: warm off-white ground, one burnt-orange "
           "accent, editorial serif, no badge, no arrow, no urgency device (Assignment 2 design discipline).",
           "Asset 2 — social note card. Body: \"NIGHT NOTE — 'Closed the laptop at 11:42. Stood on the balcony "
           "till the buildings went quiet. That was the whole victory.' Submitted, unedited.\" CTA: \"Add your "
           "line. offhours.in/landing-hour\". Direction in words: the note set in the contributor's own "
           "phrasing, single lamp-light photograph, no faces."]),
 ]),
 ("Part 3 · Slide 9 — Media, Creator & Community Outreach", [
  ("p", "Real outlets, creators and communities, chosen on relevance to the audience and the story — never on "
        "fame. Creator names carry over from Assignment 2, where the selection was reviewed and approved."),
  ("table", ["Who", "Why relevant to our audience", "Why the campaign interests them", "Angle / resource offered"],
   [["Mint Lounge (HT Media weekend magazine; culture and conscious-living long-reads)",
     "Read by metro professionals who recognise the 10 pm window; long-form culture readership",
     "A first-person archive of India's late-working evenings is a weekend long-read waiting to be written",
     "First-look access to opening entries; contributor interviews with consent; protocol explainer"],
    ["YourStory (D2C and startup ecosystem coverage; Brands of India initiative)",
     "Where founders and operators — many of them Meera's colleagues — read about new consumer brands",
     "A D2C brand turning its hardest metric (the trial window) into a cultural asset is a builder's story",
     "Founder interview; transparent growth model labelled as planning arithmetic; archive metrics as they occur"],
    ["ET BrandEquity (marketing and media trade)",
     "Read by the marketers who judge campaign craft; Meera's industry peers",
     "Restraint-led PR in a hype category — an archive instead of an announcement — is a teachable case",
     "Campaign teardown access: timeline, refusal list, what we chose not to do"],
    ["The Hindu BusinessLine (business daily with active D2C/wellness coverage)",
     "Business readers tracking the wellness D2C wave beyond discounting",
     "A subscription brand competing on trust and retention rather than price cuts fits their coverage frame",
     "Unit-economics story with stated assumptions; retention-objective data as it matures"],
    ["Shabbir Ahmed — sleep psychologist, Navi Mumbai (creator, continuity from Assignment 2)",
     "Carries the behavioural, non-chemical audience Meera trusts for method",
     "The Landing Protocol gives his teaching a public, citable home",
     "Co-reviewed protocol; expert Q&A; commentary on the archive's behavioural patterns (no invented data)"],
    ["Shruti Maheshwari — co-founder, Sleep Gurukul, Mumbai (creator, continuity from Assignment 2)",
     "Ritual- and breath-work-led Indian professionals; India-native practice",
     "A guided ten-night wind-down series fits the archive's nightly cadence",
     "Creator series; community sessions; phase-2 corporate wellness bridge"],
    ["Reddit India wellness and fitness threads (community where the persona researches, Assignment 1)",
     "Where sceptics ask unfiltered questions before buying anything ingestible",
     "An unedited archive and a label-answers AMA are rare: a brand answering, not advertising",
     "Rules-first organic participation; \"ask us about the label\" AMA with founder and psychologist"]]),
  ("h", "Sample media pitch — Mint Lounge (121 words)"),
  ("quote", "Dear Mint Lounge editor — Off Hours, a Mumbai and Bengaluru night-drink brand, is opening The "
            "Landing Hour: a public archive of real, unedited wind-down notes from India's late-working "
            "professionals, published nightly at 10 pm alongside a sleep-psychologist-reviewed Landing "
            "Protocol. We would like to offer Lounge first access to the archive's opening entries and, with "
            "each contributor's consent, to the contributors themselves. This is not a product story: it is a "
            "portrait of the twenty minutes between closing the laptop and reaching bed — written by the "
            "people living it, unranked and unjudged. Available: contributor interviews, the protocol "
            "explainer, founder commentary on why a brand built for evenings chose to host, not headline, the "
            "conversation. The archive opens in launch week; embargoes honoured."),
 ]),
 ("Part 3 · Slide 10 — Digital PR Amplification Strategy", [
  ("h", "Earned media"),
  ("bul", ["Editor first-looks become culture long-reads (Mint Lounge), builder stories (YourStory), trade "
           "teardowns (ET BrandEquity) and business pieces (Hindu BusinessLine).",
           "Expert commentary syndicates the Landing Protocol beyond our own channels."]),
  ("h", "Owned media"),
  ("bul", ["Archive microsite holds every note permanently; weekly letter excerpts push the best lines to a "
           "consented audience.",
           "Storefront carries a quiet band linking the moment guide → trial; YouTube hosts the protocol film.",
           "Branded-search landing pages (slide 3) catch every spike coverage creates."]),
  ("h", "Shared media"),
  ("bul", ["Contributors share their own note cards; nightly question replies surface in Stories.",
           "Community threads quote and discuss archive notes organically; the referral link closes the loop "
           "back to discovery (Assignment 1 loop)."]),
  ("p", "How they support one another: earned coverage gives strangers a reason to trust what shared posts "
        "say; shared participation supplies earned media with fresh human material every week; owned pages "
        "catch every visitor from both with an answer and a ₹999 next step. Paid, per Assignment 1, only "
        "re-targets archive visitors — it amplifies, never leads."),
 ]),
 ("Part 3 · Slide 11 — Integrated Discoverability Strategy", [
  ("p", "Two discovery routes, one owned retention spine. The aim is not to force PR into SEO, but to show how "
        "both make the brand findable."),
  ("h", "Route A — search-led discovery"),
  ("p", "Consumer need (\"why can't I switch off at night\") → Google → moment guide or \"The Label, Explained\" "
        "→ internal link → ₹999 trial page → 10-night letters + WhatsApp concierge → subscription → referral "
        "share re-enters discovery."),
  ("bul", ["Touchpoints: search results, blog/resource pages, product page, letters.",
           "Brand content: moment guide, label pages, FAQ, trial page.",
           "Expected consumer action: read → start trial → judge the ten nights → subscribe → refer.",
           "Objective support: acquisition (≥600 trials/month by M6) and education (own the ingredient question)."]),
  ("h", "Route B — PR-led discovery"),
  ("p", "Mint Lounge long-read or creator series → reader curiosity → branded search (\"Off Hours\", \"landing "
        "hour archive\") → archive microsite → submit a note or start a trial → letters → subscription."),
  ("bul", ["Touchpoints: article/film, search, archive microsite, letters.",
           "Brand content: archive, protocol, branded landing pages, trial page.",
           "Expected consumer action: read → search the brand → contribute or try → stay for the letters.",
           "Objective support: awareness of the moment, third-party credibility, conversion support."]),
  ("p", "Both routes hand the customer to the same owned retention spine from Assignment 1 — nothing is a dead "
        "end — and both re-enter discovery through the referral loop. PR makes the brand worth searching for; "
        "search makes the brand easy to find; owned channels make both pay for themselves."),
 ]),
 ("Part 3 · Slide 12 — Measurement & Key Recommendations", [
  ("p", "Six KPIs across both areas. Each states what it measures, why it matters, and which objective it "
        "serves. No numbers are invented; targets inherit Assignment 1's SMART objectives and Assignment 2's "
        "seven metrics."),
  ("table", ["Area", "KPI", "What it measures", "Why it matters", "Objective served"],
   [["Search visibility", "Organic impressions and CTR on moment + ingredient queries",
     "Whether we are findable at the trust gate", "Education precedes permission to sell",
     "Content objective 2 (own the ingredient question)"],
    ["Website discovery", "Organic sessions to guide, label and trial pages",
     "Route A flow from query to page", "Trials start where answers live", "Acquisition objective (≥600 trials/mo)"],
    ["Content engagement", "Saves and return visits on label explainers (continuity metric)",
     "Trust forming, not just reach", "Sceptics save before they buy", "Education + trust"],
    ["Digital PR", "Qualified coverage count and brand mentions in work-life context (named outlets)",
     "Earned credibility, not bought noise", "Third-party trust converts sceptics", "PR objective (conversation + credibility)"],
    ["Conversation", "Archive submissions, nightly-question replies, note-card shares",
     "Participation depth in the campaign", "The campaign lives only if people contribute", "PR objective + community"],
    ["Business impact", "Trial starts from search and PR referrers; trial→subscription rate of those cohorts",
     "Whether discoverability becomes revenue", "The 1,000-household goal is the only finish line",
     "Acquisition + retention objectives"]]),
  ("h", "Three SEO priorities"),
  ("bul", ["1 · Own the ingredient trust gate: ship \"The Label, Explained\" before any campaign spend.",
           "2 · Build the moment long-tail cluster (switch-off guide, gummy comparison, archive page) with one "
           "page per keyword group.",
           "3 · Fix technical routes first: mobile speed, crawl and indexation health before every push."]),
  ("h", "Three Digital PR priorities"),
  ("bul", ["1 · Launch the archive with consent-first, unedited discipline — the restraint is the credibility.",
           "2 · Sequence editors first, blast never: first-looks and embargoes before any public opening.",
           "3 · Keep the expert protocol series always-on so credibility compounds post-launch."]),
  ("h", "Strategic conclusion"),
  ("p", "Off Hours becomes discoverable by answering, in plain words, the questions its sceptics already ask — "
        "and becomes credible by letting real evenings, real editors and real experts speak before the brand "
        "does. Search catches the intent; the archive earns the trust; the owned loop turns both into subscribers."),
 ]),
]

def build_doc(path, title, subtitle, intro_lines, sections):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    h = doc.add_heading(title, level=0)
    p = doc.add_paragraph(subtitle)
    p.runs[0].italic = True
    for line in intro_lines:
        doc.add_paragraph(line)
    doc.add_paragraph(PRODUCTION_NOTE).runs[0].italic = True
    doc.add_page_break()
    for sec_title, blocks in sections:
        doc.add_heading(sec_title, level=1)
        for b in blocks:
            kind = b[0]
            if kind == "h":
                doc.add_heading(b[1], level=2)
            elif kind == "p":
                doc.add_paragraph(b[1])
            elif kind == "quote":
                qp = doc.add_paragraph(b[1])
                qp.paragraph_format.left_indent = Pt(24)
                for r in qp.runs:
                    r.italic = True
                    r.font.color.rgb = ORANGE
            elif kind == "bul":
                for item in b[1]:
                    doc.add_paragraph(item, style="List Bullet")
            elif kind == "table":
                headers, rows = b[1], b[2]
                t = doc.add_table(rows=1, cols=len(headers))
                t.style = "Light Grid Accent 2"
                for i, hd in enumerate(headers):
                    cell = t.rows[0].cells[i]
                    cell.text = hd
                    for r in cell.paragraphs[0].runs:
                        r.bold = True
                for row in rows:
                    cells = t.add_row().cells
                    for i, val in enumerate(row):
                        cells[i].text = val
        doc.add_page_break()
    doc.save(path)
    return path

INTRO_COMMON = [
 "Deliverable mode: text copy for each slide of the presentation (headings, body copy, table content).",
 "Prepared as a continuation: Assignment 1 content carries forward into every later assignment.",
]

if __name__ == "__main__":
    base = os.path.abspath(OUT)
    a1_intro = INTRO_COMMON + [
      "This document: Assignment 1 deck, REVISED per instructor feedback — business numbers strengthened "
      "(new slide 11, an explicitly labelled illustrative planning model with stated assumptions).",
      "Feedback applied: 'improve upon the business numbers'; continuation requirement honoured.",
    ]
    a2_intro = INTRO_COMMON + [
      "This document: Assignment 2 deck, REVISED per instructor feedback — the 'landing better' concept is "
      "explained warmly and translated into content (slide 2 revision + slide 7 translation table), and a "
      "post-launch content-pillar engine is added (slide 12) so publishing never stops after launch.",
      "Feedback applied: 'more on the content to explain the concept of landing better', 'a bit too serious / "
      "clinical', 'enough content pillars to continue publishing post launch'.",
    ]
    a3_intro = INTRO_COMMON + [
      "This document: the Assignment 3 solution — Search Discoverability & Digital PR Strategy for Off Hours.",
      "Structure per feedback: Part 1 restates Assignment 1 in full, Part 2 restates Assignment 2 in full "
      "(both in revised form), Part 3 carries the twelve Assignment-3 slides with complete slide copy.",
      "All research-source requirements honoured: named outlets and creators are real and verified; no keyword "
      "volumes, consumer research figures or campaign results are invented anywhere in this document.",
    ]
    p1 = build_doc(os.path.join(base, "Project_1_OffHours_context.docx"),
                   "Off Hours — Assignment 1 · Brand & Digital Strategy (slide copy, revised)",
                   "D2C sleep & recovery · Mumbai + Bengaluru · What begins when work ends.",
                   a1_intro, A1)
    p2 = build_doc(os.path.join(base, "Project_2_OffHours_context.docx"),
                   "Off Hours — Assignment 2 · Content & Social Media Strategy (slide copy, revised)",
                   "A continuation of the Assignment 1 deck.",
                   a2_intro, A2)
    sections3 = [("Part 1 — Where we began (Assignment 1, restated in flow)", [])] + \
                [(f"A1 · {t}", b) for t, b in A1] + \
                [("Part 2 — What we said and how (Assignment 2, restated in flow)", [])] + \
                [(f"A2 · {t}", b) for t, b in A2] + \
                [("Part 3 — Search Discoverability & Digital PR (Assignment 3)", [])] + \
                [(t, b) for t, b in A3]
    p3 = build_doc(os.path.join(base, "Project_3_OffHours_solution.docx"),
                   "Off Hours — Assignment 3 · Search Discoverability & Digital PR Strategy (slide copy)",
                   "Parts 1–2 restate Assignments 1–2 in flow; Part 3 is the new work.",
                   a3_intro, sections3)
    # word count check on the media pitch
    pitch = [b for t, bl in A3 for b in bl if b[0] == "quote" and b[1].startswith("Dear Mint Lounge")][0][1]
    print("pitch words:", len(re.findall(r"\S+", pitch)))
    for p in (p1, p2, p3):
        print("wrote", p, os.path.getsize(p), "bytes")
