#!/usr/bin/env python3
"""
ComplianceBridge Advisory - On-Page SEO Audit Tool
Automatically audits all pages for SEO best practices
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

class SEOAudit:
    def __init__(self, site_dir):
        self.site_dir = Path(site_dir)
        self.issues = []
        self.stats = {
            'total_pages': 0,
            'pages_with_title': 0,
            'pages_with_meta_desc': 0,
            'pages_with_canonical': 0,
            'pages_with_schema': 0,
            'pages_with_h1': 0,
            'pages_with_og': 0,
            'pages_with_twitter': 0,
            'pages_with_breadcrumb': 0,
            'pages_with_faq': 0
        }
        
    def audit_page(self, filepath):
        """Audit a single HTML page for SEO elements"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = filepath.name
        page_issues = []
        
        # Check title tag
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if not title_match:
            page_issues.append(('CRITICAL', 'Missing title tag'))
        elif len(title_match.group(1).strip()) < 30:
            page_issues.append(('WARNING', f'Title too short ({len(title_match.group(1).strip())} chars)'))
        elif len(title_match.group(1).strip()) > 60:
            page_issues.append(('WARNING', f'Title too long ({len(title_match.group(1).strip())} chars)'))
        else:
            self.stats['pages_with_title'] += 1
            
        # Check meta description
        meta_desc = re.search(r'<meta name="description" content="(.*?)"', content)
        if not meta_desc:
            page_issues.append(('CRITICAL', 'Missing meta description'))
        elif len(meta_desc.group(1).strip()) < 120:
            page_issues.append(('WARNING', f'Meta description too short ({len(meta_desc.group(1).strip())} chars)'))
        elif len(meta_desc.group(1).strip()) > 160:
            page_issues.append(('WARNING', f'Meta description too long ({len(meta_desc.group(1).strip())} chars)'))
        else:
            self.stats['pages_with_meta_desc'] += 1
            
        # Check canonical URL
        canonical = re.search(r'<link rel="canonical" href="(.*?)"', content)
        if not canonical:
            page_issues.append(('CRITICAL', 'Missing canonical URL'))
        else:
            self.stats['pages_with_canonical'] += 1
            
        # Check H1 tag
        h1_count = len(re.findall(r'<h1[^>]*>', content))
        if h1_count == 0:
            page_issues.append(('CRITICAL', 'Missing H1 tag'))
        elif h1_count > 1:
            page_issues.append(('WARNING', f'Multiple H1 tags ({h1_count})'))
        else:
            self.stats['pages_with_h1'] += 1
            
        # Check schema/structured data
        if 'application/ld+json' not in content:
            page_issues.append(('CRITICAL', 'Missing structured data'))
        else:
            self.stats['pages_with_schema'] += 1
            
        # Check Open Graph
        og_title = re.search(r'<meta property="og:title"', content)
        og_desc = re.search(r'<meta property="og:description"', content)
        if not og_title or not og_desc:
            page_issues.append(('WARNING', 'Missing Open Graph tags'))
        else:
            self.stats['pages_with_og'] += 1
            
        # Check Twitter Card
        twitter_card = re.search(r'<meta name="twitter:card"', content)
        if not twitter_card:
            page_issues.append(('WARNING', 'Missing Twitter Card tags'))
        else:
            self.stats['pages_with_twitter'] += 1
            
        # Check breadcrumb
        if 'BreadcrumbList' in content or 'breadcrumb' in content.lower():
            self.stats['pages_with_breadcrumb'] += 1
            
        # Check FAQ
        if 'FAQPage' in content or 'faq' in content.lower():
            self.stats['pages_with_faq'] += 1
            
        # Check internal links
        internal_links = re.findall(r'href="([^"]*\.html)"', content)
        
        # Check image alt text (if any images)
        images = re.findall(r'<img[^>]*>', content)
        for img in images:
            if 'alt=' not in img:
                page_issues.append(('WARNING', 'Image missing alt text'))
                
        return {
            'file': filename,
            'issues': page_issues,
            'internal_links': len(set(internal_links))
        }
    
    def run_audit(self):
        """Run audit on all HTML files"""
        html_files = list(self.site_dir.glob('*.html'))
        html_files.extend(list(self.site_dir.glob('insights/*.html')))
        
        results = []
        for filepath in html_files:
            self.stats['total_pages'] += 1
            result = self.audit_page(filepath)
            results.append(result)
            if result['issues']:
                self.issues.extend([(result['file'], *issue) for issue in result['issues']])
                
        return results
    
    def generate_report(self):
        """Generate audit report"""
        report = {
            'audit_date': datetime.now().isoformat(),
            'stats': self.stats,
            'issues': self.issues,
            'summary': {
                'critical_issues': len([i for i in self.issues if i[1] == 'CRITICAL']),
                'warnings': len([i for i in self.issues if i[1] == 'WARNING']),
                'pages_audited': self.stats['total_pages']
            }
        }
        
        # Save report
        report_path = self.site_dir / 'automation' / 'reports' / f'audit_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report
    
    def print_report(self, report):
        """Print formatted audit report"""
        print("\n" + "="*60)
        print("COMPLIANCE BRIDGE ADVISORY - SEO AUDIT REPORT")
        print("="*60)
        print(f"Audit Date: {report['audit_date']}")
        print(f"Pages Audited: {report['summary']['pages_audited']}")
        print(f"Critical Issues: {report['summary']['critical_issues']}")
        print(f"Warnings: {report['summary']['warnings']}")
        print("\n" + "-"*60)
        print("PAGE STATISTICS:")
        print("-"*60)
        for key, value in report['stats'].items():
            if key != 'total_pages':
                print(f"  {key.replace('pages_with_', 'Pages with ').replace('_', ' ').title()}: {value}/{report['stats']['total_pages']}")
        print("\n" + "-"*60)
        print("ISSUES FOUND:")
        print("-"*60)
        for issue in report['issues']:
            print(f"  [{issue[1]}] {issue[0]}: {issue[2]}")
        print("="*60)

if __name__ == "__main__":
    site_dir = "/Users/ayush/compliancebridge-advisory"
    auditor = SEOAudit(site_dir)
    results = auditor.run_audit()
    report = auditor.generate_report()
    auditor.print_report(report)
