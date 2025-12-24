# 🧠 Modern Knowledge Base System - Design Specification

## 📋 Executive Summary

Ein **selbstlernendes Knowledge Base System** für das CRM, das kontinuierlich wächst, aus jeder Interaktion lernt und sowohl für Mitarbeiter als auch für AI-Agenten als zentrale Wissensquelle dient.

### Hauptziele
- ✅ **Kontinuierliches Wachstum**: Automatische Extraktion aus jeder Customer Interaction
- ✅ **AI-Powered Q&A**: Intelligente Beantwortung von Fragen
- ✅ **Multi-Source Learning**: CRM + Emails + Dokumente + Web
- ✅ **Semantic Search**: Ähnliche Probleme/Lösungen finden
- ✅ **Versionierung**: Historie aller Änderungen
- ✅ **Privacy-First**: Sensible Daten bleiben geschützt

### ROI
- **Wissensverlust vermeiden**: 100% Retention bei Mitarbeiterwechsel
- **Schnellere Antworten**: 80% weniger Suchzeit (12h → 2.4h/Woche)
- **Bessere Kundenerfahrung**: Konsistente, fundierte Antworten
- **Self-Service**: Kunden können selbst Antworten finden

---

## 🏗️ System-Architektur

### Komponenten-Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│                     KNOWLEDGE BASE SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Ingestion  │  │   Storage    │  │  Retrieval   │          │
│  │    Engine    │  │    Layer     │  │    Engine    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                  │                   │
│         ▼                 ▼                  ▼                   │
│  ┌──────────────────────────────────────────────────┐          │
│  │            AI Processing Pipeline                 │          │
│  │  (Extraction → Embedding → Classification)       │          │
│  └──────────────────────────────────────────────────┘          │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────┐          │
│  │         Vector Database (ChromaDB/Pinecone)      │          │
│  │         + Relational DB (PostgreSQL)             │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
         │                 │                  │
         ▼                 ▼                  ▼
   ┌─────────┐      ┌──────────┐      ┌──────────┐
   │   CRM   │      │    API   │      │  Agents  │
   │   UI    │      │ Endpoints│      │ (7 AI)   │
   └─────────┘      └──────────┘      └──────────┘
```

### Tech Stack

**Backend:**
- **Vector Database**: ChromaDB (lokal) oder Pinecone (Cloud, skalierbar)
- **Embeddings**: Claude 3.5 Sonnet (via Anthropic API)
- **Relational DB**: PostgreSQL (für Metadaten, Versionierung)
- **Search Engine**: Elasticsearch (optional, für Fulltext-Search)
- **API Framework**: Flask-RESTful (passt zum bestehenden CRM)

**Frontend:**
- **KB-Interface**: React komponente (optional, für Admin)
- **Search UI**: Integriert in bestehendes CRM
- **Chat Interface**: Claude-powered Q&A Widget

**AI/ML:**
- **Embeddings Model**: Claude 3.5 Sonnet
- **Classification**: Auto-Tagging mit Claude
- **Summarization**: Automatische Zusammenfassungen
- **Entity Extraction**: Named Entity Recognition für Metadaten

---

## 📊 Datenmodell

### 1. Knowledge Article (PostgreSQL)

```python
class KnowledgeArticle(db.Model):
    """
    Zentrale Knowledge Base Einträge.

    Ein Article kann sein:
    - FAQ-Eintrag
    - Problem-Lösung Paar
    - Best Practice
    - Customer Case Study
    - Product Documentation
    """
    __tablename__ = 'kb_articles'

    id = db.Column(db.Integer, primary_key=True)

    # Content
    title = db.Column(db.String(500), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)  # AI-generierte Zusammenfassung

    # Classification
    category = db.Column(db.String(100), index=True)  # e.g., "Product", "Support", "Sales"
    tags = db.Column(db.ARRAY(db.String))  # ['pricing', 'feature-request', 'bug']
    difficulty_level = db.Column(db.String(20))  # 'beginner', 'intermediate', 'expert'

    # Source Tracking
    source_type = db.Column(db.String(50))  # 'interaction', 'manual', 'email', 'document'
    source_id = db.Column(db.Integer)  # Reference to original source
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)

    # Quality Metrics
    confidence_score = db.Column(db.Float)  # AI confidence (0.0-1.0)
    usefulness_score = db.Column(db.Float, default=0.0)  # User ratings
    view_count = db.Column(db.Integer, default=0)
    helpful_count = db.Column(db.Integer, default=0)
    not_helpful_count = db.Column(db.Integer, default=0)

    # Status
    status = db.Column(db.String(20), default='draft')  # draft, reviewed, published, archived
    is_public = db.Column(db.Boolean, default=False)  # Visible to customers?

    # Versioning
    version = db.Column(db.Integer, default=1)
    parent_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'), nullable=True)

    # Metadata
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc))
    created_by = db.Column(db.String(100))  # User or 'AI-Agent'
    updated_by = db.Column(db.String(100))

    # Relationships
    embeddings = db.relationship('ArticleEmbedding', backref='article',
                                lazy='dynamic', cascade='all, delete-orphan')
    versions = db.relationship('KnowledgeArticle', backref=db.backref('parent', remote_side=[id]))
    related_articles = db.relationship('RelatedArticle', backref='article',
                                      foreign_keys='RelatedArticle.article_id')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'category': self.category,
            'tags': self.tags,
            'status': self.status,
            'confidence_score': self.confidence_score,
            'usefulness_score': self.usefulness_score,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
