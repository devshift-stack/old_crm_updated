# 🔬 Knowledge Base: Research Agent & Verification System

## 📋 Executive Summary

Erweiterung des Knowledge Base Systems mit:

1. **🤖 Research Agent** - Kontinuierliche Recherche und KB-Aufbau
2. **🧪 Beta/Production Pipeline** - Zweistufiges Verifikationssystem
3. **⏰ Expiration Management** - Automatisches Lifecycle-Management für zeitkritische Informationen

### Hauptziele
- ✅ **Fehlinformationen vermeiden** durch mehrstufige Verifikation
- ✅ **Kontinuierlich aktuelle Daten** durch Research Agent
- ✅ **Automatisches Lifecycle-Management** für zeitkritische Informationen
- ✅ **Qualitätssicherung** durch Beta-Filter
- ✅ **Compliance** für gesetzliche/regulatorische Informationen

---

## 🏗️ Erweiterte Architektur

```
┌─────────────────────────────────────────────────────────────────┐
│                  KNOWLEDGE BASE SYSTEM V2.0                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              RESEARCH AGENT (New)                         │  │
│  │  - Web Research  - Data Collection  - Monitoring         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  BETA KNOWLEDGE BASE                      │  │
│  │  Status: draft, beta                                      │  │
│  │  Verification: 0-2 confirmations                          │  │
│  │  ⚠️  Unverified - Use with caution                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                       │
│                          │ (Multi-Verification over time)       │
│                          │ (3+ confirmations required)          │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │             PRODUCTION KNOWLEDGE BASE                     │  │
│  │  Status: verified, published                              │  │
│  │  Verification: 3+ confirmations                           │  │
│  │  ✅ Verified - Safe for automation                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           EXPIRATION MANAGEMENT SYSTEM                    │  │
│  │  - Auto-review before expiry                              │  │
│  │  - Renewal workflows                                      │  │
│  │  - Archival of outdated info                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Research Agent (AI Agent #8)

### Überblick

Der **Research Agent** ist ein kontinuierlich laufender AI-Agent, der:
- Aktuelle Informationen aus dem Web recherchiert
- Branchen-News und Updates sammelt
- Gesetzesänderungen und regulatorische Updates überwacht
- Neue Best Practices identifiziert
- Knowledge Base kontinuierlich erweitert

### Use Cases

1. **Regulatorische Compliance**
   - Überwachung von Gesetzesänderungen (DSGVO, ePrivacy, etc.)
   - Steuerrecht-Updates
   - Branchenspezifische Vorschriften

2. **Produkt-Updates**
   - Neue Features von verwendeten Tools
   - Software-Updates und Breaking Changes
   - Security-Patches und CVEs

3. **Branchen-Trends**
   - Neue CRM Best Practices
   - AI/ML Entwicklungen
   - Konkurrenz-Analyse

4. **Customer Intelligence**
   - Kunden-Unternehmen News (Fusionen, neue Produkte)
   - Branchenspezifische Entwicklungen
   - Marktveränderungen

### Implementierung

```python
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from anthropic import Anthropic
import aiohttp
from bs4 import BeautifulSoup

