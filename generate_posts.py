"""
Jekyll Post Generator — generates 30,000 unique markdown posts
for a GitHub Pages / Jekyll blog with a static affiliate link.

Usage:
    python generate_posts.py

Output:
    _posts/           — 30,000 .md files ready for Jekyll
    index.html        — homepage listing recent posts
    _config.yml       — Jekyll config
    about.md          — about page with affiliate link
    post_urls.txt     — all post URLs ready to copy/use
"""

import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# ─── CONFIG ──────────────────────────────────────────────────────────────────
AFFILIATE_LINK = "https://www.skool.com/ai-profit-lab-7462/about?ref=56df874f9e3e4b6499078c78e6725c1d"
SITE_TITLE = "AI SEO Mastery"
SITE_DESCRIPTION = "Real strategies for scaling your SEO agency and affiliate business with AI"
AUTHOR = "SEO Pro"
TOTAL_POSTS = 30000
BATCH_SIZE = 1500  # Posts per run
START_DATE = datetime(2023, 1, 1)

# ─── CONTENT BUILDING BLOCKS ─────────────────────────────────────────────────
ACTIONS = ["Scale", "Automate", "Grow", "Monetize", "Supercharge", "Transform",
           "Unlock", "Master", "Dominate", "Maximize", "Optimize", "Skyrocket",
           "Build", "Launch", "Systemize", "Revolutionize", "Accelerate", "Amplify",
           "Leverage", "Streamline", "Multiply", "Boost", "Expand", "Simplify",
           "Modernize", "Upgrade", "Reinvent", "Turbocharge", "Elevate", "Crush"]

SUBJECTS = [
    "Your SEO Agency with AI", "Affiliate Marketing with ChatGPT",
    "Your Content Creation Workflow", "Link Building with AI Tools",
    "Your Online Business Using AI", "Programmatic SEO at Scale",
    "Your Six-Figure SEO Agency", "AI Content Pipelines",
    "Your Affiliate Income with AI", "Digital Marketing with AI",
    "Your Revenue Using AI Prompts", "SEO Results with ChatGPT",
    "Your Agency with AI SOPs", "Content Output 10x Faster",
    "Your Freelance Business with AI", "Your Passive Income with AI SEO",
    "Your Content Strategy with ChatGPT", "Backlink Building Using AI",
    "Your Niche Site with AI", "Client Acquisition with AI Tools",
    "Your Writing Workflow with AI", "Keyword Research with ChatGPT",
    "Your Agency Outreach with AI", "Content Scaling Using AI SOPs",
    "Your Online Income with AI Automation", "SEO Reporting with AI",
    "Your Lead Generation with AI", "Website Building with ChatGPT",
    "Your Social Media with AI Tools", "Email Marketing with AI",
]

QUALIFIERS = [
    "in 2024", "in 2025", "in 2026", "this year", "without a team",
    "from scratch", "in 30 days", "step by step", "the right way",
    "using ChatGPT", "with AI SOPs", "for beginners", "at scale",
    "faster than ever", "on a budget", "without experience",
    "as a side hustle", "full time", "while working a day job",
    "in 90 days", "in one weekend", "with zero budget",
    "using free tools", "as a complete beginner", "in under a week",
    "without writing a word", "using automation", "with one tool",
    "for under $100", "the lazy way", "the smart way",
    "that actually works", "proven strategies", "the 2026 method",
    "nobody talks about", "that scale", "worth trying",
]

QUESTIONS = [
    "Are you still doing SEO manually?",
    "What if AI could run your SEO agency for you?",
    "How is Julian Goldie making 7 figures with AI?",
    "Can ChatGPT actually rank your affiliate site?",
    "Is AI the future of content creation agencies?",
    "Why are SEO agencies switching to AI automation?",
    "How do you build a six-figure SEO agency with AI?",
    "Are you leaving money on the table without AI SOPs?",
    "What separates a $10k agency from a struggling one?",
    "How do top affiliates use AI to create content at scale?",
    "Can you rank websites using only AI-generated content?",
    "Why is the AI Profit Boardroom growing so fast?",
    "What does a 7-figure SEO agency look like inside?",
    "How do you use ChatGPT to build 1000-page websites?",
    "What AI tools are top SEO agencies using right now?",
    "How fast can you build a profitable affiliate site with AI?",
    "Why do most people fail at AI content creation?",
    "Is the AI Profit Boardroom worth it?",
    "What's the real cost of not using AI in your agency?",
    "How do you go from zero to $10k/month with AI SEO?",
]