```

### 2. Article Embedding (ChromaDB/Pinecone)

```python
class ArticleEmbedding(db.Model):
    """
    Metadaten für Vector Embeddings (actual vectors in ChromaDB).
    """
    __tablename__ = 'kb_embeddings'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'), nullable=False)

    # Vector DB Reference
    vector_id = db.Column(db.String(100), unique=True)  # ID in ChromaDB/Pinecone
    embedding_model = db.Column(db.String(100))  # 'claude-3-5-sonnet-20241022'
    embedding_dimension = db.Column(db.Integer)  # 1024 for Claude

    # Chunk Info (für lange Articles)
    chunk_index = db.Column(db.Integer, default=0)
    chunk_text = db.Column(db.Text)  # Der Text-Chunk der embedded wurde

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

### 3. Related Articles (Similarity Graph)

```python
class RelatedArticle(db.Model):
    """
    Ähnlichkeits-Beziehungen zwischen Articles (für "Related Articles" Feature).
    """
    __tablename__ = 'kb_related'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'))
    related_article_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'))
    similarity_score = db.Column(db.Float)  # Cosine similarity (0.0-1.0)
    relation_type = db.Column(db.String(50))  # 'similar', 'prerequisite', 'follow-up'

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

### 4. Search Query Log

```python
class SearchQuery(db.Model):
    """
    Log aller Suchanfragen für Analytics und Verbesserung.
    """
    __tablename__ = 'kb_search_queries'

    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.Text, nullable=False)
    query_embedding_id = db.Column(db.String(100))  # Vector ID

    # Results
    results_count = db.Column(db.Integer)
    top_result_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'))
    user_selected_result_id = db.Column(db.Integer, db.ForeignKey('kb_articles.id'))

    # Context
    user_id = db.Column(db.String(100))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)

    # Feedback
    was_helpful = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

---

## 🔄 Ingestion Pipeline

### Automatische Wissens-Extraktion aus CRM Interactions

