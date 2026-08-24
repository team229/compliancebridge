#!/usr/bin/env python3
"""
ComplianceBridge Advisory - Main Automation Runner
Runs all automation tasks: SEO audit, content generation, backlink outreach
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add automation directories to path
automation_dir = Path("/Users/ayush/compliancebridge-advisory/automation")
sys.path.insert(0, str(automation_dir / 'seo-audit'))
sys.path.insert(0, str(automation_dir / 'content-generator'))
sys.path.insert(0, str(automation_dir / 'backlinks'))

from audit import SEOAudit
from blog_generator import BlogGenerator
from outreach import BacklinkManager

def run_full_automation():
    """Run complete automation suite"""
    site_dir = "/Users/ayush/compliancebridge-advisory"
    
    print("\n" + "="*70)
    print("COMPLIANCE BRIDGE ADVISORY - AUTOMATION SUITE")
    print("="*70)
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # 1. SEO Audit
    print("\n[1/3] Running SEO Audit...")
    print("-"*70)
    auditor = SEOAudit(site_dir)
    results = auditor.run_audit()
    report = auditor.generate_report()
    auditor.print_report(report)
    
    # 2. Content Generation
    print("\n[2/3] Generating Content Calendar...")
    print("-"*70)
    generator = BlogGenerator(site_dir)
    calendar = generator.create_content_calendar(10)
    print(f"\nScheduled {len(calendar)} blog posts")
    for item in calendar[:5]:
        print(f"  {item['date']}: {item['title']}")
    
    # 3. Backlink Outreach
    print("\n[3/3] Setting up Backlink Outreach...")
    print("-"*70)
    backlink_manager = BacklinkManager(site_dir)
    backlink_manager.save_templates()
    outreach_report = backlink_manager.generate_daily_report()
    print(f"Outreach targets: {outreach_report['total_targets']}")
    print(f"  High priority: {outreach_report['high_priority']}")
    print(f"  Medium priority: {outreach_report['medium_priority']}")
    print(f"  Low priority: {outreach_report['low_priority']}")
    
    # Summary
    print("\n" + "="*70)
    print("AUTOMATION COMPLETE")
    print("="*70)
    print(f"SEO Audit: {report['summary']['pages_audited']} pages audited")
    print(f"  Critical Issues: {report['summary']['critical_issues']}")
    print(f"  Warnings: {report['summary']['warnings']}")
    print(f"Content: {len(calendar)} blog posts scheduled")
    print(f"Backlinks: {outreach_report['total_targets']} outreach targets identified")
    print("\nReports saved to: /automation/reports/")
    print("="*70)

if __name__ == "__main__":
    run_full_automation()