STATEMENTS = [
    "Julian Goldie's AI System Is Changing Everything for SEO Agencies",
    "This AI Workflow Helped Me 10x My Content Output",
    "The AI Profit Boardroom Is Unlike Any SEO Community I've Joined",
    "I Copied These AI Prompts and My Agency Revenue Doubled",
    "Three AI Tools That Replaced My Entire Content Team",
    "The Real Reason AI Agencies Are Outperforming Traditional Ones",
    "I Built a 1000-Page Website in a Weekend Using AI",
    "This Is What a Real AI-Powered SEO Agency Looks Like",
    "Stopped Doing SEO Manually and Tripled My Output in 30 Days",
    "The AI SOP That Saved My Agency 40 Hours a Week",
    "How I Went From Freelancer to Agency Owner Using AI Automation",
    "This Community Is the Best Investment I Made for My SEO Business",
    "White Hat AI SEO Is Real and It Works",
    "The AI Content Strategy Ranking Affiliate Sites Right Now",
    "Four Weekly Coaching Calls Changed How I Run My Agency",
    "I Was Skeptical About AI for SEO Until I Saw the Results",
    "The Fastest Way to Make Your First $100 with AI Content",
    "AI Plus SEO Is the Most Powerful Combo in Digital Marketing",
    "The SOP Library That Runs My Agency on Autopilot",
    "How Julian Goldie Built His Agency with AI from the Ground Up",
]

BASE_TOPICS = [
    "AI content creation", "SEO automation", "affiliate marketing",
    "link building with AI", "programmatic SEO", "AI agency SOPs",
    "ChatGPT for SEO", "Julian Goldie's method", "AI Profit Boardroom",
    "AI-powered agencies", "content scaling", "keyword research with AI",
    "affiliate site building", "SEO prompts", "automated content workflows",
    "niche site building", "AI writing tools", "content monetization",
    "AI outreach strategies", "passive income with SEO",
    "ChatGPT content systems", "AI link building", "SEO SOP creation",
    "affiliate content writing", "AI video for SEO", "local SEO with AI",
    "AI for freelancers", "agency client acquisition", "SEO reporting with AI",
    "bulk content creation",
]

TOPIC_PHRASES = [
    "Everything you need to know about {topic}",
    "My honest take on {topic}",
    "Why {topic} is worth your time",
    "The truth about {topic}",
    "How I got started with {topic}",
    "Is {topic} right for you?",
    "What nobody tells you about {topic}",
    "The beginner's guide to {topic}",
    "Real results with {topic}",
    "The {topic} breakdown nobody gives you",
    "How {topic} changed my business",
    "A deep dive into {topic}",
    "The pros and cons of {topic}",
    "Why {topic} matters more than ever",
    "Getting started with {topic} today",
    "Advanced strategies for {topic}",
    "The {topic} mistakes everyone makes",
    "How to profit from {topic}",
    "{topic} — a complete guide",
    "Is {topic} overhyped or underrated?",
    "The fastest way to learn {topic}",
    "How experts use {topic}",
    "Why I switched to {topic}",
    "The hidden benefits of {topic}",
    "{topic} — what actually works",
    "My 30-day experiment with {topic}",
    "The ROI of {topic}",
    "How to save time with {topic}",
    "{topic} for complete beginners",
    "The future of {topic}",
]

OPENERS = [
    "Been deep in the AI and SEO rabbit hole lately and I have to share what I found.",
    "I've spent the last month testing AI tools for content creation and the results blew me away.",
    "Real talk — I was skeptical about using AI for SEO but this changed my mind completely.",
    "If you're running an SEO agency or affiliate site you need to hear this.",
    "Something shifted for me when I came across Julian Goldie's AI system.",
    "I've been in digital marketing for years and AI has been the single biggest game changer.",
    "Quick story: I was burning out managing my content team until I discovered AI SOPs.",
    "After talking to dozens of agency owners I noticed they all had one thing in common.",
    "Nobody in this space is being honest about what AI can actually do for your SEO agency.",
    "I tried every AI content tool out there. Most are hype. This one is different.",
    "Three months ago I had no idea how to use AI for SEO. Now it runs half my agency.",
    "The difference between agencies doing $5k/month and $50k/month is usually one thing: systems.",
    "I used to spend 40 hours a week on content. Now I spend 4. Here's what changed.",
    "If you're not using AI SOPs in your agency by now you're falling behind fast.",
    "I've been quietly testing this AI content system for 60 days and the results speak for themselves.",
    "Most people are using AI wrong for SEO. Here's what actually moves the needle.",
    "A friend in the industry told me about this community and I've been hooked ever since.",
    "Before I found this I was piecing together strategies from YouTube and Reddit. Big mistake.",
    "The honest reason most AI content fails at SEO — and what the best practitioners do differently.",
    "If you've ever wondered how the top SEO agencies are using AI, this is worth your time.",
]