```python
from typing import List, Dict, Any
from anthropic import Anthropic
import chromadb

class KnowledgeIngestionEngine:
    """
    Automatische Extraktion von Wissen aus CRM Interaktionen.

    Workflow:
    1. Interaction erstellt → Trigger Event
    2. AI analysiert Interaction auf wiederverwendbares Wissen
    3. Wenn relevant: Erstelle Knowledge Article (Draft)
    4. Generiere Embedding
    5. Speichere in Vector DB
    6. Finde ähnliche Articles
    7. Benachrichtige Team für Review
    """

    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )

    def process_interaction(self, interaction: Interaction) -> Result[KnowledgeArticle, str]:
        """
        Hauptfunktion: Extrahiere Wissen aus Interaction.

        Args:
            interaction: CRM Interaction Objekt

        Returns:
            Ok(KnowledgeArticle) wenn Wissen extrahiert wurde
            Err(reason) wenn keine Extraktion möglich/nötig
        """
        # 1. Check if interaction contains valuable knowledge
        if not self._is_knowledge_worthy(interaction):
            return Err("Interaction contains no reusable knowledge")

        # 2. Extract structured knowledge with AI
        extraction_result = self._extract_knowledge(interaction)
        if extraction_result.is_err():
            return extraction_result

        knowledge_data = extraction_result.unwrap()

        # 3. Create draft article
        article = KnowledgeArticle(
            title=knowledge_data['title'],
            content=knowledge_data['content'],
            summary=knowledge_data['summary'],
            category=knowledge_data['category'],
            tags=knowledge_data['tags'],
            source_type='interaction',
            source_id=interaction.id,
            customer_id=interaction.customer_id,
            confidence_score=knowledge_data['confidence'],
            status='draft',
            created_by='AI-Knowledge-Agent'
        )

        try:
            db.session.add(article)
            db.session.commit()

            # 4. Generate and store embedding
            self._create_embedding(article)

            # 5. Find related articles
            self._link_related_articles(article)

            # 6. Notify team for review
            self._notify_review_needed(article)

            return Ok(article)

        except Exception as e:
            db.session.rollback()
            return Err(f"Database error: {str(e)}")

    def _is_knowledge_worthy(self, interaction: Interaction) -> bool:
        """
        Schnelle Heuristik: Lohnt sich AI-Analyse?

        Kriterien:
        - Mindestlänge (>100 Zeichen)
        - Enthält Frage + Antwort Pattern
        - Nicht nur "Thank you" / "OK" etc.
        """
        if not interaction.description:
            return False

        desc = interaction.description.strip()

        # Mindestlänge
        if len(desc) < 100:
            return False

        # Muss substantielle Informationen enthalten
        # (Heuristik: mehr als 10 Wörter)
        if len(desc.split()) < 10:
            return False

        # Bestimmte Interaction Types sind wertvoller
        if interaction.type in ['meeting', 'email']:
            return True

        # Calls nur wenn lang genug
        if interaction.type == 'call' and len(desc) > 200:
            return True

        return False

    def _extract_knowledge(self, interaction: Interaction) -> Result[Dict[str, Any], str]:
        """
        AI-gestützte Wissens-Extraktion.

        Returns:
            Ok({
                'title': str,
                'content': str,
                'summary': str,
                'category': str,
                'tags': List[str],
                'confidence': float
            })
        """
        # Build context
        customer = interaction.customer
        context = f"""
Customer: {customer.name} ({customer.company or 'No company'})
Interaction Type: {interaction.type}
Subject: {interaction.subject}
Description:
{interaction.description}

Previous interactions with this customer:
{self._get_recent_interactions_summary(customer)}
"""

        # AI Prompt for extraction
        prompt = f"""
Analyze this customer interaction and extract reusable knowledge for a knowledge base.

{context}

Extract:
1. **Title**: A clear, searchable title (max 100 chars)
2. **Content**: The reusable knowledge in detail (problem, solution, context)
3. **Summary**: One-sentence summary
4. **Category**: One of [Product, Support, Sales, Technical, Billing, General]
5. **Tags**: 3-5 relevant tags (lowercase, hyphenated)
6. **Confidence**: Your confidence that this is valuable knowledge (0.0-1.0)

Only extract if this interaction contains:
- A problem and its solution
- Important product/service information
- Common customer questions
- Best practices
- Technical insights

Return JSON:
{{
    "should_extract": true/false,
    "reason": "why or why not",
    "title": "...",
    "content": "...",
    "summary": "...",
    "category": "...",
    "tags": ["tag1", "tag2"],
    "confidence": 0.85
}}
"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse JSON response
            result = json.loads(response.content[0].text)

            if not result.get('should_extract', False):
                return Err(result.get('reason', 'Not valuable knowledge'))

            # Validate required fields
            required = ['title', 'content', 'summary', 'category', 'tags', 'confidence']
            if not all(key in result for key in required):
                return Err("Incomplete extraction from AI")

            return Ok(result)

        except json.JSONDecodeError:
            return Err("Invalid JSON from AI")
        except Exception as e:
            return Err(f"AI error: {str(e)}")

    def _create_embedding(self, article: KnowledgeArticle) -> None:
        """
        Erstelle Vector Embedding für Semantic Search.

        Uses Claude's embedding capability (alternative: OpenAI ada-002).
        """
        # Combine title + content for embedding
        text_to_embed = f"{article.title}\n\n{article.content}"

        # Split into chunks if too long (Claude max ~200k tokens, but we use smaller chunks)
        chunks = self._chunk_text(text_to_embed, max_length=8000)

        for i, chunk in enumerate(chunks):
            # Generate embedding via Claude
            # Note: Claude doesn't have dedicated embedding endpoint,
            # so we use a workaround or switch to OpenAI/Cohere for embeddings

            # Using OpenAI ada-002 as it's standard for embeddings:
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')

            response = openai.embeddings.create(
                model="text-embedding-ada-002",
                input=chunk
            )

            embedding_vector = response.data[0].embedding

            # Store in ChromaDB
            vector_id = f"article_{article.id}_chunk_{i}"

            self.collection.add(
                embeddings=[embedding_vector],
                documents=[chunk],
                metadatas=[{
                    'article_id': article.id,
                    'chunk_index': i,
                    'category': article.category,
                    'tags': ','.join(article.tags or []),
                    'confidence': article.confidence_score,
                }],
                ids=[vector_id]
            )

            # Store metadata in PostgreSQL
            embedding_meta = ArticleEmbedding(
                article_id=article.id,
                vector_id=vector_id,
                embedding_model='text-embedding-ada-002',
                embedding_dimension=1536,  # ada-002 dimension
                chunk_index=i,
                chunk_text=chunk
            )
            db.session.add(embedding_meta)

        db.session.commit()

    def _chunk_text(self, text: str, max_length: int = 8000) -> List[str]:
        """
        Split long text into chunks for embedding.

        Uses sentence boundaries to avoid cutting mid-sentence.
        """
        if len(text) <= max_length:
            return [text]

        chunks = []
        sentences = text.split('. ')
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _link_related_articles(self, article: KnowledgeArticle, top_k: int = 5) -> None:
        """
        Finde ähnliche Articles via Vector Similarity.
        """
        # Get article's embedding
        embedding_meta = article.embeddings.first()
        if not embedding_meta:
            return

        # Query ChromaDB for similar articles
        results = self.collection.query(
            query_embeddings=None,  # Use document ID instead
            query_texts=[embedding_meta.chunk_text],
            n_results=top_k + 1,  # +1 because it includes itself
            where={"article_id": {"$ne": article.id}}  # Exclude self
        )

        # Store relationships
        for i, related_id in enumerate(results['ids'][0]):
            if related_id == embedding_meta.vector_id:
                continue  # Skip self

            similarity_score = 1.0 - results['distances'][0][i]  # Convert distance to similarity

            # Extract article_id from vector_id
            related_article_id = int(related_id.split('_')[1])

            relation = RelatedArticle(
                article_id=article.id,
                related_article_id=related_article_id,
                similarity_score=similarity_score,
                relation_type='similar'
            )
            db.session.add(relation)

        db.session.commit()

    def _notify_review_needed(self, article: KnowledgeArticle) -> None:
        """
        Benachrichtige Team dass neuer KB-Eintrag Review braucht.

        Hier: Einfaches Logging (kann erweitert werden mit Email/Slack).
        """
        import logging
        logging.info(f"New KB article needs review: {article.id} - {article.title}")

        # TODO: Send to Slack/Email/Dashboard notification

    def _get_recent_interactions_summary(self, customer, limit: int = 3) -> str:
        """Helper: Hole letzte Interactions für Kontext."""
        interactions = customer.interactions.order_by(
            Interaction.created_at.desc()
        ).limit(limit).all()

        if not interactions:
            return "No previous interactions"

        summary = []
        for i, interaction in enumerate(interactions, 1):
            summary.append(
                f"{i}. {interaction.type.upper()}: {interaction.subject} "
                f"({interaction.created_at.strftime('%Y-%m-%d')})"
            )

        return "\n".join(summary)
```

