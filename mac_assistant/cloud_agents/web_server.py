"""
Web Server Agent
Provides web interface for remote access
"""

from flask import Flask, render_template_string, request, jsonify
import threading
import os


class WebServerAgent:
    """Web server for remote access"""

    def __init__(self, core, host='0.0.0.0', port=5000):
        self.core = core
        self.host = host
        self.port = port

        self.app = Flask(__name__)
        self.running = False

        self._setup_routes()

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        def index():
            """Main dashboard"""
            return self._render_dashboard()

        @self.app.route('/api/status')
        def api_status():
            """Get system status"""
            return jsonify({
                'plugins': len(self.core.plugin_manager.get_available_plugins()),
                'ai_enabled': self.core.ai_enabled,
                'available_plugins': [p.name for p in self.core.plugin_manager.get_available_plugins()]
            })

        @self.app.route('/api/query', methods=['POST'])
        def api_query():
            """Process query"""
            data = request.get_json()
            query = data.get('query', '')

            if not query:
                return jsonify({'error': 'No query provided'}), 400

            try:
                result = self.core.process_user_query(query)
                return jsonify({'success': True, 'result': result})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500

        @self.app.route('/api/execute', methods=['POST'])
        def api_execute():
            """Execute task"""
            data = request.get_json()
            task = data.get('task', '')

            if not task:
                return jsonify({'error': 'No task provided'}), 400

            try:
                result = self.core.execute_task(task)
                return jsonify(result)
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500

        @self.app.route('/api/plugins')
        def api_plugins():
            """Get plugin list"""
            plugins = []
            for p in self.core.plugin_manager.get_all_plugins():
                plugins.append({
                    'name': p.name,
                    'available': p.is_available(),
                    'enabled': p.enabled,
                    'capabilities': p.get_capabilities()
                })
            return jsonify(plugins)

    def _render_dashboard(self):
        """Render web dashboard"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Mac Remote Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f7;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: #007AFF;
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 { font-size: 32px; margin-bottom: 10px; }
        h2 { font-size: 20px; margin-bottom: 15px; color: #1d1d1f; }
        .input-group {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            background: #007AFF;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover { background: #0056b3; }
        .result {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: 'SF Mono', monospace;
            font-size: 14px;
        }
        .status { display: flex; gap: 20px; flex-wrap: wrap; }
        .status-item {
            flex: 1;
            min-width: 200px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
        }
        .status-label { color: #666; font-size: 12px; }
        .status-value { font-size: 24px; font-weight: bold; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Mac Remote Assistant</h1>
            <p>Steuere deinen Mac von überall</p>
        </div>

        <div class="card">
            <h2>📊 System-Status</h2>
            <div class="status" id="status">
                <div class="status-item">
                    <div class="status-label">Plugins</div>
                    <div class="status-value" id="plugin-count">-</div>
                </div>
                <div class="status-item">
                    <div class="status-label">KI-Status</div>
                    <div class="status-value" id="ai-status">-</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🤖 KI-Assistent</h2>
            <div class="input-group">
                <input type="text" id="query-input" placeholder="Was möchtest du tun?">
                <button onclick="sendQuery()">Senden</button>
            </div>
            <div id="query-result" class="result" style="display:none;"></div>
        </div>

        <div class="card">
            <h2>⚡ Task ausführen</h2>
            <div class="input-group">
                <input type="text" id="task-input" placeholder="Task Befehl">
                <button onclick="executeTask()">Ausführen</button>
            </div>
            <div id="task-result" class="result" style="display:none;"></div>
        </div>
    </div>

    <script>
        // Load status
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                document.getElementById('plugin-count').textContent = data.plugins;
                document.getElementById('ai-status').textContent = data.ai_enabled ? '✅ Aktiv' : '❌ Inaktiv';
            });

        // Send query
        function sendQuery() {
            const input = document.getElementById('query-input');
            const result = document.getElementById('query-result');
            const query = input.value;

            if (!query) return;

            result.textContent = '⏳ Verarbeite...';
            result.style.display = 'block';

            fetch('/api/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: query})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    result.textContent = data.result;
                } else {
                    result.textContent = '❌ Fehler: ' + data.error;
                }
            })
            .catch(err => {
                result.textContent = '❌ Fehler: ' + err;
            });
        }

        // Execute task
        function executeTask() {
            const input = document.getElementById('task-input');
            const result = document.getElementById('task-result');
            const task = input.value;

            if (!task) return;

            result.textContent = '⏳ Führe aus...';
            result.style.display = 'block';

            fetch('/api/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({task: task})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    result.textContent = '✅ Erledigt!\\n\\n' + JSON.stringify(data.result, null, 2);
                } else {
                    result.textContent = '❌ Fehler: ' + data.error;
                }
            })
            .catch(err => {
                result.textContent = '❌ Fehler: ' + err;
            });
        }

        // Enter key support
        document.getElementById('query-input').addEventListener('keypress', e => {
            if (e.key === 'Enter') sendQuery();
        });
        document.getElementById('task-input').addEventListener('keypress', e => {
            if (e.key === 'Enter') executeTask();
        });
    </script>
</body>
</html>
        """
        return html

    def start(self):
        """Start web server"""
        if self.running:
            return

        print(f"🌐 Starting web server on http://{self.host}:{self.port}")

        self.running = True
        threading.Thread(target=self._run_server, daemon=True).start()

    def stop(self):
        """Stop web server"""
        self.running = False
        print("🌐 Web server stopped")

    def _run_server(self):
        """Run Flask server"""
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                use_reloader=False
            )
        except Exception as e:
            print(f"Error running web server: {e}")