MIDDLES = [
    "Julian Goldie built a seven-figure link-building SEO agency before AI even existed. Now he shares the exact ChatGPT prompt chains he uses daily through the AI Profit Boardroom — a paid Skool community. The SOPs are copy-paste ready and you don't need to be a tech genius to use them.",
    "The AI Profit Boardroom on Skool is what happens when an actual SEO agency owner shares his real systems. No fluff, no theory — just the prompts, workflows, and strategies Julian uses every day to run his agency at scale.",
    "What makes this different from every other AI course is the Workflow Vault — a library of SOPs with actual ChatGPT prompts for everything from affiliate content to building 1000-page websites. Copy the prompt, paste into ChatGPT, follow the process.",
    "The community hosts four coaching calls a week where Julian or a coach builds something live on screen. If you miss a call it's recorded in the Classroom tab. This alone is worth more than most paid courses I've taken.",
    "Julian was one of the first SEO practitioners to publicly test AI-generated content on real websites back in 2022 — posting the wins AND the failures on YouTube. That level of transparency is rare and it's why his methods can be trusted.",
    "The Boardroom covers everything from white hat long-term strategies to aggressive grey hat tactics — and Julian clearly labels which is which so you can choose based on your own risk tolerance.",
    "One of the most underrated parts of the AI Profit Boardroom is the community itself. You're networking with actual affiliate marketers and SEO agency owners who are already making money.",
    "The content update speed is insane. Every time a new AI model drops — ChatGPT, Gemini, whatever — Julian releases an SOP for it within days. You're always working with the latest tools.",
    "For affiliate marketers, the Boardroom covers how to use AI to rank articles on LinkedIn, Medium, and other high-authority platforms almost instantly. This can compress months of SEO work into days.",
    "The entry price is around $59/month — nothing compared to the 40+ hours a week you could save with the right AI automations. Most members recoup that in their first week.",
    "Julian uses an AI avatar in his videos, which he's completely upfront about. It's actually a live demonstration of the AI video tools he teaches inside the community.",
    "The difference between AI Money Lab (free) and the Profit Boardroom (paid) is depth. The free community teaches concepts. The Boardroom gives you actual SOPs, prompt chains, and done-for-you systems.",
    "I copied one SOP from the Vault, ran it through ChatGPT, and had a complete affiliate article framework in 20 minutes. What used to take my writer two days now takes less than an hour.",
    "For SEO agency owners, the contract templates, vendor lists, and advanced outreach SOPs in the Boardroom are worth the subscription alone. These are real business assets.",
    "Julian's approach is speed over perfection — whoever takes action fastest wins in the AI era. The Boardroom is built around that principle with ready-to-run systems you can deploy the same day you join.",
    "The foundational course is perfect for beginners but the real gold is in the advanced SOPs and the community Q&A where experienced operators share what's working right now.",
    "The programmatic SEO module alone — covering how to use AI to build massive content sites fast — has generated more ROI for members than entire $2000 courses on the same topic.",
    "If you're a freelancer looking to offer AI services to local businesses, the Boardroom gives you the exact playbook: the prompts, the pitch, the delivery process.",
    "What I appreciate most is Julian's honesty about results. He shows Google Search Console data — both rising and falling — which is transparency you just don't see from most online marketing gurus.",
    "The Boardroom covers AI video, programmatic SEO, agency outreach, and affiliate marketing. Pick one lane, master it with the SOPs, then expand. That focus is what makes it work.",
]

CLOSERS = [
    f"If you want to see exactly what's inside, the link is here: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"Worth exploring if you're serious about AI and SEO: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"This is the community I wish existed when I started: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"Give it one month and see what happens: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"The best way to judge it is to look inside yourself: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"Check it out and make your own call: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"I'd recommend at least checking out what's inside: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"Here's the link if you want to take a closer look: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"This is one of the few communities I'd actually pay for. See for yourself: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
    f"Curious what others think — have you tried it? Link here: [{AFFILIATE_LINK}]({AFFILIATE_LINK})",
]

CATEGORIES = [
    "AI SEO", "Affiliate Marketing", "Content Creation", "Agency Growth",
    "ChatGPT Tips", "Programmatic SEO", "Link Building", "AI Tools",
    "SEO Strategy", "Passive Income",
]