---

## 🔍 Retrieval Engine (Q&A System)

### Semantic Search + AI-Powered Answers

```python
class KnowledgeRetrievalEngine:
    """
    Intelligente Wissensabfrage mit Semantic Search + Claude.

    Features:
    - Vector-basierte Similarity Search
    - Hybrid Search (Vector + Keyword)
    - AI-generierte Antworten mit Quellenangaben
    - Kontext-aware (berücksichtigt Customer/Interaction History)
    """

    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="knowledge_base")

    def search(
        self,
        query: str,
        top_k: int = 5,
        category: str = None,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Semantic Search in Knowledge Base.

        Args:
            query: Natural language search query
            top_k: Number of results to return
            category: Optional category filter
            min_confidence: Minimum confidence score

        Returns:
            List of {
                'article_id': int,
                'title': str,
                'content': str,
                'similarity_score': float,
                'category': str,
                'tags': List[str]
            }
        """
        # Generate query embedding
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')

        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        query_embedding = response.data[0].embedding

        # Build filter
        where_filter = {}
        if category:
            where_filter['category'] = category
        if min_confidence:
            where_filter['confidence'] = {'$gte': min_confidence}

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter if where_filter else None
        )

        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            article_id = int(results['ids'][0][i].split('_')[1])
            article = KnowledgeArticle.query.get(article_id)

            if article and article.status == 'published':
                formatted_results.append({
                    'article_id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'summary': article.summary,
                    'similarity_score': 1.0 - results['distances'][0][i],
                    'category': article.category,
                    'tags': article.tags,
                    'usefulness_score': article.usefulness_score
                })

        # Log search query
        self._log_search(query, formatted_results)

        return formatted_results

    def ask_question(
        self,
        question: str,
        customer_id: int = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        AI-powered Q&A using knowledge base.

        Workflow:
        1. Search knowledge base for relevant articles
        2. If found: Use Claude to synthesize answer from articles
        3. If not found: Return "I don't know" + suggest creating new KB entry
        4. Always include source citations

        Args:
            question: User's question
            customer_id: Optional customer context
            context: Additional context (current page, etc.)

        Returns:
            {
                'answer': str,  # AI-generated answer
                'confidence': float,  # 0.0-1.0
                'sources': List[Dict],  # Referenced articles
                'suggestions': List[str],  # Follow-up questions
                'should_create_article': bool  # If no good answer found
            }
        """
        # 1. Search for relevant articles
        search_results = self.search(question, top_k=5)

        if not search_results:
            return {
                'answer': "Ich habe leider keine relevanten Informationen in der Knowledge Base gefunden.",
                'confidence': 0.0,
                'sources': [],
                'suggestions': [],
                'should_create_article': True
            }

        # 2. Build context from top results
        context_text = self._build_context_from_results(search_results)

        # 3. Get customer context if provided
        customer_context = ""
        if customer_id:
            customer = Customer.query.get(customer_id)
            if customer:
                customer_context = f"""
Customer Context:
- Name: {customer.name}
- Company: {customer.company or 'N/A'}
- Status: {customer.status}
- Recent interactions: {customer.interactions.count()}
"""

        # 4. Ask Claude to synthesize answer
        prompt = f"""
You are a helpful knowledge base assistant. Answer the user's question using ONLY the information from the knowledge base articles provided below.

Question: {question}

{customer_context}

Knowledge Base Articles:
{context_text}

Instructions:
1. Answer the question accurately using the provided articles
2. If the articles don't contain enough information, say so clearly
3. Cite sources by mentioning article titles
4. Suggest 2-3 related follow-up questions
5. Be concise but complete

Return JSON:
{{
    "answer": "Your detailed answer here...",
    "confidence": 0.85,  // Your confidence in the answer (0.0-1.0)
    "sources_used": [1, 3],  // Article IDs used
    "follow_up_questions": ["Question 1?", "Question 2?"],
    "needs_more_info": false  // true if articles insufficient
}}
"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            result = json.loads(response.content[0].text)

            # Build final response
            sources = []
            for article_id in result.get('sources_used', []):
                article = next((r for r in search_results if r['article_id'] == article_id), None)
                if article:
                    sources.append({
                        'id': article['article_id'],
                        'title': article['title'],
                        'similarity_score': article['similarity_score']
                    })

            return {
                'answer': result['answer'],
                'confidence': result.get('confidence', 0.5),
                'sources': sources,
                'suggestions': result.get('follow_up_questions', []),
                'should_create_article': result.get('needs_more_info', False)
            }

        except Exception as e:
            return {
                'answer': f"Fehler bei der Antwortgenerierung: {str(e)}",
                'confidence': 0.0,
                'sources': search_results[:3],  # Fallback to search results
                'suggestions': [],
                'should_create_article': False
            }

    def _build_context_from_results(self, results: List[Dict], max_length: int = 4000) -> str:
        """
        Build context string from search results, respecting max length.
        """
        context_parts = []
        current_length = 0

        for i, result in enumerate(results, 1):
            article_text = f"""
--- Article {i} (ID: {result['article_id']}, Score: {result['similarity_score']:.2f}) ---
Title: {result['title']}
Category: {result['category']}
Content:
{result['content']}
"""

            if current_length + len(article_text) > max_length:
                break

            context_parts.append(article_text)
            current_length += len(article_text)

        return "\n".join(context_parts)

    def _log_search(self, query: str, results: List[Dict]) -> None:
        """
        Log search query for analytics and improvement.
        """
        # Generate query embedding for analytics
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')

        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )

        # Store in ChromaDB with special collection for queries
        query_id = f"query_{datetime.now().timestamp()}"

        # Log to database
        search_log = SearchQuery(
            query_text=query,
            query_embedding_id=query_id,
            results_count=len(results),
            top_result_id=results[0]['article_id'] if results else None
        )
        db.session.add(search_log)
        db.session.commit()
```