class ResearchAgent:
    """
    Kontinuierlicher Research Agent für Knowledge Base.

    Läuft als Background Task:
    - Scheduled: Täglich für reguläre Updates
    - Real-time: Bei spezifischen Triggers (Customer-Event, etc.)
    - On-demand: Manuelle Research-Anfragen
    """

    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.research_sources = self._load_research_sources()
        self.monitoring_topics = self._load_monitoring_topics()

    def _load_research_sources(self) -> List[Dict[str, str]]:
        """
        Konfigurierbare Research-Quellen.

        Returns:
            List of {
                'name': 'Source name',
                'url': 'Base URL or API endpoint',
                'type': 'web' | 'api' | 'rss',
                'category': 'legal' | 'product' | 'industry' | 'customer',
                'frequency': 'daily' | 'weekly' | 'real-time'
            }
        """
        return [
            # Legal/Compliance
            {
                'name': 'DSGVO Updates',
                'url': 'https://www.datenschutz.org/aktuelles/',
                'type': 'web',
                'category': 'legal',
                'frequency': 'weekly'
            },
            {
                'name': 'EU-DSGVO Blog',
                'url': 'https://dsgvo-gesetz.de/category/news/',
                'type': 'rss',
                'category': 'legal',
                'frequency': 'weekly'
            },

            # Product/Tech Updates
            {
                'name': 'Python Release Notes',
                'url': 'https://www.python.org/downloads/',
                'type': 'web',
                'category': 'product',
                'frequency': 'weekly'
            },
            {
                'name': 'Flask Release Notes',
                'url': 'https://flask.palletsprojects.com/en/latest/changes/',
                'type': 'web',
                'category': 'product',
                'frequency': 'weekly'
            },

            # Industry News
            {
                'name': 'CRM Magazine',
                'url': 'https://www.destinationcrm.com/',
                'type': 'web',
                'category': 'industry',
                'frequency': 'daily'
            },

            # Security
            {
                'name': 'CVE Database',
                'url': 'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=python+flask',
                'type': 'api',
                'category': 'security',
                'frequency': 'daily'
            },
        ]

    def _load_monitoring_topics(self) -> List[str]:
        """
        Themen die der Agent aktiv überwachen soll.
        """
        return [
            # Legal
            "DSGVO Änderungen",
            "ePrivacy Verordnung",
            "Datenschutz Compliance",

            # Product
            "Flask Security Updates",
            "Python CVE",
            "SQLAlchemy Updates",

            # Industry
            "CRM Best Practices",
            "AI in Customer Service",
            "Lead Scoring Trends",

            # Business
            "B2B Sales Automation",
            "Customer Onboarding",
        ]

    async def run_daily_research(self) -> Dict[str, Any]:
        """
        Tägliche Research-Routine.

        Returns:
            {
                'new_articles': int,
                'updates_found': int,
                'sources_checked': int,
                'errors': List[str]
            }
        """
        results = {
            'new_articles': 0,
            'updates_found': 0,
            'sources_checked': 0,
            'errors': []
        }

        # Research alle konfigurierten Quellen
        for source in self.research_sources:
            try:
                # Check frequency
                if not self._should_check_source(source):
                    continue

                # Perform research
                findings = await self._research_source(source)

                # Process findings
                for finding in findings:
                    # Create Beta KB article
                    article_result = await self._create_beta_article(finding, source)

                    if article_result.is_ok():
                        results['new_articles'] += 1
                    else:
                        results['errors'].append(
                            f"Failed to create article from {source['name']}: {article_result.unwrap_err()}"
                        )

                results['sources_checked'] += 1

            except Exception as e:
                results['errors'].append(f"Error researching {source['name']}: {str(e)}")

        # Topic-based research (without specific source)
        for topic in self.monitoring_topics:
            try:
                topic_findings = await self._research_topic(topic)

                for finding in topic_findings:
                    article_result = await self._create_beta_article(finding, {'name': 'Topic Research'})

                    if article_result.is_ok():
                        results['updates_found'] += 1

            except Exception as e:
                results['errors'].append(f"Error researching topic '{topic}': {str(e)}")

        return results

    async def _research_source(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Research eine spezifische Quelle.

        Returns:
            List of findings {
                'title': str,
                'content': str,
                'url': str,
                'published_date': datetime,
                'relevance_score': float,
                'category': str
            }
        """
        if source['type'] == 'web':
            return await self._scrape_web_source(source)
        elif source['type'] == 'rss':
            return await self._parse_rss_feed(source)
        elif source['type'] == 'api':
            return await self._query_api_source(source)
        else:
            return []

    async def _scrape_web_source(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Scrape Web-Quelle und extrahiere relevante Informationen.
        """
        findings = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source['url'], timeout=30) as response:
                    if response.status != 200:
                        return []

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Extrahiere relevante Content (heuristisch)
                    # In Produktion: Spezifische Selektoren pro Quelle
                    articles = soup.find_all(['article', 'div'], class_=['post', 'article', 'news-item'])

                    for article in articles[:5]:  # Max 5 pro Source
                        # Extrahiere Titel, Content, URL
                        title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                        title = title_elem.get_text(strip=True) if title_elem else "Untitled"

                        content_elem = article.find(['p', 'div'], class_=['content', 'summary', 'excerpt'])
                        content = content_elem.get_text(strip=True) if content_elem else article.get_text(strip=True)[:500]

                        link = article.find('a')
                        url = link['href'] if link and link.get('href') else source['url']

                        # Vollständige URL
                        if url.startswith('/'):
                            from urllib.parse import urljoin
                            url = urljoin(source['url'], url)

                        # AI-Analyse: Ist das relevant?
                        relevance = await self._assess_relevance(title, content, source['category'])

                        if relevance['is_relevant'] and relevance['score'] > 0.6:
                            findings.append({
                                'title': title,
                                'content': content,
                                'url': url,
                                'published_date': datetime.now(timezone.utc),  # Ideal: Extrahieren aus HTML
                                'relevance_score': relevance['score'],
                                'category': source['category'],
                                'reason': relevance['reason']
                            })

        except Exception as e:
            import logging
            logging.error(f"Web scraping error for {source['url']}: {e}")

        return findings

    async def _parse_rss_feed(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Parse RSS/Atom Feed.
        """
        import feedparser

        findings = []

        try:
            feed = feedparser.parse(source['url'])

            for entry in feed.entries[:10]:  # Max 10 pro Feed
                title = entry.get('title', 'Untitled')
                content = entry.get('summary', entry.get('description', ''))
                url = entry.get('link', source['url'])
                published = entry.get('published_parsed')

                # Convert published to datetime
                if published:
                    published_date = datetime(*published[:6], tzinfo=timezone.utc)
                else:
                    published_date = datetime.now(timezone.utc)

                # Nur neuere Einträge (letzte 7 Tage)
                if (datetime.now(timezone.utc) - published_date).days > 7:
                    continue

                # AI-Relevanz-Check
                relevance = await self._assess_relevance(title, content, source['category'])

                if relevance['is_relevant'] and relevance['score'] > 0.6:
                    findings.append({
                        'title': title,
                        'content': content,
                        'url': url,
                        'published_date': published_date,
                        'relevance_score': relevance['score'],
                        'category': source['category'],
                        'reason': relevance['reason']
                    })

        except Exception as e:
            import logging
            logging.error(f"RSS parsing error for {source['url']}: {e}")

        return findings

    async def _assess_relevance(
        self,
        title: str,
        content: str,
        category: str
    ) -> Dict[str, Any]:
        """
        AI-basierte Relevanz-Bewertung.

        Returns:
            {
                'is_relevant': bool,
                'score': float (0.0-1.0),
                'reason': str
            }
        """
        prompt = f"""
Beurteile die Relevanz dieser Information für unser CRM Knowledge Base System.

Kategorie: {category}

Titel: {title}

Inhalt (Auszug):
{content[:500]}

Kriterien für Relevanz:
- Legal/Compliance: Betrifft DSGVO, Datenschutz, CRM-relevante Gesetze
- Product: Betrifft Python, Flask, SQLAlchemy, Security Updates
- Industry: CRM Best Practices, Sales Automation, Customer Service
- Customer: B2B Business Trends, Tools die Kunden verwenden könnten

Bewerte:
1. Ist das relevant für unser CRM System? (ja/nein)
2. Relevanz-Score (0.0 = irrelevant, 1.0 = sehr relevant)
3. Begründung

Return JSON:
{{
    "is_relevant": true/false,
    "score": 0.85,
    "reason": "Kurze Begründung...",
    "suggested_tags": ["tag1", "tag2"],
    "urgency": "low" | "medium" | "high"  // Wie zeitkritisch ist das?
}}
"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            # Fallback: Alles als potentiell relevant markieren
            return {
                'is_relevant': True,
                'score': 0.5,
                'reason': f'Error during assessment: {e}',
                'suggested_tags': [],
                'urgency': 'low'
            }

    async def _research_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Freie Topic-basierte Recherche (ohne spezifische Quelle).

        Nutzt Claude's web-search Fähigkeit oder externe APIs.
        """
        # Placeholder für echte Web-Search Implementation
        # In Produktion: Integration mit Perplexity API, Google Custom Search, etc.

        prompt = f"""
Recherchiere aktuelle Informationen (2024-2025) zum Thema: "{topic}"

Fokus auf:
- Änderungen in den letzten 6 Monaten
- Best Practices
- Regulatorische Updates
- Tool/Technology Updates

Gib 2-3 wichtige Findings zurück.

Return JSON:
{{
    "findings": [
        {{
            "title": "...",
            "summary": "...",
            "key_points": ["Point 1", "Point 2"],
            "sources": ["URL1", "URL2"],
            "date": "2024-12-15",
            "relevance": 0.85
        }},
        ...
    ]
}}
"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            result = json.loads(response.content[0].text)

            # Konvertiere zu standardisiertem Format
            findings = []
            for finding in result.get('findings', []):
                findings.append({
                    'title': finding['title'],
                    'content': finding['summary'] + '\n\nKey Points:\n' + '\n'.join(f"- {p}" for p in finding['key_points']),
                    'url': finding['sources'][0] if finding['sources'] else '',
                    'published_date': datetime.fromisoformat(finding['date']) if finding.get('date') else datetime.now(timezone.utc),
                    'relevance_score': finding.get('relevance', 0.7),
                    'category': 'research',
                    'reason': f'Topic research: {topic}'
                })

            return findings

        except Exception as e:
            import logging
            logging.error(f"Topic research error for '{topic}': {e}")
            return []

    async def _create_beta_article(
        self,
        finding: Dict[str, Any],
        source: Dict[str, str]
    ) -> Result[KnowledgeArticle, str]:
        """
        Erstelle Beta KB Article aus Research Finding.

        Beta Articles starten mit:
        - Status: 'beta'
        - verification_count: 1 (initial finding)
        - requires_verification: True
        """
        # Generiere strukturierten KB Content mit AI
        prompt = f"""
Erstelle einen strukturierten Knowledge Base Artikel aus diesem Research Finding:

Titel: {finding['title']}
Inhalt: {finding['content']}
Quelle: {source['name']}
URL: {finding.get('url', 'N/A')}
Kategorie: {finding['category']}

Erstelle:
1. Klaren, präzisen Titel
2. Vollständigen, gut strukturierten Content
3. Zusammenfassung (1 Satz)
4. Relevante Tags
5. Einschätzung ob Verfallsdatum sinnvoll (z.B. bei zeitkritischen Gesetzen)

Return JSON:
{{
    "title": "...",
    "content": "... (strukturiert mit Markdown)",
    "summary": "...",
    "tags": ["tag1", "tag2"],
    "needs_expiration": true/false,
    "suggested_expiration_days": 365,  // Falls needs_expiration=true
    "confidence": 0.75
}}
"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            article_data = json.loads(response.content[0].text)

            # Erstelle Beta Article
            article = KnowledgeArticle(
                title=article_data['title'],
                content=article_data['content'],
                summary=article_data['summary'],
                category=finding['category'],
                tags=article_data['tags'],
                source_type='research_agent',
                source_url=finding.get('url'),
                status='beta',  # BETA STATUS!
                verification_count=1,  # Erste Verifikation durch Research Agent
                requires_verification=True,
                confidence_score=article_data.get('confidence', 0.7),
                created_by='ResearchAgent',
                research_date=finding['published_date']
            )

            # Verfallsdatum falls nötig
            if article_data.get('needs_expiration'):
                expiration_days = article_data.get('suggested_expiration_days', 365)
                article.expiration_date = datetime.now(timezone.utc) + timedelta(days=expiration_days)
                article.auto_review_date = article.expiration_date - timedelta(days=30)  # 30 Tage vor Ablauf

            db.session.add(article)
            db.session.commit()

            # Erstelle Verification Entry
            verification = ArticleVerification(
                article_id=article.id,
                verification_source='research_agent',
                verification_type='initial_discovery',
                verified_by='ResearchAgent',
                source_url=finding.get('url'),
                notes=finding.get('reason', 'Initial discovery by research agent')
            )
            db.session.add(verification)
            db.session.commit()

            # Notify Team über neue Beta Article
            await self._notify_new_beta_article(article)

            return Ok(article)

        except Exception as e:
            return Err(f"Failed to create beta article: {str(e)}")

    async def _notify_new_beta_article(self, article: KnowledgeArticle) -> None:
        """
        Benachrichtige Team über neue Beta Article die Verifikation braucht.
        """
        import logging
        logging.info(
            f"🧪 New BETA KB Article: {article.id} - {article.title} "
            f"(Category: {article.category}, Confidence: {article.confidence_score:.2f})"
        )

        # TODO: Slack/Email notification
        # TODO: Dashboard notification badge

    def _should_check_source(self, source: Dict[str, str]) -> bool:
        """
        Check ob Source jetzt gecheckt werden soll basierend auf Frequency.
        """
        # Placeholder - in Produktion: Check last_checked timestamp
        frequency = source.get('frequency', 'daily')

        if frequency == 'real-time':
            return True
        elif frequency == 'daily':
            # Check ob heute schon gecheckt
            return True  # Simplified
        elif frequency == 'weekly':
            # Check ob diese Woche schon gecheckt
            return True  # Simplified

        return False

    async def research_customer_company(self, customer_id: int) -> List[Dict[str, Any]]:
        """
        On-demand research für spezifisches Kunden-Unternehmen.

        Use Case:
        - Vor wichtigem Sales Call
        - Bei Lead-Scoring
        - Für personalisierte Kommunikation
        """
        customer = Customer.query.get(customer_id)
        if not customer or not customer.company:
            return []

        company_name = customer.company

        # Research Company News
        findings = await self._research_topic(f"{company_name} news updates 2024 2025")

        # Erstelle Beta Articles für relevante Findings
        for finding in findings:
            finding['category'] = 'customer_intelligence'
            await self._create_beta_article(
                finding,
                {'name': f'Customer Research: {company_name}'}
            )

        return findings
```

---

## 🧪 Beta/Production Verification System

### Konzept

**Zwei-Stufen-System:**

1. **Beta KB** (Unverified)
   - Status: `beta`, `draft`
   - Neue Informationen landen hier
   - Mehrfach-Verifikation erforderlich
   - ⚠️ Mit Vorsicht nutzen (nur für informative Zwecke)

2. **Production KB** (Verified)
   - Status: `verified`, `published`
   - Nur nach mehrmaliger Bestätigung
   - ✅ Sicher für Automation und kritische Entscheidungen

### Erweiterte Datenmodelle

```python
class KnowledgeArticle(db.Model):
    """
    Erweitertes Datenmodell mit Verification & Expiration.
    """
    __tablename__ = 'kb_articles'

    id = db.Column(db.Integer, primary_key=True)

    # ... (bestehende Felder) ...

    # VERIFICATION SYSTEM (NEU)
    verification_count = db.Column(db.Integer, default=0)
    """Anzahl unabhängiger Verifikationen"""

    requires_verification = db.Column(db.Boolean, default=True)
    """True wenn Article Verifikation braucht bevor Production"""

    verification_threshold = db.Column(db.Integer, default=3)
    """Mindestanzahl Verifikationen für Production (Standard: 3)"""

    last_verified_at = db.Column(db.DateTime)
    """Zeitpunkt der letzten Verifikation"""

    # EXPIRATION SYSTEM (NEU)
    expiration_date = db.Column(db.DateTime, nullable=True)
    """Verfallsdatum (NULL = kein Ablauf)"""

    auto_review_date = db.Column(db.DateTime, nullable=True)
    """Datum für automatischen Review (z.B. 30 Tage vor Expiration)"""

    is_expired = db.Column(db.Boolean, default=False)
    """True wenn abgelaufen"""

    renewal_count = db.Column(db.Integer, default=0)
    """Wie oft wurde Article erneuert/verlängert"""

    # RESEARCH METADATA (NEU)
    source_url = db.Column(db.String(500))
    """URL der Original-Quelle (für Research Agent)"""

    research_date = db.Column(db.DateTime)
    """Wann wurde diese Info recherchiert/gefunden"""

    # Relationships
    verifications = db.relationship('ArticleVerification', backref='article',
                                   lazy='dynamic', cascade='all, delete-orphan')
    expiration_reviews = db.relationship('ExpirationReview', backref='article',
                                        lazy='dynamic', cascade='all, delete-orphan')

    def can_promote_to_production(self) -> bool:
        """
        Check ob Article bereit für Production ist.

        Kriterien:
        - verification_count >= verification_threshold
        - Verifikationen über Zeit verteilt (nicht alle am selben Tag)
        - Mindestens 2 unterschiedliche Verifikations-Quellen
        """
        if self.verification_count < self.verification_threshold:
            return False

        # Check zeitliche Verteilung
        verifications = self.verifications.order_by(ArticleVerification.created_at).all()

        if len(verifications) < self.verification_threshold:
            return False

        # Mindestens 2 Tage zwischen erster und letzter Verifikation
        first_verification = verifications[0].created_at
        last_verification = verifications[-1].created_at
        time_span = (last_verification - first_verification).days

        if time_span < 2:
            return False  # Zu schnell verifiziert - verdächtig

        # Mindestens 2 unterschiedliche Quellen
        unique_sources = set(v.verification_source for v in verifications)
        if len(unique_sources) < 2:
            return False  # Nur eine Quelle - nicht robust genug

        return True

    def is_expired_check(self) -> bool:
        """Check ob Article abgelaufen ist."""
        if not self.expiration_date:
            return False

        return datetime.now(timezone.utc) >= self.expiration_date

    def needs_review(self) -> bool:
        """Check ob Article Review braucht (vor Expiration)."""
        if not self.auto_review_date:
            return False

        return datetime.now(timezone.utc) >= self.auto_review_date


class ArticleVerification(db.Model):
    """
    Verifikations-Historie für KB Articles.

    Jede unabhängige Bestätigung wird hier geloggt.
    """
    __tablename__ = 'kb_verifications'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'), nullable=False)

    # Verification Details
    verification_source = db.Column(db.String(100), nullable=False)
    """Quelle der Verifikation: 'research_agent', 'manual', 'customer_feedback', 'ai_agent_usage'"""

    verification_type = db.Column(db.String(50))
    """Art: 'initial_discovery', 'cross_reference', 'manual_review', 'usage_confirmation'"""

    verified_by = db.Column(db.String(100))
    """User oder Agent Name"""

    source_url = db.Column(db.String(500))
    """URL/Quelle die diese Verifikation unterstützt"""

    confidence_delta = db.Column(db.Float)
    """Confidence-Änderung durch diese Verifikation (+0.1, etc.)"""

    notes = db.Column(db.Text)
    """Optionale Notizen zur Verifikation"""

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class ExpirationReview(db.Model):
    """
    Review-Historie für ablaufende Articles.
    """
    __tablename__ = 'kb_expiration_reviews'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'), nullable=False)

    # Review Details
    review_date = db.Column(db.DateTime, nullable=False)
    reviewed_by = db.Column(db.String(100))  # User oder 'ExpirationAgent'

    review_result = db.Column(db.String(50))
    """'renewed', 'extended', 'archived', 'deleted', 'still_valid'"""

    new_expiration_date = db.Column(db.DateTime, nullable=True)
    """Neues Verfallsdatum falls verlängert"""

    notes = db.Column(db.Text)
    """Begründung für Entscheidung"""

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

---

## 🔄 Verification Pipeline

### Automatische Verifikation

```python
class VerificationEngine:
    """
    Automatische und manuelle Verifikation von KB Articles.
    """

    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def verify_article(
        self,
        article: KnowledgeArticle,
        verification_source: str,
        verified_by: str,
        source_url: str = None,
        notes: str = None
    ) -> Result[ArticleVerification, str]:
        """
        Verifiziere Article und aktualisiere verification_count.

        Args:
            article: KB Article
            verification_source: 'research_agent', 'manual', 'customer_feedback', etc.
            verified_by: User/Agent name
            source_url: Optional URL die Verifikation unterstützt
            notes: Optional notes

        Returns:
            Ok(ArticleVerification) wenn erfolgreich
        """
        # Erstelle Verification Entry
        verification = ArticleVerification(
            article_id=article.id,
            verification_source=verification_source,
            verification_type='cross_reference',
            verified_by=verified_by,
            source_url=source_url,
            confidence_delta=0.1,  # +10% confidence per verification
            notes=notes
        )

        db.session.add(verification)

        # Update Article
        article.verification_count += 1
        article.last_verified_at = datetime.now(timezone.utc)

        # Erhöhe Confidence (max 1.0)
        article.confidence_score = min(1.0, article.confidence_score + 0.1)

        # Check ob Production-ready
        if article.can_promote_to_production() and article.status == 'beta':
            article.status = 'verified'
            article.requires_verification = False

            # Notify Team
            await self._notify_promoted_to_production(article)

        db.session.commit()

        return Ok(verification)

    async def cross_verify_with_web(self, article: KnowledgeArticle) -> Result[bool, str]:
        """
        Automatische Cross-Verifikation durch Web-Research.

        Nutzt Research Agent um dieselbe Info aus anderer Quelle zu finden.
        """
        # Research das Topic erneut
        research_agent = ResearchAgent()

        # Erstelle Search Query aus Article
        query = f"{article.title} {' '.join(article.tags or [])}"

        findings = await research_agent._research_topic(query)

        # Check ob Findings den Article bestätigen
        for finding in findings:
            similarity = await self._check_content_similarity(article.content, finding['content'])

            if similarity > 0.7:  # 70% Übereinstimmung
                # Automatische Verifikation
                await self.verify_article(
                    article=article,
                    verification_source='research_agent',
                    verified_by='AutoVerification',
                    source_url=finding.get('url'),
                    notes=f"Cross-verified via web research (similarity: {similarity:.2f})"
                )

                return Ok(True)

        return Err("No confirming sources found")

    async def _check_content_similarity(self, content1: str, content2: str) -> float:
        """
        AI-basierte Content-Ähnlichkeit (0.0-1.0).
        """
        prompt = f"""
Vergleiche diese beiden Texte und gib einen Similarity Score zurück.

Text 1:
{content1[:1000]}

Text 2:
{content2[:1000]}

Bewerte:
- Gleiche Fakten/Informationen? (wichtigster Faktor)
- Gleiche Schlussfolgerungen?
- Widersprüche?

Return JSON:
{{
    "similarity": 0.85,  // 0.0 = komplett unterschiedlich, 1.0 = identisch
    "matching_facts": ["Fact 1", "Fact 2"],
    "contradictions": ["..."] or [],
    "conclusion": "Same information from different sources"
}}
"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            result = json.loads(response.content[0].text)
            return result.get('similarity', 0.0)

        except Exception as e:
            return 0.0

    async def _notify_promoted_to_production(self, article: KnowledgeArticle) -> None:
        """
        Benachrichtige Team dass Beta Article zu Production promoted wurde.
        """
        import logging
        logging.info(
            f"✅ Article PROMOTED to Production: {article.id} - {article.title} "
            f"(Verifications: {article.verification_count})"
        )

        # TODO: Slack/Email notification
```

---

## ⏰ Expiration Management System

### Automatisches Lifecycle-Management

```python
class ExpirationAgent:
    """
    Automatisches Management von ablaufenden KB Articles.

    Läuft täglich:
    1. Finde Articles die bald ablaufen (auto_review_date erreicht)
    2. Versuche automatisch zu verifizieren ob noch gültig
    3. Notify Team für manuelle Review
    4. Archive/Delete expired articles
    """

    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.research_agent = ResearchAgent()
        self.verification_engine = VerificationEngine()

    async def run_daily_expiration_check(self) -> Dict[str, Any]:
        """
        Tägliche Expiration-Routine.
        """
        results = {
            'reviews_triggered': 0,
            'auto_renewed': 0,
            'archived': 0,
            'deleted': 0,
            'errors': []
        }

        # 1. Finde Articles die Review brauchen
        articles_needing_review = KnowledgeArticle.query.filter(
            KnowledgeArticle.auto_review_date <= datetime.now(timezone.utc),
            KnowledgeArticle.is_expired == False,
            KnowledgeArticle.status.in_(['verified', 'published'])
        ).all()

        for article in articles_needing_review:
            try:
                review_result = await self._review_expiring_article(article)

                if review_result == 'auto_renewed':
                    results['auto_renewed'] += 1
                elif review_result == 'needs_manual_review':
                    results['reviews_triggered'] += 1

            except Exception as e:
                results['errors'].append(f"Error reviewing article {article.id}: {e}")

        # 2. Finde abgelaufene Articles
        expired_articles = KnowledgeArticle.query.filter(
            KnowledgeArticle.expiration_date <= datetime.now(timezone.utc),
            KnowledgeArticle.is_expired == False
        ).all()

        for article in expired_articles:
            try:
                # Markiere als expired
                article.is_expired = True

                # Entscheide: Archive oder Delete?
                if article.view_count > 10 or article.helpful_count > 5:
                    # Wertvoller Article - archivieren
                    article.status = 'archived'
                    results['archived'] += 1
                else:
                    # Wenig genutzt - löschen
                    db.session.delete(article)
                    results['deleted'] += 1

                db.session.commit()

            except Exception as e:
                results['errors'].append(f"Error handling expired article {article.id}: {e}")

        return results

    async def _review_expiring_article(self, article: KnowledgeArticle) -> str:
        """
        Review Article der bald abläuft.

        Returns:
            'auto_renewed' - Automatisch verlängert
            'needs_manual_review' - Manuelle Review erforderlich
            'archived' - Nicht mehr relevant
        """
        # 1. Versuche automatische Verifikation via Web-Research
        verification_result = await self.verification_engine.cross_verify_with_web(article)

        if verification_result.is_ok():
            # Info noch aktuell! Automatisch verlängern
            await self._renew_article(
                article=article,
                new_expiration_days=365,
                reviewed_by='ExpirationAgent',
                notes='Auto-renewed after successful web verification'
            )
            return 'auto_renewed'

        # 2. AI-Check: Ist die Info möglicherweise veraltet?
        obsolescence_check = await self._check_if_obsolete(article)

        if obsolescence_check['is_obsolete']:
            # Info veraltet - archivieren
            article.status = 'archived'
            article.is_expired = True

            review = ExpirationReview(
                article_id=article.id,
                review_date=datetime.now(timezone.utc),
                reviewed_by='ExpirationAgent',
                review_result='archived',
                notes=f"Auto-archived: {obsolescence_check['reason']}"
            )
            db.session.add(review)
            db.session.commit()

            return 'archived'

        # 3. Unsicher - manuelle Review anfordern
        await self._request_manual_review(article, obsolescence_check)
        return 'needs_manual_review'

    async def _check_if_obsolete(self, article: KnowledgeArticle) -> Dict[str, Any]:
        """
        AI-Check ob Information möglicherweise veraltet ist.
        """
        prompt = f"""
Prüfe ob diese Knowledge Base Information möglicherweise veraltet ist:

Titel: {article.title}
Kategorie: {article.category}
Erstellt: {article.created_at.strftime('%Y-%m-%d')}
Letztes Update: {article.updated_at.strftime('%Y-%m-%d')}
Content:
{article.content[:1000]}

Expiration Date: {article.expiration_date.strftime('%Y-%m-%d') if article.expiration_date else 'None'}

Bewerte:
1. Ist die Information zeitgebunden? (z.B. Gesetz mit Gültigkeit)
2. Könnte sich etwas geändert haben seit Erstellung?
3. Ist die Info wahrscheinlich noch aktuell?

Return JSON:
{{
    "is_obsolete": true/false,
    "confidence": 0.85,
    "reason": "Begründung...",
    "recommendation": "renew" | "archive" | "manual_review",
    "suggested_new_expiration_days": 365
}}
"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            return {
                'is_obsolete': False,
                'confidence': 0.0,
                'reason': f'Error during check: {e}',
                'recommendation': 'manual_review'
            }

    async def _renew_article(
        self,
        article: KnowledgeArticle,
        new_expiration_days: int,
        reviewed_by: str,
        notes: str
    ) -> None:
        """
        Verlängere Article Expiration Date.
        """
        old_expiration = article.expiration_date
        new_expiration = datetime.now(timezone.utc) + timedelta(days=new_expiration_days)

        article.expiration_date = new_expiration
        article.auto_review_date = new_expiration - timedelta(days=30)
        article.renewal_count += 1

        review = ExpirationReview(
            article_id=article.id,
            review_date=datetime.now(timezone.utc),
            reviewed_by=reviewed_by,
            review_result='renewed',
            new_expiration_date=new_expiration,
            notes=notes
        )
        db.session.add(review)
        db.session.commit()

        import logging
        logging.info(
            f"📅 Article {article.id} renewed: "
            f"{old_expiration.strftime('%Y-%m-%d')} → {new_expiration.strftime('%Y-%m-%d')}"
        )

    async def _request_manual_review(
        self,
        article: KnowledgeArticle,
        obsolescence_check: Dict[str, Any]
    ) -> None:
        """
        Fordere manuelle Review an für unsichere Fälle.
        """
        import logging
        logging.warning(
            f"⚠️ Manual review required for article {article.id} - {article.title}\n"
            f"Reason: {obsolescence_check.get('reason', 'Unknown')}\n"
            f"Recommendation: {obsolescence_check.get('recommendation', 'review')}"
        )

        # TODO: Slack/Email notification mit Review-Link
        # TODO: Dashboard notification badge
```

---

## 🎯 Anwendungsfälle

### Use Case 1: Gesetzesänderung (DSGVO)

```
Tag 1:
- Research Agent findet neue DSGVO-Richtlinie auf EU-Webseite
- Erstellt Beta Article "DSGVO Änderung: Cookie-Consent ab 2025"
- Status: beta, verification_count: 1
- Expiration: 2025-12-31 (Gesetz zeitlich begrenzt)

Tag 3:
- Research Agent findet selbe Info auf anderem Portal
- Verification +1 (verification_count: 2)

Tag 7:
- Mitarbeiter bestätigt manuell (gelesen auf offizieller EU-Seite)
- Verification +1 (verification_count: 3)
- ✅ PROMOTION zu Production (verified)
- Alle AI Agents können jetzt sicher darauf zugreifen

2025-12-01:
- Auto-review Date erreicht
- Expiration Agent prüft via Web ob Gesetz verlängert wurde
- Falls ja: Renew für weitere 12 Monate
- Falls nein: Archive
```

### Use Case 2: Customer Intelligence

```
Tag 1:
- Sales Agent bereitet Call mit "ACME Corp" vor
- Ruft ResearchAgent.research_customer_company(acme_id)
- Research Agent findet: "ACME Corp acquires competitor XYZ"
- Erstellt Beta Article
- Status: beta, verification_count: 1

Tag 2:
- Anderer Mitarbeiter sieht Beta Article im Dashboard
- Liest Original-Artikel, bestätigt
- Verification +1

Tag 5:
- Research Agent findet Follow-up Article
- Verification +1
- ✅ PROMOTION zu Production

Im Sales Call:
- Sales Agent sieht verifizierte Info
- Kann gezielt auf Akquisition eingehen
- Bessere Gesprächsqualität
```

### Use Case 3: Security CVE

```
Tag 1 (14:00):
- Research Agent findet kritisches Flask CVE
- Erstellt Beta Article "Flask Security CVE-2024-XXXXX"
- Status: beta, verification_count: 1
- Urgency: HIGH
- Expiration: 90 Tage (Security Patches haben kurzes Fenster)

Tag 1 (15:00):
- Automatische Cross-Verification findet CVE auch auf nvd.nist.gov
- Verification +1

Tag 1 (16:00):
- DevOps Team bestätigt manuell (checked Flask GitHub)
- Verification +1
- ✅ PROMOTION zu Production (innerhalb 2h!)

Tag 2:
- Analytics Agent nutzt verified Info um Security Report zu erstellen
- Empfiehlt Update

Tag 90:
- Auto-review prüft ob CVE noch relevant
- Flask bereits geupdated → Archive Article
```

---

## 📊 Analytics für Verification System

```python
class VerificationAnalytics:
    """
    Analytics für Beta/Production Pipeline.
    """

    @staticmethod
    def get_verification_metrics() -> Dict[str, Any]:
        """
        Metriken für Verification System.
        """
        # Beta Articles (waiting for verification)
        beta_count = KnowledgeArticle.query.filter_by(status='beta').count()

        # Production Articles
        verified_count = KnowledgeArticle.query.filter_by(status='verified').count()

        # Average time to production
        promoted_articles = KnowledgeArticle.query.filter(
            KnowledgeArticle.status == 'verified',
            KnowledgeArticle.created_at >= datetime.now(timezone.utc) - timedelta(days=90)
        ).all()

        avg_time_to_production = 0
        if promoted_articles:
            times = []
            for article in promoted_articles:
                first_verification = article.verifications.order_by(
                    ArticleVerification.created_at
                ).first()
                last_verification = article.verifications.order_by(
                    ArticleVerification.created_at.desc()
                ).first()

                if first_verification and last_verification:
                    time_diff = (last_verification.created_at - first_verification.created_at).days
                    times.append(time_diff)

            avg_time_to_production = sum(times) / len(times) if times else 0

        # Expiring soon
        expiring_soon = KnowledgeArticle.query.filter(
            KnowledgeArticle.expiration_date.between(
                datetime.now(timezone.utc),
                datetime.now(timezone.utc) + timedelta(days=30)
            ),
            KnowledgeArticle.is_expired == False
        ).count()

        # Already expired
        expired = KnowledgeArticle.query.filter_by(is_expired=True).count()

        return {
            'beta_articles': beta_count,
            'verified_articles': verified_count,
            'avg_days_to_production': round(avg_time_to_production, 1),
            'expiring_within_30_days': expiring_soon,
            'expired_archived': expired,
            'verification_pipeline_health': 'healthy' if avg_time_to_production < 7 else 'slow'
        }

    @staticmethod
    def get_verification_sources_breakdown() -> Dict[str, int]:
        """
        Welche Quellen verifizieren am meisten?
        """
        results = db.session.query(
            ArticleVerification.verification_source,
            db.func.count(ArticleVerification.id)
        ).group_by(
            ArticleVerification.verification_source
        ).all()

        return {source: count for source, count in results}
```

---

## 🚀 Implementation Roadmap

### Phase 1: Research Agent (Wochen 1-2)
- [ ] ResearchAgent Basis-Implementation
- [ ] Web Scraping + RSS Parsing
- [ ] AI Relevanz-Bewertung
- [ ] Beta Article Creation
- [ ] Scheduled Daily Runs

### Phase 2: Verification System (Wochen 3-4)
- [ ] Erweiterte Datenmodelle (ArticleVerification, ExpirationReview)
- [ ] VerificationEngine Implementation
- [ ] Auto-Promotion Beta → Production
- [ ] Cross-Verification via Web
- [ ] Manual Verification UI

### Phase 3: Expiration Management (Wochen 5-6)
- [ ] ExpirationAgent Implementation
- [ ] Auto-Review vor Ablauf
- [ ] Renewal Workflows
- [ ] Archival Logic
- [ ] Notification System

### Phase 4: UI & Integration (Wochen 7-8)
- [ ] Beta/Production Toggle in Search
- [ ] Verification Status Badges
- [ ] Manual Review Dashboard
- [ ] Expiration Calendar View
- [ ] Research Agent Control Panel

### Phase 5: Advanced Features (Wochen 9-10)
- [ ] Customer Company Research
- [ ] Real-time Topic Monitoring
- [ ] Contradiction Detection
- [ ] Version Diffing
- [ ] Analytics Dashboard

---

## 💰 Kosten (Zusätzlich zu Base KB System)

**Research Agent:**
- Web Scraping: Free (self-hosted)
- AI Analysis: ~1000 articles/month × $0.02 = **$20/month**

**Verification:**
- Cross-Verification: ~500 checks/month × $0.01 = **$5/month**

**Expiration Management:**
- Auto-Reviews: ~200 reviews/month × $0.01 = **$2/month**

### Total Additional Cost: **~$27/month**

### Combined System Cost:
- Base KB: €32-102/month
- Research + Verification: €27/month
- **Total: €59-129/month**

### ROI bleibt extrem hoch:
- Time saved: 10h/week = €2,000/month
- Cost: €129/month
- **Net savings: €1,871/month**
- **ROI: 1,449%** 🚀

---

## 🎯 Success Metrics

### Neue KPIs:

1. **Verification Velocity**
   - Target: <7 Tage von Beta → Production
   - Measure: Durchschnittliche Zeit für 3 Verifikationen

2. **Auto-Verification Rate**
   - Target: 40% automatic verifications
   - Measure: `auto_verifications / total_verifications`

3. **Expiration Management**
   - Target: 90% auto-renewed (kein manueller Eingriff)
   - Measure: `auto_renewed / total_expirations`

4. **Information Freshness**
   - Target: 95% of articles <6 Monate alt
   - Measure: Articles updated in last 6 months

5. **Beta Quality**
   - Target: 60% Beta articles promoted to Production
   - Measure: `promoted / total_beta_created`

---

## 🔒 Security Considerations

1. **Web Scraping**: Rate Limiting, robots.txt compliance
2. **Source Trust**: Whitelist vertrauenswürdiger Domains
3. **Content Sanitization**: XSS Prevention bei externen Inhalten
4. **API Keys**: Sichere Verwaltung für externe APIs
5. **Data Privacy**: Keine persönlichen Daten in Research speichern

---

## 📝 Zusammenfassung

### Das erweiterte KB System bietet:

✅ **Research Agent** - Kontinuierliche Recherche und KB-Aufbau
✅ **Beta/Production Pipeline** - Fehlinformationen vermeiden durch Mehrfach-Verifikation
✅ **Expiration Management** - Automatisches Lifecycle-Management
✅ **Cross-Verification** - Mehrere Quellen über Zeit
✅ **Compliance-Ready** - Für zeitkritische/gesetzliche Informationen
✅ **Auto-Renewal** - Intelligente Verlängerung relevanter Infos
✅ **Quality Gates** - Nur verifizierte Infos für kritische Automation

### Nächste Schritte:
1. Review dieser Erweiterung
2. Entscheidung über Priorität (nach Bug Fixes?)
3. Integration in 12-Wochen Roadmap des Base KB Systems
4. Start Implementation

---

**Erstellt**: 2025-12-25
**Autor**: Claude Development Team
**Version**: KB Research & Verification System v1.0
**Status**: Ready for Implementation 🚀
**Abhängig von**: KNOWLEDGE_BASE_SYSTEM.md (Base System)
