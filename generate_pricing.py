import re

template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__NICHE_NAME__ - Pricing Packages</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;700&family=DM+Sans:wght@300;400;500&display=swap');

        :root {
            --color-background: #0a0a0a;
            --color-card-bg: rgba(26, 26, 26, 0.6);
            --color-text-primary: #f5f5f5;
            --color-text-secondary: #a3a3a3;
            --color-accent: #d4af37;
            --color-border: rgba(255, 255, 255, 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'DM Sans', sans-serif; background-color: var(--color-background); color: var(--color-text-primary); line-height: 1.6; overflow-x: hidden; }
        .container { max-width: 1200px; margin: 0 auto; padding: 4rem 1.5rem; }
        .header { text-align: center; margin-bottom: 5rem; position: relative; }
        .header h1 { font-family: 'Playfair Display', serif; font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 700; margin-bottom: 1rem; letter-spacing: -0.02em; background: linear-gradient(135deg, #fff 0%, #a3a3a3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .header p { color: var(--color-text-secondary); font-size: 1.1rem; max-width: 600px; margin: 0 auto; }
        .back-btn { position: absolute; top: -2rem; left: 0; color: var(--color-text-secondary); text-decoration: none; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; transition: color 0.3s; }
        .back-btn:hover { color: var(--color-text-primary); }
        .pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem; align-items: stretch; }
        .pricing-card { background: var(--color-card-bg); backdrop-filter: blur(12px); border: 1px solid var(--color-border); border-radius: 24px; padding: 3rem 2rem; display: flex; flex-direction: column; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.4s; position: relative; }
        .pricing-card:hover { transform: translateY(-10px); border-color: rgba(212, 175, 55, 0.4); }
        .pricing-card.featured { border-color: var(--color-accent); background: rgba(212, 175, 55, 0.05); }
        .featured-tag { position: absolute; top: 20px; right: -10px; background: var(--color-accent); color: #000; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 1rem; border-radius: 4px; transform: rotate(5deg); }
        .package-name { font-family: 'Playfair Display', serif; font-size: 1.75rem; font-weight: 500; margin-bottom: 1.5rem; color: var(--color-accent); }
        .package-price { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
        .package-subtitle { font-size: 0.9rem; color: var(--color-text-secondary); margin-bottom: 2.5rem; min-height: 3rem; }
        .features-list { list-style: none; margin-bottom: 3rem; flex-grow: 1; }
        .features-list li { padding: 0.75rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.95rem; color: var(--color-text-primary); display: flex; align-items: center; gap: 0.75rem; }
        .features-list li:last-child { border-bottom: none; }
        .features-list li::before { content: '✓'; color: var(--color-accent); font-weight: bold; }
        .cta-button { display: block; width: 100%; padding: 1.25rem; text-align: center; text-decoration: none; border-radius: 12px; font-weight: 600; transition: all 0.3s; cursor: pointer; }
        .basic-btn { background: transparent; border: 1px solid var(--color-border); color: var(--color-text-primary); }
        .basic-btn:hover { background: rgba(255, 255, 255, 0.05); border-color: var(--color-text-primary); }
        .accent-btn { background: var(--color-accent); color: #000; border: none; }
        .accent-btn:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(212, 175, 55, 0.2); }
        .premium-btn { background: #fff; color: #000; border: none; }
        .premium-btn:hover { background: #e0e0e0; }
        .note { font-size: 0.8rem; color: var(--color-text-secondary); margin-top: 1rem; font-style: italic; opacity: 0.8; }
        @media (max-width: 768px) { .pricing-grid { grid-template-columns: 1fr; } }

        .sample-pulse-btn {
            margin-top: 12px; padding: 0.8rem; font-size: 0.85rem;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(212, 175, 55, 0.05));
            border: 1px solid rgba(212, 175, 55, 0.6); color: var(--color-accent); font-weight: 700;
            text-transform: uppercase; letter-spacing: 0.1em; position: relative; overflow: hidden;
            animation: borderPulse 2s infinite; text-align: center; display: block; border-radius: 12px;
        }
        .sample-pulse-btn::after {
            content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transform: skewX(-20deg); animation: shineSweep 4s infinite;
        }
        @keyframes borderPulse {
            0% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.5); }
            70% { box-shadow: 0 0 0 12px rgba(212, 175, 55, 0); }
            100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); }
        }
        @keyframes shineSweep {
            0% { left: -100%; }
            20% { left: 200%; }
            100% { left: 200%; }
        }
    </style>
</head>
<body>
<div class="container">
    <header class="header">
        <a href="index.html" class="back-btn">← Back to Showcase</a>
        <h1>Elevate Your Business</h1>
        <p>Premium web experiences tailored for __NICHE_NAME__.</p>
    </header>

    <div class="pricing-grid">
        <!-- Basic -->
        <div class="pricing-card">
            <div class="package-name">Basic "__B_NAME__"</div>
            <div class="package-price">__B_PRICE__</div>
            <div class="package-subtitle">Perfect for starting your digital journey.</div>
            <ul class="features-list">
                __B_FEATURES__
                <li>Custom Design Modifications</li>
            </ul>
            <a href="tel:9501071554" class="cta-button basic-btn">Get Started</a>
            <a href="PHOTOGRAPHYBASIC.html" class="cta-button sample-pulse-btn" style="color:var(--color-text-secondary); border-color:rgba(255,255,255,0.05); background:rgba(255,255,255,0.02);">✨ View Sample Page ✨</a>
        </div>

        <!-- Pro -->
        <div class="pricing-card featured">
            <div class="featured-tag">The Sweet Spot</div>
            <div class="package-name">Pro "__P_NAME__"</div>
            <div class="package-price">__P_PRICE__</div>
            <div class="package-subtitle">Advanced selection systems and automated flows.</div>
            <ul class="features-list">
                <li>Everything in Basic</li>
                __P_FEATURES__
                <li>Custom Design Modifications</li>
            </ul>
            <a href="tel:9501071554" class="cta-button accent-btn">Inquire Now</a>
            <a href="LUMIERE_REDESIGN.html" class="cta-button sample-pulse-btn">✨ View Sample Page ✨</a>
            <p class="note">* Includes monthly maintenance & Ops fee.</p>
        </div>

        <!-- Premium -->
        <div class="pricing-card">
            <div class="package-name">Premium "__PR_NAME__"</div>
            <div class="package-price">__PR_PRICE__</div>
            <div class="package-subtitle">The ultimate business engine with full automation.</div>
            <ul class="features-list">
                <li>Everything in Professional</li>
                __PR_FEATURES__
                <li>Custom Design Modifications</li>
            </ul>
            <a href="tel:9501071554" class="cta-button premium-btn">Book Strategy Call</a>
            <div style="margin-top: 12px; padding: 0.8rem; border-radius: 12px; border: 1px solid rgba(212,175,55,0.6); background: rgba(212,175,55,0.15); text-align: center; color: var(--color-accent); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; box-shadow: inset 0 0 10px rgba(212,175,55,0.2);">
                🔒 Sample Page Available on Order Only
            </div>
            <p class="note">* Includes monthly payments for API & advanced hosting</p>
        </div>
    </div>
</div>
</body>
</html>
"""

data = [
    {
        "file": "gym_pricing.html",
        "niche_name": "Gyms & Fitness Centres",
        "b_name": "Digital Presence", "b_price": "₹18,000 – ₹28,000",
        "b_features": "<li>5 Pages & Trainer Profiles</li><li>WhatsApp Chat Integration</li><li>Google Maps & SEO</li><li>Shared Hosting (₹500/mo)</li>",
        "p_name": "Active Management", "p_price": "₹45,000 – ₹70,000",
        "p_features": "<li>Automated Class Booking</li><li>Trainer Slot Booking</li><li>BMI/Fitness Calculators</li><li>Fast Cloud Hosting (₹1,500/mo)</li>",
        "pr_name": "Elite SaaS", "pr_price": "₹95,000 – ₹1,60,000+",
        "pr_features": "<li>Member Dashboard (SaaS)</li><li>Auto-Payment Reminders</li><li>Calorie & Step Tracking</li><li>Dedicated Server (₹3,000/mo)</li>"
    },
    {
        "file": "clinic_pricing.html",
        "niche_name": "Medical & Dental Clinics",
        "b_name": "Clinic Connect", "b_price": "₹22,000 – ₹32,000",
        "b_features": "<li>Doctor Bio & Experience</li><li>Call Now Button</li><li>Standard SSL Security</li><li>Shared Hosting (₹600/mo)</li>",
        "p_name": "Doctor Assist", "p_price": "₹55,000 – ₹85,000",
        "p_features": "<li>Real-time Appointment Calendar</li><li>Auto-SMS Reminders</li><li>Advanced Encryption</li><li>Secure Cloud Hosting (₹2,000/mo)</li>",
        "pr_name": "Smart Health", "pr_price": "₹1,30,000 – ₹2,10,000+",
        "pr_features": "<li>Patient Health Portal</li><li>Digital Report Delivery</li><li>HIPAA-Compliant Database</li><li>Encrypted Managed Host (₹4,500/mo)</li>"
    },
    {
        "file": "law_pricing.html",
        "niche_name": "Law Firms & Accountants",
        "b_name": "Professional", "b_price": "₹20,000 – ₹30,000",
        "b_features": "<li>Case Results & Expertise</li><li>Inquiry Form to Email</li><li>Standard Security</li><li>Standard Hosting (₹500/mo)</li>",
        "p_name": "Practice Flow", "p_price": "₹50,000 – ₹75,000",
        "p_features": "<li>Practice Area Landing Pages</li><li>Client Intake Automation</li><li>Lead Conversion Optimised</li><li>Fast Cloud Hosting (₹1,500/mo)</li>",
        "pr_name": "Global Firm", "pr_price": "₹1,10,000 – ₹1,80,000+",
        "pr_features": "<li>Secure Client Login</li><li>Document Upload System</li><li>Full Case Management</li><li>Secure Hosting (₹2,500/mo)</li>"
    },
    {
        "file": "food_pricing.html",
        "niche_name": "Food & Beverages",
        "b_name": "Digital Menu", "b_price": "₹12,000 – ₹18,000",
        "b_features": "<li>Interactive Photo Menu</li><li>Social Media Sync</li><li>Mobile Optimised</li><li>Shared Hosting (₹400/mo)</li>",
        "p_name": "Order Station", "p_price": "₹35,000 – ₹55,000",
        "p_features": "<li>WhatsApp Ordering System</li><li>Table Reservations</li><li>Higher Table Turnover</li><li>E-com Ready Hosting (₹1,800/mo)</li>",
        "pr_name": "Dining Tech", "pr_price": "₹85,000 – ₹1,40,000+",
        "pr_features": "<li>Full E-commerce (Pre-orders)</li><li>Loyalty Program / SMS</li><li>Direct Customer Ownership</li><li>High-Traffic Cloud (₹3,000/mo)</li>"
    },
    {
        "file": "interior_pricing.html",
        "niche_name": "Interior Design & Architecture",
        "b_name": "Digital Presence", "b_price": "₹15,000 – ₹25,000",
        "b_features": "<li>5-7 Custom Pages</li><li>HD Project Portfolio</li><li>Google Maps Integration</li><li>WhatsApp Chat Support</li>",
        "p_name": "Visual Studio Site", "p_price": "₹30,000 – ₹55,000",
        "p_features": "<li>Interactive Mood Boards</li><li>Secure Client Project Portal</li><li>Automated Email Notifications</li><li>Enhanced SEO Package</li>",
        "pr_name": "Full Automation", "pr_price": "₹60,000 – ₹1,20,000+",
        "pr_features": "<li>Online Booking & Payments</li><li>CRM Integration (Lead Mgmt)</li><li>Custom ADMIN Dashboard</li><li>Priority 24/7 Support</li>"
    }
]

for d in data:
    html = template.replace("__NICHE_NAME__", d["niche_name"])
    html = html.replace("__B_NAME__", d["b_name"])
    html = html.replace("__B_PRICE__", d["b_price"])
    html = html.replace("__B_FEATURES__", d["b_features"])
    
    html = html.replace("__P_NAME__", d["p_name"])
    html = html.replace("__P_PRICE__", d["p_price"])
    html = html.replace("__P_FEATURES__", d["p_features"])
    
    html = html.replace("__PR_NAME__", d["pr_name"])
    html = html.replace("__PR_PRICE__", d["pr_price"])
    html = html.replace("__PR_FEATURES__", d["pr_features"])
    
    with open(d['file'], 'w') as f:
        f.write(html)