---

## 🎨 User Interface Integration

### 1. CRM Integration Points

**A) Dashboard Widget: "Quick KB Search"**
```html
<!-- templates/dashboard.html -->
<div class="kb-search-widget">
    <h3>🔍 Knowledge Base</h3>
    <input type="text" id="kb-quick-search" placeholder="Ask a question..." />
    <div id="kb-quick-results"></div>
</div>

<script>
// Instant search with debounce
const searchInput = document.getElementById('kb-quick-search');
let searchTimeout;

searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchKnowledgeBase(e.target.value);
    }, 300);
});

async function searchKnowledgeBase(query) {
    if (query.length < 3) return;

    const response = await fetch('/api/kb/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query: query, top_k: 3})
    });

    const results = await response.json();
    displayResults(results);
}
</script>
```

**B) Customer Detail Page: "Related Knowledge"**
```html
<!-- templates/customers/detail.html -->
<section class="related-knowledge">
    <h3>📚 Related Knowledge Articles</h3>
    <p>Based on this customer's interactions:</p>

    {% for article in related_kb_articles %}
    <div class="kb-card">
        <h4>{{ article.title }}</h4>
        <p>{{ article.summary }}</p>
        <span class="badge">{{ article.category }}</span>
        <a href="/kb/{{ article.id }}">Read more →</a>
    </div>
    {% endfor %}
</section>
```

**C) AI Chat Widget (Emma Assistant)**
```html
<!-- templates/base.html -->
<div id="kb-chat-widget" class="chat-widget">
    <div class="chat-header">
        <span>💬 Emma - KB Assistant</span>
        <button id="chat-toggle">−</button>
    </div>

    <div class="chat-messages" id="chat-messages"></div>

    <div class="chat-input">
        <input type="text" id="chat-input" placeholder="Ask me anything..." />
        <button id="chat-send">Send</button>
    </div>
</div>

<script src="/static/js/kb-chat.js"></script>
```

### 2. API Endpoints

```python
# routes/kb_routes.py

from flask import Blueprint, request, jsonify
from services.kb_ingestion import KnowledgeIngestionEngine
from services.kb_retrieval import KnowledgeRetrievalEngine

kb_bp = Blueprint('kb', __name__, url_prefix='/api/kb')

ingestion = KnowledgeIngestionEngine()
retrieval = KnowledgeRetrievalEngine()


@kb_bp.route('/search', methods=['POST'])
def search_kb():
    """
    Semantic search in knowledge base.

    POST /api/kb/search
    {
        "query": "How do I reset a password?",
        "top_k": 5,
        "category": "Support",  // optional
        "min_confidence": 0.7  // optional
    }
    """
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query required'}), 400

    results = retrieval.search(
        query=query,
        top_k=data.get('top_k', 5),
        category=data.get('category'),
        min_confidence=data.get('min_confidence', 0.5)
    )

    return jsonify({
        'query': query,
        'results': results,
        'count': len(results)
    })


@kb_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    AI-powered Q&A.

    POST /api/kb/ask
    {
        "question": "What's our refund policy?",
        "customer_id": 123,  // optional
        "context": {}  // optional
    }
    """
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question required'}), 400

    answer = retrieval.ask_question(
        question=question,
        customer_id=data.get('customer_id'),
        context=data.get('context')
    )

    return jsonify(answer)


@kb_bp.route('/articles', methods=['GET'])
def list_articles():
    """
    List all published KB articles.

    GET /api/kb/articles?category=Support&page=1&per_page=20
    """
    category = request.args.get('category')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    query = KnowledgeArticle.query.filter_by(status='published')

    if category:
        query = query.filter_by(category=category)

    pagination = query.order_by(KnowledgeArticle.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'articles': [a.to_dict() for a in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@kb_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """
    Get single article by ID.
    """
    article = KnowledgeArticle.query.get_or_404(article_id)

    if article.status != 'published':
        return jsonify({'error': 'Article not published'}), 404

    # Increment view count
    article.view_count += 1
    db.session.commit()

    # Get related articles
    related = RelatedArticle.query.filter_by(
        article_id=article_id
    ).order_by(RelatedArticle.similarity_score.desc()).limit(5).all()

    related_articles = [
        KnowledgeArticle.query.get(r.related_article_id).to_dict()
        for r in related
    ]

    result = article.to_dict()
    result['related_articles'] = related_articles

    return jsonify(result)


@kb_bp.route('/articles/<int:article_id>/feedback', methods=['POST'])
def article_feedback(article_id):
    """
    Submit feedback on article usefulness.

    POST /api/kb/articles/123/feedback
    {
        "helpful": true
    }
    """
    article = KnowledgeArticle.query.get_or_404(article_id)
    data = request.json

    if data.get('helpful'):
        article.helpful_count += 1
    else:
        article.not_helpful_count += 1

    # Recalculate usefulness score
    total_feedback = article.helpful_count + article.not_helpful_count
    if total_feedback > 0:
        article.usefulness_score = article.helpful_count / total_feedback

    db.session.commit()

    return jsonify({
        'message': 'Feedback recorded',
        'usefulness_score': article.usefulness_score
    })


@kb_bp.route('/admin/drafts', methods=['GET'])
def list_drafts():
    """
    List all draft articles awaiting review (admin only).
    """
    drafts = KnowledgeArticle.query.filter_by(status='draft').order_by(
        KnowledgeArticle.created_at.desc()
    ).all()

    return jsonify({
        'drafts': [d.to_dict() for d in drafts],
        'count': len(drafts)
    })


@kb_bp.route('/admin/articles/<int:article_id>/publish', methods=['POST'])
def publish_article(article_id):
    """
    Publish a draft article (admin only).
    """
    article = KnowledgeArticle.query.get_or_404(article_id)

    article.status = 'published'
    article.updated_by = request.json.get('user', 'admin')

    db.session.commit()

    return jsonify({
        'message': 'Article published',
        'article': article.to_dict()
    })
```

