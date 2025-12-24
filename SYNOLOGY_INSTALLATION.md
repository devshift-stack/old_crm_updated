# 🏠 Synology NAS Installation - AI Agents zu Hause

## Security & AI Agents auf deinem Synology NAS

---

## 🎯 Warum Synology NAS?

### Vorteile
- ✅ **Läuft zu Hause** - Deine Daten bleiben lokal
- ✅ **Schnelles LAN** - Kein Internet-Delay
- ✅ **24/7 verfügbar** - Immer online
- ✅ **Keine Cloud-Kosten** - Einmalige Investition
- ✅ **Volle Kontrolle** - Du bestimmst alles
- ✅ **Energieeffizient** - NAS verbraucht wenig Strom

### Was wir installieren
- 🔒 **Security Agent** - Überwacht Code & Server
- 🤖 **AI Agent Server** - Lokale AI-Modelle (Ollama)
- 📊 **Monitoring Dashboard** - Übersicht aller Agents
- 🔔 **Alert System** - Notifications bei Problemen

---

## 📋 Voraussetzungen

### Hardware
- Synology NAS (min. DS220+, besser DS920+)
- Min. 4GB RAM (8GB empfohlen)
- Min. 100GB freier Speicher

### Software
- DSM 7.0 oder neuer
- Docker Package installiert
- Node.js installiert (optional)

---

## 🚀 Schritt-für-Schritt Installation

### Phase 1: Synology vorbereiten

**Schritt 1: Docker aktivieren**

```
1. Öffne DSM (http://deine-synology-ip:5000)
2. Gehe zu "Package Center"
3. Suche "Docker"
4. Klicke "Installieren"
5. Warte bis Installation abgeschlossen
```

**Schritt 2: Shared Folder erstellen**

```
1. "Control Panel" > "Shared Folder"
2. Klicke "Create"
3. Name: "ai-agents"
4. Enable: Recycle Bin
5. Permissions:
   - Dein User: Read/Write
   - Docker: Read/Write
```

**Schritt 3: SSH aktivieren (optional, für Advanced Setup)**

```
1. "Control Panel" > "Terminal & SNMP"
2. Enable "Enable SSH service"
3. Port: 22 (oder custom)
4. Apply
```

---

### Phase 2: Security Agent installieren

**Schritt 1: Docker Compose File erstellen**

SSH in Synology oder nutze File Station:

```yaml
# /volume1/docker/ai-agents/docker-compose.yml

version: '3.8'

services:
  # Security Agent
  security-agent:
    image: node:18-alpine
    container_name: security-agent
    restart: always
    volumes:
      - /volume1/ai-agents/projects:/workspace
      - /volume1/ai-agents/security-agent:/app
    environment:
      - SCAN_INTERVAL=60000
      - ALERT_EMAIL=deine@email.com
      - NODE_ENV=production
    ports:
      - "3001:3001"
    command: >
      sh -c "cd /app && npm install && npm start"
    networks:
      - ai-network

  # Ollama (Local AI)
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: always
    volumes:
      - /volume1/ai-agents/ollama:/root/.ollama
    ports:
      - "11434:11434"
    networks:
      - ai-network
    # GPU support (wenn Synology GPU hat)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]

  # Monitoring Dashboard
  dashboard:
    image: grafana/grafana:latest
    container_name: monitoring-dashboard
    restart: always
    volumes:
      - /volume1/ai-agents/grafana:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=dein-password
    ports:
      - "3000:3000"
    networks:
      - ai-network

  # Alert Manager (für Notifications)
  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: always
    volumes:
      - /volume1/ai-agents/alertmanager:/etc/alertmanager
    ports:
      - "9093:9093"
    command:
      - '--config.file=/etc/alertmanager/config.yml'
    networks:
      - ai-network

networks:
  ai-network:
    driver: bridge
```

**Schritt 2: Security Agent Code**

Erstelle `/volume1/ai-agents/security-agent/index.js`:

