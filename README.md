# 🎯 JobsForHer Scraper — Women-Focused Job Board Data

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-00D4AA?style=flat&logo=apify)](https://apify.com/fervent_bus/jobsforher-scraper)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![AI Agent Ready](https://img.shields.io/badge/AI%20Agent-Ready-blueviolet?style=flat)](https://claude-code.nousresearch.com/)

Extract comprehensive job listing data from **JobsForHer.com**, India's leading platform for women's employment opportunities, flexible work, and work-from-home positions. This actor uses advanced browser automation to scrape job titles, companies, locations, work modes, salaries, experience requirements, and more.

Perfect for **Claude Code**, **ChatGPT**, **MCP agents**, and other AI assistants connected to Apify.

---

## 🎯 Features

✅ **Zero Competition** — First and only JobsForHer scraper on Apify Store  
✅ **Women-Focused Jobs** — Flexible work, WFH, part-time opportunities  
✅ **500K+ Monthly Traffic** — High-value Indian job market data  
✅ **Complete Job Data** — Title, company, location, salary, type, experience, URL  
✅ **AI Agent Compatible** — Works seamlessly with Claude, ChatGPT, MCP agents  
✅ **Residential Proxies** — Bypass geo-restrictions and rate limits  
✅ **Pagination Support** — Scrape 10, 100, or 1000+ job listings  
✅ **Client-Side Rendering** — Uses Camoufox browser automation for JavaScript-heavy sites  

---

## 📊 Output Data

Each job listing includes:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Job title (e.g., "Senior Software Engineer") |
| `company` | string | Company name |
| `location` | string | Job location (city/state) |
| `jobType` | string | Work mode (WFH, Hybrid, Onsite, Flexible) |
| `experience` | string | Required experience (e.g., "2-5 years") |
| `salary` | string | Salary range or CTC |
| `url` | string | Direct link to job posting |
| `postedDate` | string | When the job was posted |
| `description` | string | Job description snippet |
| `scrapedAt` | string | ISO 8601 timestamp of scrape |
| `sourceUrl` | string | Page URL where job was found |

---

## 🚀 Quick Start

### Input Configuration

```json
{
  "startUrl": "https://www.jobsforher.com/jobs",
  "maxResults": 50,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

### Example Output

```json
{
  "title": "Content Writer - Work From Home",
  "company": "Acme Marketing Solutions",
  "location": "Mumbai, Maharashtra",
  "jobType": "Work From Home",
  "experience": "1-3 years",
  "salary": "₹3-5 LPA",
  "url": "https://www.jobsforher.com/job/content-writer-wfh-12345",
  "postedDate": "2 days ago",
  "description": "Looking for a creative content writer to join our remote team...",
  "scrapedAt": "2025-08-25T10:30:00.000Z",
  "sourceUrl": "https://www.jobsforher.com/jobs"
}
```

---

## 🤖 AI Integration

This actor is **optimized for AI agents** and works seamlessly with:

- **Claude Code** — via Apify MCP integration
- **ChatGPT** — via Apify plugin or API
- **Custom AI Agents** — any system using Apify SDK
- **Automation Workflows** — Zapier, Make, n8n

### Claude Code Example

```bash
# Ask Claude to get job data
"Find 20 work-from-home jobs for women in tech from JobsForHer"
```

Claude will automatically:
1. Connect to Apify MCP server
2. Run this actor with appropriate parameters
3. Parse and analyze the results
4. Present insights in readable format

---

## 💼 Use Cases

| Use Case | Description |
|----------|-------------|
| **Recruitment** | Source diverse candidates from women-focused job boards |
| **Market Research** | Analyze salary trends, job types, top hiring companies |
| **Competitor Analysis** | Track job postings from specific companies |
| **Job Aggregation** | Build your own job board or newsletter |
| **AI Training Data** | Collect job market data for ML models |
| **Diversity Analytics** | Study flexible work opportunities for women |

---

## ⚙️ Technical Details

- **Language:** Python 3.11
- **Framework:** Apify SDK 2.0
- **Browser:** Camoufox (privacy-focused Firefox fork)
- **Rendering:** Full JavaScript execution for React/MUI sites
- **Proxy Support:** Residential proxies recommended (included)
- **Pagination:** Automatic multi-page scraping

---

## 📝 Notes

- **Zero Bot Protection:** JobsForHer has no Cloudflare/Akamai blocking
- **Client-Side Rendered:** Uses browser automation (not simple HTTP requests)
- **Residential Proxies:** Pre-configured for best results
- **Respectful Scraping:** Built-in delays between requests

---

## 🔗 Links

- **Apify Store:** https://apify.com/fervent_bus/jobsforher-scraper
- **GitHub Repo:** https://github.com/roshtarg-cpu/jobsforher-scraper
- **JobsForHer Website:** https://www.jobsforher.com

---

## 📄 License

Apache 2.0

---

**Built with ❤️ for the AI agent ecosystem**