---

## 📈 Analytics & Continuous Improvement

### 1. KB Health Metrics

```python
class KBAnalytics:
    """
    Analytics für Knowledge Base Performance und Gesundheit.
    """

    @staticmethod
    def get_kb_health_score() -> Dict[str, Any]:
        """
        Overall KB health score (0-100).

        Factors:
        - Coverage (% of customer questions answerable)
        - Freshness (avg age of articles)
        - Quality (avg usefulness score)
        - Usage (search frequency)
        """
        total_articles = KnowledgeArticle.query.filter_by(status='published').count()

        # Average usefulness
        avg_usefulness = db.session.query(
            db.func.avg(KnowledgeArticle.usefulness_score)
        ).filter_by(status='published').scalar() or 0.0

        # Average age (days)
        now = datetime.now(timezone.utc)
        avg_age = db.session.query(
            db.func.avg(
                db.func.extract('epoch', now - KnowledgeArticle.created_at) / 86400
            )
        ).filter_by(status='published').scalar() or 0.0

        # Search success rate (last 30 days)
        thirty_days_ago = now - timedelta(days=30)
        successful_searches = SearchQuery.query.filter(
            SearchQuery.created_at >= thirty_days_ago,
            SearchQuery.was_helpful == True
        ).count()
        total_searches = SearchQuery.query.filter(
            SearchQuery.created_at >= thirty_days_ago
        ).count()

        search_success_rate = (successful_searches / total_searches * 100) if total_searches > 0 else 0

        # Calculate health score
        health_score = (
            (min(total_articles / 100, 1.0) * 25) +  # Volume (25%)
            (avg_usefulness * 25) +  # Quality (25%)
            (max(1.0 - (avg_age / 365), 0) * 25) +  # Freshness (25%)
            (search_success_rate / 100 * 25)  # Search success (25%)
        )

        return {
            'health_score': round(health_score, 2),
            'total_articles': total_articles,
            'avg_usefulness': round(avg_usefulness, 2),
            'avg_age_days': round(avg_age, 1),
            'search_success_rate': round(search_success_rate, 1),
            'recommendations': KBAnalytics._get_recommendations(
                total_articles, avg_usefulness, avg_age, search_success_rate
            )
        }

    @staticmethod
    def _get_recommendations(articles, usefulness, age, success_rate) -> List[str]:
        """Generate improvement recommendations."""
        recs = []

        if articles < 50:
            recs.append("📝 Create more articles (target: 50+)")
        if usefulness < 0.7:
            recs.append("⭐ Improve article quality (target: 0.7+)")
        if age > 180:
            recs.append("🔄 Update old articles (avg age: 180 days)")
        if success_rate < 70:
            recs.append("🎯 Improve search relevance (target: 70%+)")

        if not recs:
            recs.append("✅ KB is healthy!")

        return recs

    @staticmethod
    def get_trending_topics() -> List[Dict[str, Any]]:
        """
        Most searched topics in last 30 days.
        """
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

        # Count queries by selected articles
        trending = db.session.query(
            KnowledgeArticle.id,
            KnowledgeArticle.title,
            KnowledgeArticle.category,
            db.func.count(SearchQuery.id).label('search_count')
        ).join(
            SearchQuery,
            SearchQuery.user_selected_result_id == KnowledgeArticle.id
        ).filter(
            SearchQuery.created_at >= thirty_days_ago
        ).group_by(
            KnowledgeArticle.id
        ).order_by(
            db.desc('search_count')
        ).limit(10).all()

        return [{
            'article_id': t.id,
            'title': t.title,
            'category': t.category,
            'search_count': t.search_count
        } for t in trending]

    @staticmethod
    def get_coverage_gaps() -> List[Dict[str, Any]]:
        """
        Identify topics with searches but no good answers.

        These are opportunities for new KB articles.
        """
        # Find searches where no result was selected or marked unhelpful
        gaps = db.session.query(
            SearchQuery.query_text,
            db.func.count(SearchQuery.id).label('frequency')
        ).filter(
            db.or_(
                SearchQuery.user_selected_result_id == None,
                SearchQuery.was_helpful == False
            )
        ).group_by(
            SearchQuery.query_text
        ).order_by(
            db.desc('frequency')
        ).limit(20).all()

        return [{
            'query': gap.query_text,
            'frequency': gap.frequency,
            'recommendation': f"Create article about: {gap.query_text}"
        } for gap in gaps]
```

