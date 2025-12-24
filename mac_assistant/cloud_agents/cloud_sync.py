"""
Cloud Sync Agent
Synchronize data between Mac and cloud storage
"""

import os
import json
import time
import threading
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class CloudSyncAgent:
    """Cloud sync for data backup and synchronization"""

    def __init__(self, core, sync_dir: Optional[str] = None, interval: int = 3600):
        self.core = core
        self.sync_dir = Path(sync_dir or os.getenv('CLOUD_SYNC_DIR', '~/Dropbox/MacAssistant')).expanduser()
        self.interval = interval  # Sync interval in seconds (default: 1 hour)

        self.running = False
        self.last_sync = None

        # Create sync directory if it doesn't exist
        self.sync_dir.mkdir(parents=True, exist_ok=True)

        print(f"✓ Cloud sync initialized: {self.sync_dir}")

    def start(self):
        """Start automatic sync"""
        if self.running:
            return True

        print("☁️  Starting cloud sync...")
        self.running = True

        # Start sync thread
        threading.Thread(target=self._sync_loop, daemon=True).start()

        return True

    def stop(self):
        """Stop automatic sync"""
        self.running = False
        print("☁️  Cloud sync stopped")

    def _sync_loop(self):
        """Background sync loop"""
        while self.running:
            try:
                self.sync_now()
                time.sleep(self.interval)
            except Exception as e:
                print(f"Error in sync loop: {e}")
                time.sleep(60)  # Wait 1 minute on error

    def sync_now(self) -> Dict[str, Any]:
        """Perform sync immediately"""
        print("☁️  Syncing to cloud...")

        results = {
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'synced': []
        }

        try:
            # 1. Sync database
            if self._sync_database():
                results['synced'].append('database')

            # 2. Sync configuration
            if self._sync_config():
                results['synced'].append('config')

            # 3. Sync activity logs
            if self._sync_logs():
                results['synced'].append('logs')

            # 4. Create sync manifest
            self._create_manifest(results)

            self.last_sync = datetime.now()
            print(f"✓ Cloud sync complete: {len(results['synced'])} items")

        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
            print(f"✗ Cloud sync failed: {e}")

        return results

    def _sync_database(self) -> bool:
        """Sync activity database"""
        try:
            db_path = Path(self.core.tracker.db_path)
            if not db_path.exists():
                return False

            # Create backup directory
            backup_dir = self.sync_dir / 'database'
            backup_dir.mkdir(exist_ok=True)

            # Copy database with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = backup_dir / f'activities_{timestamp}.db'
            shutil.copy2(db_path, backup_path)

            # Also keep latest version
            latest_path = backup_dir / 'activities_latest.db'
            shutil.copy2(db_path, latest_path)

            # Clean old backups (keep last 10)
            self._cleanup_old_backups(backup_dir, '*.db', keep=10)

            return True

        except Exception as e:
            print(f"Error syncing database: {e}")
            return False

    def _sync_config(self) -> bool:
        """Sync configuration files"""
        try:
            config_dir = self.sync_dir / 'config'
            config_dir.mkdir(exist_ok=True)

            # Sync .env file (without sensitive keys!)
            env_path = Path(__file__).parent.parent / '.env'
            if env_path.exists():
                # Read and filter sensitive data
                config_data = self._filter_sensitive_config(env_path)

                # Save filtered config
                with open(config_dir / 'config.json', 'w') as f:
                    json.dump(config_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error syncing config: {e}")
            return False

    def _sync_logs(self) -> bool:
        """Sync activity logs"""
        try:
            logs_dir = self.sync_dir / 'logs'
            logs_dir.mkdir(exist_ok=True)

            # Export recent activities to JSON
            activities = self._export_recent_activities()

            # Save to dated file
            today = datetime.now().strftime('%Y-%m-%d')
            log_file = logs_dir / f'activities_{today}.json'

            with open(log_file, 'w') as f:
                json.dump(activities, f, indent=2)

            # Clean old logs (keep last 30 days)
            self._cleanup_old_backups(logs_dir, '*.json', keep=30)

            return True

        except Exception as e:
            print(f"Error syncing logs: {e}")
            return False

    def _export_recent_activities(self, days: int = 7) -> Dict:
        """Export recent activities"""
        try:
            activities = self.core.tracker.get_recent_activities(days=days)

            export = {
                'exported_at': datetime.now().isoformat(),
                'days': days,
                'count': len(activities),
                'activities': []
            }

            for activity in activities:
                export['activities'].append({
                    'timestamp': activity.get('timestamp'),
                    'app': activity.get('app_name'),
                    'type': activity.get('activity_type'),
                    'title': activity.get('title'),
                    'content': activity.get('content', '')[:200]  # Truncate long content
                })

            return export

        except Exception as e:
            print(f"Error exporting activities: {e}")
            return {'activities': []}

    def _filter_sensitive_config(self, env_path: Path) -> Dict:
        """Filter out sensitive data from config"""
        config = {}

        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()

                        # Skip API keys and tokens
                        if any(sensitive in key.upper() for sensitive in ['KEY', 'TOKEN', 'PASSWORD', 'SECRET']):
                            config[key] = '***HIDDEN***'
                        else:
                            config[key] = value.strip()

        except Exception as e:
            print(f"Error filtering config: {e}")

        return config

    def _create_manifest(self, sync_results: Dict):
        """Create sync manifest"""
        manifest = {
            'last_sync': sync_results['timestamp'],
            'success': sync_results['success'],
            'synced_items': sync_results['synced'],
            'system_info': {
                'plugins': len(self.core.plugin_manager.get_available_plugins()),
                'ai_enabled': self.core.ai_enabled
            }
        }

        manifest_path = self.sync_dir / 'manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

    def _cleanup_old_backups(self, directory: Path, pattern: str, keep: int):
        """Clean up old backup files"""
        try:
            files = sorted(directory.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)

            # Keep latest files, delete old ones
            for old_file in files[keep:]:
                if old_file.name.endswith('_latest.db'):
                    continue  # Never delete latest
                old_file.unlink()

        except Exception as e:
            print(f"Error cleaning up backups: {e}")

    # ===== Restore Methods =====

    def restore_from_cloud(self) -> bool:
        """Restore data from cloud"""
        print("☁️  Restoring from cloud...")

        try:
            # Check if latest database exists
            latest_db = self.sync_dir / 'database' / 'activities_latest.db'
            if latest_db.exists():
                # Backup current database
                current_db = Path(self.core.tracker.db_path)
                if current_db.exists():
                    backup = current_db.with_suffix('.db.backup')
                    shutil.copy2(current_db, backup)

                # Restore from cloud
                shutil.copy2(latest_db, current_db)
                print("✓ Database restored from cloud")
                return True

            else:
                print("✗ No cloud backup found")
                return False

        except Exception as e:
            print(f"✗ Restore failed: {e}")
            return False

    def get_sync_status(self) -> Dict:
        """Get sync status"""
        manifest_path = self.sync_dir / 'manifest.json'

        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                return json.load(f)

        return {
            'last_sync': None,
            'status': 'never_synced'
        }

    def list_backups(self) -> Dict:
        """List available backups"""
        backups = {
            'database': [],
            'logs': []
        }

        # Database backups
        db_dir = self.sync_dir / 'database'
        if db_dir.exists():
            for db_file in sorted(db_dir.glob('*.db'), reverse=True):
                backups['database'].append({
                    'name': db_file.name,
                    'size': db_file.stat().st_size,
                    'modified': datetime.fromtimestamp(db_file.stat().st_mtime).isoformat()
                })

        # Log backups
        logs_dir = self.sync_dir / 'logs'
        if logs_dir.exists():
            for log_file in sorted(logs_dir.glob('*.json'), reverse=True):
                backups['logs'].append({
                    'name': log_file.name,
                    'size': log_file.stat().st_size,
                    'modified': datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
                })

        return backups