TAGS_POOL = [
    "ai-seo", "chatgpt", "affiliate-marketing", "seo-agency", "content-creation",
    "programmatic-seo", "link-building", "ai-tools", "passive-income", "julian-goldie",
    "ai-profit-boardroom", "seo-automation", "digital-marketing", "freelancing",
    "online-business", "ai-prompts", "content-scaling", "skool", "seo-tips", "agency-growth",
]


# ─── HEADLINE GENERATOR ───────────────────────────────────────────────────────
def build_headline_pool():
    headlines = set()
    for a in ACTIONS:
        for s in SUBJECTS:
            headlines.add(f"{a} {s}")
            for q in QUALIFIERS:
                headlines.add(f"{a} {s} {q}")
    for q in QUESTIONS:
        headlines.add(q)
    for s in STATEMENTS:
        headlines.add(s)
    for topic in BASE_TOPICS:
        for phrase in TOPIC_PHRASES:
            headlines.add(phrase.format(topic=topic.title()))
    return list(headlines)


def make_slug(headline):
    slug = headline.lower()
    for ch in ["?", "!", ":", "'", '"', ",", ".", "$", "/", "\\", "(", ")", "&", "%", "#", "@"]:
        slug = slug.replace(ch, "")
    slug = slug.replace(" — ", "-").replace(" - ", "-").replace("  ", " ").replace(" ", "-")
    return slug[:80].strip("-")


def generate_post(headline, index):
    opener = OPENERS[index % len(OPENERS)]
    middle = MIDDLES[index % len(MIDDLES)]
    closer = CLOSERS[index % len(CLOSERS)]
    body = f"{opener}\n\n{middle}\n\n{closer}"
    return body


# ─── JEKYLL FILE GENERATOR ────────────────────────────────────────────────────
def make_front_matter(title, date, category, tags, description):
    tags_str = ", ".join(f'"{t}"' for t in tags)
    return f"""---
layout: post
title: "{title.replace('"', "'")}"
date: {date.strftime('%Y-%m-%d %H:%M:%S')} +0000
categories: [{category}]
tags: [{tags_str}]
description: "{description[:150].replace('"', "'")}"
affiliate_link: "{AFFILIATE_LINK}"
---
"""