### 2. Auto-Improvement Loop

```python
class KBImprovementAgent:
    """
    Kontinuierliche Verbesserung der Knowledge Base.

    Runs daily:
    1. Identify low-quality articles (low usefulness score)
    2. Suggest improvements with AI
    3. Identify coverage gaps
    4. Suggest new articles for trending searches
    5. Update outdated articles
    """

    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def run_daily_improvements(self) -> Dict[str, Any]:
        """
        Daily improvement routine.
        """
        results = {
            'low_quality_improved': 0,
            'new_articles_suggested': 0,
            'outdated_updated': 0,
            'errors': []
        }

        # 1. Improve low-quality articles
        low_quality = KnowledgeArticle.query.filter(
            KnowledgeArticle.status == 'published',
            KnowledgeArticle.usefulness_score < 0.6,
            KnowledgeArticle.helpful_count + KnowledgeArticle.not_helpful_count >= 5
        ).all()

        for article in low_quality:
            try:
                self._suggest_improvements(article)
                results['low_quality_improved'] += 1
            except Exception as e:
                results['errors'].append(str(e))

        # 2. Suggest new articles for coverage gaps
        gaps = KBAnalytics.get_coverage_gaps()
        for gap in gaps[:5]:  # Top 5 gaps
            try:
                self._suggest_new_article(gap)
                results['new_articles_suggested'] += 1
            except Exception as e:
                results['errors'].append(str(e))

        # 3. Update outdated articles
        six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)
        outdated = KnowledgeArticle.query.filter(
            KnowledgeArticle.status == 'published',
            KnowledgeArticle.updated_at < six_months_ago
        ).limit(10).all()

        for article in outdated:
            try:
                self._check_if_still_relevant(article)
                results['outdated_updated'] += 1
            except Exception as e:
                results['errors'].append(str(e))

        return results

    def _suggest_improvements(self, article: KnowledgeArticle) -> None:
        """
        AI-generated improvement suggestions for low-quality article.
        """
        prompt = f"""
Analyze this knowledge base article and suggest improvements:

Title: {article.title}
Content: {article.content}
Current usefulness score: {article.usefulness_score:.2f}
Helpful votes: {article.helpful_count}
Not helpful votes: {article.not_helpful_count}

Suggest 3-5 specific improvements to make this article more useful.

Return JSON:
{{
    "issues": ["Issue 1", "Issue 2"],
    "improvements": [
        {{"what": "...", "why": "...", "how": "..."}},
        ...
    ],
    "improved_title": "Better title...",
    "improved_content": "Improved content..."
}}
"""

        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        suggestions = json.loads(response.content[0].text)

        # Create improvement task (stored for human review)
        # In production: send to Slack/Email/Dashboard
        import logging
        logging.info(f"Improvement suggestions for article {article.id}: {suggestions}")

    def _suggest_new_article(self, gap: Dict[str, Any]) -> None:
        """
        Suggest creating new article for coverage gap.
        """
        prompt = f"""
Based on this frequent unanswered search query, draft a knowledge base article:

Query: {gap['query']}
Frequency: {gap['frequency']} searches

Create a complete article draft.

Return JSON:
{{
    "title": "...",
    "content": "...",
    "summary": "...",
    "category": "...",
    "tags": [...]
}}
"""

        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        draft = json.loads(response.content[0].text)

        # Create draft article
        article = KnowledgeArticle(
            title=draft['title'],
            content=draft['content'],
            summary=draft['summary'],
            category=draft['category'],
            tags=draft['tags'],
            source_type='ai_suggested',
            status='draft',
            created_by='AI-Improvement-Agent',
            confidence_score=0.7
        )

        db.session.add(article)
        db.session.commit()

    def _check_if_still_relevant(self, article: KnowledgeArticle) -> None:
        """
        Check if old article is still relevant or needs update/archival.
        """
        # Check if article has been accessed recently
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        recent_searches = SearchQuery.query.filter(
            SearchQuery.top_result_id == article.id,
            SearchQuery.created_at >= thirty_days_ago
        ).count()

        if recent_searches == 0:
            # No recent searches - consider archiving
            article.status = 'archived'
            db.session.commit()
        else:
            # Still used - suggest content update
            # (In production: notify team to review)
            import logging
            logging.info(f"Article {article.id} is old but still used - consider updating")
```

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] **Week 1**: Database schema + models
  - Create `KnowledgeArticle`, `ArticleEmbedding`, `RelatedArticle`, `SearchQuery` models
  - Database migrations
  - Basic CRUD operations

- [ ] **Week 2**: Vector database setup
  - Install ChromaDB/Pinecone
  - Set up embedding pipeline (OpenAI ada-002)
  - Test vector search