```javascript
/**
 * Security Agent - Home Edition
 * Läuft 24/7 auf Synology NAS
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

const express = require('express');
const app = express();
const PORT = 3001;

// Configuration
const CONFIG = {
  workspaceDir: '/workspace',
  scanInterval: parseInt(process.env.SCAN_INTERVAL) || 60000,
  alertEmail: process.env.ALERT_EMAIL,
};

// Security Scanner
class SecurityScanner {
  async scan() {
    console.log('🔍 Starting security scan...');

    const results = {
      timestamp: new Date(),
      vulnerabilities: [],
      stats: {},
    };

    // 1. Scan dependencies
    const depVulns = await this.scanDependencies();
    results.vulnerabilities.push(...depVulns);

    // 2. Scan for secrets
    const secrets = await this.scanSecrets();
    results.vulnerabilities.push(...secrets);

    // 3. Scan code for patterns
    const codeVulns = await this.scanCode();
    results.vulnerabilities.push(...codeVulns);

    // 4. Generate stats
    results.stats = this.generateStats(results.vulnerabilities);

    // 5. Alert if critical
    if (this.hasCritical(results.vulnerabilities)) {
      await this.sendAlert(results);
    }

    return results;
  }

  async scanDependencies() {
    console.log('📦 Scanning dependencies...');
    const vulnerabilities = [];

    try {
      const { stdout } = await execPromise(
        'npm audit --json',
        { cwd: CONFIG.workspaceDir }
      );

      const auditResult = JSON.parse(stdout);

      if (auditResult.metadata.vulnerabilities) {
        const vulns = auditResult.metadata.vulnerabilities;

        Object.entries(vulns).forEach(([severity, count]) => {
          if (count > 0) {
            vulnerabilities.push({
              type: 'dependency',
              severity,
              count,
              message: `${count} ${severity} severity vulnerabilities found`,
            });
          }
        });
      }
    } catch (error) {
      console.error('Error scanning dependencies:', error.message);
    }

    return vulnerabilities;
  }

  async scanSecrets() {
    console.log('🔑 Scanning for exposed secrets...');
    const vulnerabilities = [];

    const patterns = {
      'API Key': /(?:api[_-]?key|apikey)[\s:=]+['"]([a-zA-Z0-9]{20,})['"]/, 'AWS Key': /(AKIA[0-9A-Z]{16})/,
      'Private Key': /-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----/,
      'Password': /password[\s:=]+['"]([^'"]{8,})['"]/, // nur hardcoded
    };

    try {
      const files = await this.getAllFiles(CONFIG.workspaceDir);

      for (const file of files) {
        // Skip node_modules, .git, etc.
        if (file.includes('node_modules') || file.includes('.git')) {
          continue;
        }

        const content = await fs.readFile(file, 'utf-8');

        for (const [name, pattern] of Object.entries(patterns)) {
          if (pattern.test(content)) {
            vulnerabilities.push({
              type: 'secret',
              severity: 'critical',
              file,
              secretType: name,
              message: `Exposed ${name} found in ${file}`,
            });
          }
        }
      }
    } catch (error) {
      console.error('Error scanning secrets:', error.message);
    }

    return vulnerabilities;
  }

  async scanCode() {
    console.log('💻 Scanning code patterns...');
    const vulnerabilities = [];

    const dangerousPatterns = {
      'SQL Injection': /(?:SELECT|INSERT|UPDATE|DELETE).*\$\{.*\}/i,
      'eval() usage': /eval\s*\(/,
      'dangerous HTML': /innerHTML\s*=.*\$\{/,
    };

    try {
      const files = await this.getAllFiles(CONFIG.workspaceDir);

      for (const file of files) {
        if (!file.match(/\.(js|ts|tsx|jsx)$/)) continue;
        if (file.includes('node_modules')) continue;

        const content = await fs.readFile(file, 'utf-8');

        for (const [name, pattern] of Object.entries(dangerousPatterns)) {
          if (pattern.test(content)) {
            vulnerabilities.push({
              type: 'code',
              severity: 'high',
              file,
              pattern: name,
              message: `Potentially dangerous pattern: ${name} in ${file}`,
            });
          }
        }
      }
    } catch (error) {
      console.error('Error scanning code:', error.message);
    }

    return vulnerabilities;
  }

  async getAllFiles(dir, fileList = []) {
    const files = await fs.readdir(dir);

    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = await fs.stat(filePath);

      if (stat.isDirectory()) {
        await this.getAllFiles(filePath, fileList);
      } else {
        fileList.push(filePath);
      }
    }

    return fileList;
  }

  generateStats(vulnerabilities) {
    const stats = {
      total: vulnerabilities.length,
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
    };

    vulnerabilities.forEach(v => {
      stats[v.severity] = (stats[v.severity] || 0) + 1;
    });

    return stats;
  }

  hasCritical(vulnerabilities) {
    return vulnerabilities.some(v => v.severity === 'critical');
  }

  async sendAlert(results) {
    console.log('🚨 CRITICAL VULNERABILITIES FOUND!');
    console.log(JSON.stringify(results, null, 2));

    // Hier könntest du Email/Webhook senden
    // Beispiel mit curl zu Slack/Discord Webhook:
    /*
    await execPromise(
      `curl -X POST -H 'Content-type: application/json' \
       --data '{"text":"🚨 Critical Security Issue!"}' \
       YOUR_WEBHOOK_URL`
    );
    */
  }
}

// API Server
const scanner = new SecurityScanner();
let lastScanResult = null;

// Dashboard endpoint
app.get('/dashboard', (req, res) => {
  res.json({
    status: 'running',
    lastScan: lastScanResult,
    config: CONFIG,
  });
});

// Manual scan endpoint
app.post('/scan', async (req, res) => {
  try {
    const result = await scanner.scan();
    lastScanResult = result;
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🔒 Security Agent running on port ${PORT}`);
  console.log(`📊 Dashboard: http://synology-ip:${PORT}/dashboard`);

  // Start periodic scanning
  setInterval(async () => {
    lastScanResult = await scanner.scan();
  }, CONFIG.scanInterval);
});
```

**Schritt 3: package.json erstellen**

```json
{
  "name": "security-agent",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "express": "^4.18.2"
  },
  "scripts": {
    "start": "node index.js"
  }
}
```

**Schritt 4: Docker Compose starten**

```bash
# SSH in Synology
ssh admin@synology-ip