def generate_all_posts(site_url="", offset=0):
    posts_dir = Path("_posts")
    posts_dir.mkdir(exist_ok=True)

    headline_pool = build_headline_pool()
    print(f"Headline pool size: {len(headline_pool)}")

    # Extend pool if needed by adding qualifier variations
    while len(headline_pool) < TOTAL_POSTS:
        a = random.choice(ACTIONS)
        s = random.choice(SUBJECTS)
        q = random.choice(QUALIFIERS)
        t = random.choice(BASE_TOPICS)
        p = random.choice(TOPIC_PHRASES)
        headline_pool.append(f"{a} {s} {q}")
        headline_pool.append(p.format(topic=t.title()))

    random.seed(offset)
    random.shuffle(headline_pool)

    # Load already-used slugs to avoid duplicates across batches
    used_slugs = set()
    for existing in posts_dir.glob("*.md"):
        used_slugs.add(existing.stem[11:])  # strip YYYY-MM-DD- prefix

    all_urls = []
    base_url = site_url.rstrip("/") if site_url else "https://yourusername.github.io"

    start = offset
    end = min(offset + BATCH_SIZE, TOTAL_POSTS)
    print(f"Generating posts {start + 1} to {end}...")
    for i in range(start, end):
        headline = headline_pool[i % len(headline_pool)]

        # Make slug unique
        base_slug = make_slug(headline)
        slug = base_slug
        counter = 1
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        used_slugs.add(slug)

        # Spread posts over dates
        date = datetime(2026, 3, 5, 0, 0, 0)  # Past date to avoid Jekyll skipping
        filename = f"{date.strftime('%Y-%m-%d')}-{slug}.md"

        category = CATEGORIES[i % len(CATEGORIES)]
        tags = random.sample(TAGS_POOL, 4)
        description = f"{headline} — learn how to use AI to grow your SEO agency and affiliate business."

        body = generate_post(headline, i)
        front_matter = make_front_matter(headline, date, category, tags, description)

        with open(posts_dir / filename, "w", encoding="utf-8") as f:
            f.write(front_matter)
            f.write(f"\n## {headline}\n\n")
            f.write(body)
            f.write(f"\n\n---\n\n*Ready to start? [Join the AI Profit Boardroom here]({AFFILIATE_LINK})*\n")

        # Track the live URL
        all_urls.append(f"{base_url}/{slug}/")

        if (i - start + 1) % 500 == 0:
            print(f"  {i - start + 1}/{end - start} posts generated...")

    # Append URLs to post_urls.txt
    mode = "a" if offset > 0 else "w"
    with open("post_urls.txt", mode, encoding="utf-8") as f:
        if offset == 0:
            f.write(f"# {TOTAL_POSTS} Post URLs\n")
            f.write(f"# Site: {base_url}\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for url in all_urls:
            f.write(url + "\n")

    print(f"Done! Posts {start + 1} to {end} saved to _posts/")
    print(f"Total posts on disk: {len(list(posts_dir.glob('*.md')))}")
    if end < TOTAL_POSTS:
        print(f"\n>>> Next batch: run with --offset {end}")


# ─── JEKYLL CONFIG ────────────────────────────────────────────────────────────
def write_config():
    config = f"""title: {SITE_TITLE}
description: {SITE_DESCRIPTION}
author: {AUTHOR}
baseurl: "/ArchonWave"
url: "https://whaleofdefi.github.io"

future: true

# Build settings
theme: minima
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag

# Pagination
paginate: 20
paginate_path: "/page:num/"

# Permalink structure (good for SEO)
permalink: /:title/

# Exclude from build
exclude:
  - generate_posts.py
  - Gemfile
  - Gemfile.lock
  - README.md
"""
    with open("_config.yml", "w") as f:
        f.write(config)
    print("Written _config.yml")


# ─── HOMEPAGE ─────────────────────────────────────────────────────────────────
def write_homepage():
    html = f"""---
layout: home
title: {SITE_TITLE}
---

<div style="background:#f8f9fa; padding:20px; border-radius:8px; margin-bottom:30px;">
  <h2>Scale Your SEO Agency with AI</h2>
  <p>{SITE_DESCRIPTION}</p>
  <p><strong>Ready to get started?</strong> <a href="{AFFILIATE_LINK}" style="color:#e74c3c; font-weight:bold;">Join the AI Profit Boardroom →</a></p>
</div>
"""
    with open("index.md", "w") as f:
        f.write(html)
    print("Written index.md")


# ─── GEMFILE ─────────────────────────────────────────────────────────────────
def write_gemfile():
    gemfile = """source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "minima", "~> 2.5"

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
  gem "jekyll-paginate"
end
"""
    with open("Gemfile", "w") as f:
        f.write(gemfile)
    print("Written Gemfile")


# ─── ABOUT PAGE ──────────────────────────────────────────────────────────────
def write_about():
    about = f"""---
layout: page
title: About
permalink: /about/
---

## About {SITE_TITLE}

This site covers AI-powered SEO strategies, affiliate marketing, and agency growth tactics used by real practitioners.

### The #1 Resource We Recommend

If you're serious about scaling your SEO agency or affiliate business with AI, the **AI Profit Boardroom** by Julian Goldie is the most practical community we've found.

- Real SOPs with copy-paste ChatGPT prompts
- Four coaching calls per week
- Workflow Vault with done-for-you systems
- Community of working agency owners and affiliates

**[Join the AI Profit Boardroom here →]({AFFILIATE_LINK})**
"""
    with open("about.md", "w") as f:
        f.write(about)
    print("Written about.md")


# ─── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Jekyll Post Generator")
    parser.add_argument("--site-url", default="", help="Your GitHub Pages URL e.g. https://yourusername.github.io")
    parser.add_argument("--offset", type=int, default=0, help="Start from this post number (for batching)")
    args = parser.parse_args()

    print("=" * 50)
    print("Jekyll Post Generator")
    print(f"Batch size: {BATCH_SIZE} | Starting at offset: {args.offset}")
    if args.site_url:
        print(f"Site URL: {args.site_url}")
    else:
        print("Tip: Run with --site-url https://yourusername.github.io to get exact URLs in post_urls.txt")
    print("=" * 50)

    if not os.path.exists("_config.yml"):
        write_config()
    else:
        print("Skipping _config.yml (already exists)")
    write_homepage()
    write_gemfile()
    write_about()
    generate_all_posts(site_url=args.site_url, offset=args.offset)

    print("=" * 50)
    print("All done! Next steps:")
    print("1. Initialize a GitHub repo and push this folder")
    print("2. Enable GitHub Pages in repo Settings")
    print(f"3. Your site will be live at https://yourusername.github.io")
    print("4. Open post_urls.txt to find all 30,000 post URLs")
    print("=" * 50)