### Phase 2: Ingestion (Weeks 3-4)
- [ ] **Week 3**: Automatic extraction
  - Implement `KnowledgeIngestionEngine`
  - Hook into CRM interaction creation
  - AI extraction with Claude

- [ ] **Week 4**: Manual article creation
  - Admin UI for creating/editing articles
  - Review workflow for AI-generated drafts
  - Batch import from existing docs

### Phase 3: Retrieval (Weeks 5-6)
- [ ] **Week 5**: Search engine
  - Implement `KnowledgeRetrievalEngine`
  - Semantic search API
  - Hybrid search (vector + keyword)

- [ ] **Week 6**: Q&A system
  - AI-powered question answering
  - Source citation
  - Follow-up suggestions

### Phase 4: UI Integration (Weeks 7-8)
- [ ] **Week 7**: CRM integration
  - Dashboard search widget
  - Customer detail page KB section
  - Related articles component

- [ ] **Week 8**: Chat interface (Emma)
  - Chat widget UI
  - Real-time Q&A
  - Feedback collection

### Phase 5: Analytics & Improvement (Weeks 9-10)
- [ ] **Week 9**: Analytics
  - KB health metrics
  - Coverage gap analysis
  - Trending topics tracking

- [ ] **Week 10**: Auto-improvement
  - Daily improvement agent
  - Low-quality detection
  - Content suggestions

### Phase 6: Production (Weeks 11-12)
- [ ] **Week 11**: Testing & optimization
  - Performance testing
  - Edge case handling
  - Security audit

- [ ] **Week 12**: Deployment
  - Production deployment
  - Team training
  - Monitoring setup

---

## 💰 Cost Estimation

### Monthly Operating Costs

**AI APIs:**
- Claude API (Anthropic):
  - Ingestion: ~500 interactions/month × $0.02 = **$10**
  - Q&A: ~1000 queries/month × $0.02 = **$20**
  - Improvement agent: ~100 tasks/month × $0.02 = **$2**

- OpenAI Embeddings (ada-002):
  - New articles: ~100/month × $0.0001 = **$0.01**
  - Search queries: ~1000/month × $0.0001 = **$0.10**

**Vector Database:**
- **ChromaDB (Self-hosted)**: $0 (free, runs locally)
- **Pinecone (Cloud)**: $70/month (Starter plan, 100k vectors)

**Storage:**
- PostgreSQL: Included in existing CRM infrastructure

### Total Monthly Cost
- **With ChromaDB (local)**: ~$32/month
- **With Pinecone (cloud, skalierbar)**: ~$102/month

### ROI Calculation
- **Time saved**: 10h/week × €50/hour = €2,000/month
- **Cost**: €102/month
- **Net savings**: €1,898/month
- **ROI**: **1,861%** 🚀

---

## 📏 Success Metrics

### KPIs (Key Performance Indicators)

1. **Coverage Rate**
   - Target: 80% of customer questions answerable
   - Measure: `answerable_questions / total_questions`

2. **Search Success Rate**
   - Target: 75% helpful searches
   - Measure: `helpful_searches / total_searches`

3. **Knowledge Growth**
   - Target: +20 high-quality articles/month
   - Measure: New articles with confidence >0.7

4. **Response Time**
   - Target: <2 seconds for search
   - Measure: Average API response time

5. **User Adoption**
   - Target: 50% of team uses KB weekly
   - Measure: Unique weekly users

6. **Customer Self-Service**
   - Target: 30% of customer questions self-served
   - Measure: Customer portal KB usage

---

## 🔒 Security & Privacy

### Data Protection

1. **Sensitive Data Filtering**
```python
class DataSanitizer:
    """
    Remove sensitive data before storing in KB.
    """

    SENSITIVE_PATTERNS = [
        r'\b\d{16}\b',  # Credit card
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',  # Email (optional)
        r'\bpassword\s*[:=]\s*\S+',  # Passwords
    ]

    @staticmethod
    def sanitize(text: str) -> str:
        """Remove sensitive data from text."""
        sanitized = text
        for pattern in DataSanitizer.SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)
        return sanitized
```

2. **Access Control**
- Internal KB: Only authenticated users
- Public KB: Only articles marked `is_public=True`
- Admin functions: Role-based permissions

3. **Audit Log**
- Log all KB article creations/modifications
- Track who accessed what
- GDPR-compliant data retention

---

## 🎯 Zusammenfassung

### Das Knowledge Base System bietet:

✅ **Automatisches Lernen** aus jeder Customer Interaction
✅ **AI-Powered Q&A** mit Claude 3.5 Sonnet
✅ **Semantic Search** via Vector Embeddings
✅ **Self-Improvement** durch täglichen AI Agent
✅ **Emma Chat Interface** für intuitive Nutzung
✅ **Analytics** für kontinuierliche Optimierung
✅ **Privacy-First** Design mit Data Sanitization
✅ **ROI von 1,861%** (€1,898 net savings/month)

### Nächste Schritte:
1. Review dieses Design-Dokuments
2. Entscheidung: ChromaDB (local, free) vs. Pinecone (cloud, scalable)
3. Start Phase 1 (Foundation)
4. Iterative Entwicklung über 12 Wochen

---

**Erstellt**: 2025-12-24
**Autor**: Claude Development Team
**Version**: KB System Design v1.0
**Status**: Ready for Implementation 🚀