# Navigate to docker folder
cd /volume1/docker/ai-agents

# Start containers
sudo docker-compose up -d

# Check status
sudo docker-compose ps

# View logs
sudo docker-compose logs -f security-agent
```

---

### Phase 3: Ollama (Local AI) einrichten

**Schritt 1: Modell herunterladen**

```bash
# SSH in Synology
ssh admin@synology-ip

# Exec into Ollama container
sudo docker exec -it ollama bash

# Download model
ollama pull llama3.2

# Test
ollama run llama3.2 "Hello"

# Exit
exit
```

**Schritt 2: Test von außen**

```bash
# Von deinem Mac/PC
curl http://synology-ip:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?"
}'
```

---

### Phase 4: Monitoring Dashboard

**Schritt 1: Grafana konfigurieren**

```
1. Öffne http://synology-ip:3000
2. Login: admin / dein-password
3. Add Data Source:
   - Type: Prometheus (optional)
   - URL: http://prometheus:9090

4. Import Dashboard:
   - Dashboard ID: 1860 (Node Exporter)
```

**Schritt 2: Custom Dashboard für Security Agent**

```
1. Create New Dashboard
2. Add Panel
3. Data Source: JSON API
4. URL: http://security-agent:3001/dashboard
5. Visualize vulnerabilities
```

---

## 🌐 Zugriff von außen (optional)

### VPN Setup (sicher!)

**Via Synology VPN Server:**

```
1. Package Center > VPN Server
2. Installieren
3. OpenVPN oder L2TP/IPSec konfigurieren
4. Client Config downloaden
5. Von außen via VPN verbinden
→ Zugriff auf http://synology-local-ip:3001
```

### Reverse Proxy (fortgeschritten)

```
1. Control Panel > Login Portal > Advanced
2. Enable Reverse Proxy
3. Create Rule:
   - Source: agents.deine-domain.com
   - Destination: localhost:3001
4. Enable HTTPS (Let's Encrypt)
```

---

## 📊 Nutzung

### Tägliche Nutzung

**Dashboard aufrufen:**
```
http://synology-ip:3000 → Grafana Dashboard
http://synology-ip:3001/dashboard → Security Agent
```

**Manueller Scan:**
```bash
curl -X POST http://synology-ip:3001/scan
```

**Logs ansehen:**
```bash
ssh admin@synology-ip
sudo docker-compose logs -f security-agent
```

---

## 🔔 Alerts & Notifications

### Email Alerts

Erstelle `/volume1/ai-agents/alertmanager/config.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'email'

receivers:
  - name: 'email'
    email_configs:
      - to: 'deine@email.com'
        from: 'alerts@synology.local'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'deine@gmail.com'
        auth_password: 'app-specific-password'
```

### Slack/Discord Webhook

```javascript
// In security-agent/index.js
async sendAlert(results) {
  const webhookUrl = process.env.SLACK_WEBHOOK;

  if (webhookUrl) {
    await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: `🚨 Security Alert!`,
        attachments: [{
          color: 'danger',
          fields: [
            { title: 'Critical', value: results.stats.critical, short: true },
            { title: 'High', value: results.stats.high, short: true },
          ]
        }]
      })
    });
  }
}
```

---

## ⚡ Performance-Tipps

### SSD Cache nutzen

```
1. Storage Manager > SSD Cache
2. Create Cache
3. Select SSDs
4. Mode: Read-Write
→ Deutlich schnellere Container
```

### RAM Upgrade

```
Empfohlen: 8GB+ RAM
→ Bessere Performance für AI Modelle
→ Mehr Docker Container möglich
```

---

## 🔒 Sicherheit

### Firewall Regeln

```
1. Control Panel > Security > Firewall
2. Enable Firewall
3. Create Rules:
   - Allow: Port 3000, 3001, 11434 (nur LAN)
   - Deny: All others
```

### Auto-Backup

```
1. Control Panel > Task Scheduler
2. Create > Backup Task
3. Schedule: Daily 2AM
4. Backup: /volume1/ai-agents → External Drive
```

---

## 🎯 Zusammenfassung

**Du hast jetzt:**
- ✅ Security Agent (24/7 scanning)
- ✅ Ollama (Lokale AI)
- ✅ Monitoring Dashboard
- ✅ Alert System
- ✅ Alles läuft zu Hause im LAN

**Zugriff:**
- Security Dashboard: http://synology-ip:3001/dashboard
- Grafana: http://synology-ip:3000
- Ollama API: http://synology-ip:11434

**Next Steps:**
- Verbinde Research Agent App mit Synology Ollama
- Configure Alerts
- Customize Security Rules

---

**Dein eigenes AI & Security Center zu Hause! 🏠🤖**
