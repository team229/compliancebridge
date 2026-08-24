#!/usr/bin/env python3
"""
ComplianceBridge Advisory - Blog Content Generator
Generates SEO-optimized blog posts based on high-traffic keywords
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# High-traffic keyword topics for compliance/advisory niche
BLOG_TOPICS = [
    {
        "title": "Companies Act 2013 Annual Compliance Calendar for Private Limited Companies",
        "keywords": ["annual compliance calendar india", "private limited company compliance", "companies act 2013 compliance"],
        "category": "Annual Compliance",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["annual-compliance.html", "companies-act-compliance.html", "roc-compliance.html"]
    },
    {
        "title": "FEMA Compliance for Startups: A Complete Guide",
        "keywords": ["fema compliance startups", "fema for startups india", "foreign investment startups"],
        "category": "FEMA",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["fema-compliance.html", "fdi-compliance.html", "india-entry.html"]
    },
    {
        "title": "How to Register a Private Limited Company in India: Step-by-Step Guide",
        "keywords": ["register private limited company india", "company incorporation process", "pvt ltd registration"],
        "category": "Company Incorporation",
        "search_volume": "very high",
        "difficulty": "high",
        "service_links": ["company-incorporation.html", "india-entry.html"]
    },
    {
        "title": "NBFC Compliance Requirements Under RBI: 2026 Guide",
        "keywords": ["nbfc compliance requirements", "rbi compliance nbfc", "nbfc annual compliance"],
        "category": "NBFC Compliance",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["nbfc-compliance.html", "rbi-compliance.html"]
    },
    {
        "title": "FC-GPR Filing: Complete Guide for Foreign Direct Investment in India",
        "keywords": ["fc-gpr filing", "fc-gpr form", "foreign direct investment filing india"],
        "category": "FDI Compliance",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["fdi-compliance.html", "fema-compliance.html"]
    },
    {
        "title": "POSH Act Compliance: Employer's Complete Guide 2026",
        "keywords": ["posh compliance", "posh act compliance", "sexual harassment policy india"],
        "category": "Labour Compliance",
        "search_volume": "high",
        "difficulty": "low",
        "service_links": ["posh-compliance.html", "labour-law-compliance.html"]
    },
    {
        "title": "LEI Registration in India: Who Needs It and How to Apply",
        "keywords": ["lei registration india", "legal entity identifier india", "lei code registration"],
        "category": "LEI Registration",
        "search_volume": "medium",
        "difficulty": "low",
        "service_links": ["lei-registration.html"]
    },
    {
        "title": "Corporate Governance Best Practices for Indian Companies",
        "keywords": ["corporate governance india", "board governance best practices", "sebi corporate governance"],
        "category": "Corporate Governance",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["corporate-governance.html", "board-advisory.html"]
    },
    {
        "title": "ODI Compliance: Overseas Investment Rules for Indian Companies",
        "keywords": ["odi compliance india", "overseas direct investment", "odi reporting india"],
        "category": "ODI Compliance",
        "search_volume": "medium",
        "difficulty": "medium",
        "service_links": ["odi-compliance.html", "fema-compliance.html"]
    },
    {
        "title": "Share Transfer in Private Limited Company: Complete Procedure",
        "keywords": ["share transfer private limited company", "share transfer procedure india", "share transfer compliance"],
        "category": "Share Transfer",
        "search_volume": "medium",
        "difficulty": "low",
        "service_links": ["share-transfer.html", "company-incorporation.html"]
    },
    {
        "title": "CSR Compliance Under Companies Act 2013: Complete Guide",
        "keywords": ["csr compliance india", "csr under companies act", "corporate social responsibility compliance"],
        "category": "CSR Compliance",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["csr-advisory.html", "companies-act-compliance.html"]
    },
    {
        "title": "ECB Compliance: External Commercial Borrowings in India",
        "keywords": ["ecb compliance india", "external commercial borrowings", "ecb reporting india"],
        "category": "ECB Compliance",
        "search_volume": "medium",
        "difficulty": "medium",
        "service_links": ["ecb-compliance.html", "fema-compliance.html"]
    },
    {
        "title": "DIR-3 KYC Filing: Director KYC Compliance Guide",
        "keywords": ["dir-3 kyc", "director kyc filing", "dir 3 kyc due date"],
        "category": "Director Compliance",
        "search_volume": "high",
        "difficulty": "low",
        "service_links": ["annual-compliance.html", "companies-act-compliance.html"]
    },
    {
        "title": "Labour Law Compliance Checklist for Indian Companies",
        "keywords": ["labour law compliance india", "labour compliance checklist", "employment law compliance"],
        "category": "Labour Compliance",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["labour-law-compliance.html", "posh-compliance.html"]
    },
    {
        "title": "ESG Reporting in India: SEBI BRSR Requirements Explained",
        "keywords": ["esg reporting india", "brsr reporting", "sustainability reporting india"],
        "category": "ESG Compliance",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["esg-advisory.html", "brsr-advisory.html"]
    },
    {
        "title": "Foreign Company Registration in India: Subsidiary vs Branch vs Liaison Office",
        "keywords": ["foreign company india", "subsidiary company india", "branch office india"],
        "category": "India Entry",
        "search_volume": "high",
        "difficulty": "medium",
        "service_links": ["india-entry.html", "company-incorporation.html"]
    },
    {
        "title": "ROC Filing Due Dates 2026: Complete Compliance Calendar",
        "keywords": ["roc filing due dates", "roc compliance calendar", "mca filing due dates"],
        "category": "ROC Compliance",
        "search_volume": "very high",
        "difficulty": "high",
        "service_links": ["roc-compliance.html", "annual-compliance.html"]
    },
    {
        "title": "Board Meeting Compliance Under Companies Act 2013",
        "keywords": ["board meeting compliance", "board meeting requirements companies act", "board meeting notice"],
        "category": "Board Compliance",
        "search_volume": "medium",
        "difficulty": "low",
        "service_links": ["corporate-governance.html", "board-advisory.html"]
    },
    {
        "title": "Downstream Investment Compliance Under FEMA",
        "keywords": ["downstream investment compliance", "downstream investment fema", "indirect foreign investment"],
        "category": "FDI Compliance",
        "search_volume": "medium",
        "difficulty": "medium",
        "service_links": ["fdi-compliance.html", "fema-compliance.html"]
    },
    {
        "title": "Independent Director Compliance: Appointment, Duties & Obligations",
        "keywords": ["independent director compliance", "independent director duties", "independent director appointment"],
        "category": "Board Compliance",
        "search_volume": "medium",
        "difficulty": "low",
        "service_links": ["board-advisory.html", "corporate-governance.html"]
    }
]

class BlogGenerator:
    def __init__(self, site_dir):
        self.site_dir = Path(site_dir)
        self.topics = BLOG_TOPICS
        self.content_dir = self.site_dir / 'insights'
        self.scheduled_dir = self.site_dir / 'automation' / 'content-calendar'
        self.scheduled_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_blog_template(self, topic, publish_date):
        """Generate a blog post template"""
        slug = topic['title'].lower().replace(' ', '-').replace(':', '').replace(',', '').replace("'", "")
        filename = f"{slug}.html"
        
        template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic['title']} | ComplianceBridge Advisory</title>
    <meta name="description" content="Comprehensive guide on {topic['title'].lower()}. Expert insights from ComplianceBridge Advisory on corporate compliance in India.">
    <meta name="keywords" content="{', '.join(topic['keywords'])}">
    <link rel="canonical" href="https://compliancebridgeadvisory.com/insights/{filename}">
    <link rel="icon" href="../favicon.svg" type="image/svg+xml">
    <!-- Open Graph -->
    <meta property="og:title" content="{topic['title']} | ComplianceBridge Advisory">
    <meta property="og:description" content="Comprehensive guide on {topic['title'].lower()}. Expert insights from ComplianceBridge Advisory.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://compliancebridgeadvisory.com/insights/{filename}">
    <meta property="og:site_name" content="ComplianceBridge Advisory">
    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{topic['title']}",
        "description": "Comprehensive guide on {topic['title'].lower()}",
        "author": {{
            "@type": "Organization",
            "name": "ComplianceBridge Advisory"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "ComplianceBridge Advisory",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://compliancebridgeadvisory.com/favicon.svg"
            }}
        }},
        "datePublished": "{publish_date}",
        "dateModified": "{publish_date}"
    }}
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#111827',
                        accent: '#D97706',
                        'accent-hover': '#B45309',
                        'light-bg': '#F9FAFB',
                    }},
                    fontFamily: {{
                        serif: ['"Playfair Display"', 'serif'],
                        sans: ['Inter', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="font-sans text-gray-700 antialiased">
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 bg-primary text-white py-4 shadow-lg">
        <div class="container mx-auto px-6 flex justify-between items-center">
            <a href="../index.html" class="text-2xl font-serif font-bold tracking-wide">
                Compliance<span class="text-accent">Bridge</span> Advisory
            </a>
            <div class="hidden lg:flex items-center space-x-1 text-sm font-medium tracking-wider">
                <a href="../index.html" class="px-3 py-2 hover:text-accent transition-colors">HOME</a>
                <a href="../about.html" class="px-3 py-2 hover:text-accent transition-colors">ABOUT</a>
                <a href="../practice-areas.html" class="px-3 py-2 hover:text-accent transition-colors">SERVICES</a>
                <a href="../industries.html" class="px-3 py-2 hover:text-accent transition-colors">INDUSTRIES</a>
                <a href="../insights.html" class="px-3 py-2 text-accent transition-colors">INSIGHTS</a>
                <a href="../contact.html" class="px-3 py-2 hover:text-accent transition-colors">CONTACT</a>
                <a href="../contact.html" class="ml-4 bg-accent hover:bg-accent-hover text-white px-5 py-2.5 font-medium transition-colors inline-flex items-center gap-2 text-sm">
                    <i data-lucide="calendar" class="w-4 h-4"></i> SCHEDULE A CALL
                </a>
            </div>
            <button id="mobile-menu-button" class="lg:hidden text-white focus:outline-none">
                <i data-lucide="menu" class="w-6 h-6"></i>
            </button>
        </div>
    </nav>

    <!-- Breadcrumb -->
    <div class="bg-gray-50 py-4 border-b border-gray-100">
        <div class="container mx-auto px-6">
            <nav class="flex items-center space-x-2 text-sm text-gray-500">
                <a href="../index.html" class="hover:text-accent transition-colors">Home</a>
                <span>/</span>
                <a href="../insights.html" class="hover:text-accent transition-colors">Insights</a>
                <span>/</span>
                <span class="text-primary">{topic['category']}</span>
            </nav>
        </div>
    </div>

    <!-- Article Header -->
    <header class="bg-primary text-white py-16">
        <div class="container mx-auto px-6 max-w-4xl">
            <span class="text-accent text-sm font-bold uppercase tracking-wider">{topic['category']}</span>
            <h1 class="text-3xl md:text-5xl font-serif font-medium leading-tight mt-4 mb-6">
                {topic['title']}
            </h1>
            <div class="flex items-center gap-4 text-gray-400 text-sm">
                <span>By ComplianceBridge Advisory</span>
                <span>|</span>
                <span>{publish_date}</span>
                <span>|</span>
                <span>12 min read</span>
            </div>
        </div>
    </header>

    <!-- Article Content -->
    <article class="py-16 bg-white">
        <div class="container mx-auto px-6 max-w-4xl">
            <div class="prose prose-lg max-w-none">
                <p class="text-xl text-gray-600 leading-relaxed mb-8">
                    [INTRODUCTION PARAGRAPH - Write a compelling introduction explaining what this guide covers and why it matters for businesses in India]
                </p>

                <h2 class="text-2xl font-serif text-primary mt-12 mb-4">Table of Contents</h2>
                <ul class="list-disc pl-6 space-y-2 mb-8 text-gray-600">
                    <li><a href="#section-1" class="text-accent hover:text-accent-hover">Section 1 Title</a></li>
                    <li><a href="#section-2" class="text-accent hover:text-accent-hover">Section 2 Title</a></li>
                    <li><a href="#section-3" class="text-accent hover:text-accent-hover">Section 3 Title</a></li>
                    <li><a href="#section-4" class="text-accent hover:text-accent-hover">Section 4 Title</a></li>
                    <li><a href="#section-5" class="text-accent hover:text-accent-hover">Section 5 Title</a></li>
                </ul>

                <h2 id="section-1" class="text-2xl font-serif text-primary mt-12 mb-4">Section 1 Title</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    [SECTION 1 CONTENT - Write detailed, authoritative content covering this topic. Include relevant laws, regulations, practical examples, and actionable advice.]
                </p>

                <h2 id="section-2" class="text-2xl font-serif text-primary mt-12 mb-4">Section 2 Title</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    [SECTION 2 CONTENT]
                </p>

                <h2 id="section-3" class="text-2xl font-serif text-primary mt-12 mb-4">Section 3 Title</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    [SECTION 3 CONTENT]
                </p>

                <h2 id="section-4" class="text-2xl font-serif text-primary mt-12 mb-4">Section 4 Title</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    [SECTION 4 CONTENT]
                </p>

                <h2 id="section-5" class="text-2xl font-serif text-primary mt-12 mb-4">Section 5 Title</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    [SECTION 5 CONTENT]
                </p>

                <h2 class="text-2xl font-serif text-primary mt-12 mb-4">Conclusion</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    [CONCLUSION - Summarize key points and provide a clear call to action]
                </p>
            </div>

            <!-- CTA Box -->
            <div class="bg-gray-50 p-8 rounded-sm mt-12 border border-gray-200">
                <h3 class="text-xl font-serif text-primary mb-4">Need Help with Compliance?</h3>
                <p class="text-gray-600 mb-6">Our team of experts can help you navigate complex compliance requirements. Schedule a consultation today.</p>
                <a href="../contact.html" class="bg-accent hover:bg-accent-hover text-white px-6 py-3 font-medium transition-colors inline-flex items-center gap-2">
                    <i data-lucide="calendar" class="w-4 h-4"></i> SCHEDULE A CONSULTATION
                </a>
            </div>

            <!-- Related Services -->
            <div class="mt-12">
                <h3 class="text-xl font-serif text-primary mb-6">Related Services</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {"".join([f'<a href="../{link}" class="bg-gray-50 p-4 hover:bg-gray-100 transition-colors border border-gray-200"><span class="text-accent font-medium text-sm">{link.replace(".html", "").replace("-", " ").title()}</span></a>' for link in topic['service_links']])}
                </div>
            </div>
        </div>
    </article>

    <!-- Footer -->
    <footer class="bg-[#0a0f1a] text-gray-400 py-12 text-sm border-t border-gray-800">
        <div class="container mx-auto px-6 text-center">
            <p>&copy; 2026 ComplianceBridge Advisory. All rights reserved.</p>
        </div>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>'''
        
        return filename, template
    
    def create_content_calendar(self, days=30):
        """Create a content calendar for the next N days"""
        calendar = []
        today = datetime.now()
        
        for i, topic in enumerate(self.topics[:days]):
            publish_date = today + timedelta(days=i)
            calendar.append({
                'date': publish_date.strftime('%Y-%m-%d'),
                'title': topic['title'],
                'category': topic['category'],
                'keywords': topic['keywords'],
                'search_volume': topic['search_volume'],
                'difficulty': topic['difficulty'],
                'status': 'scheduled'
            })
            
            # Generate template
            filename, template = self.generate_blog_template(topic, publish_date.strftime('%Y-%m-%d'))
            filepath = self.content_dir / filename
            
            if not filepath.exists():
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(template)
                print(f"Created: {filename}")
            else:
                print(f"Exists: {filename}")
        
        # Save calendar
        calendar_path = self.scheduled_dir / 'content_calendar.json'
        with open(calendar_path, 'w') as f:
            json.dump(calendar, f, indent=2)
            
        print(f"\nContent calendar created: {len(calendar)} posts scheduled")
        return calendar

if __name__ == "__main__":
    site_dir = "/Users/ayush/compliancebridge-advisory"
    generator = BlogGenerator(site_dir)
    calendar = generator.create_content_calendar(20)
