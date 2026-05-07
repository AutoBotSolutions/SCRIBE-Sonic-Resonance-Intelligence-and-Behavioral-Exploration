"""
Feedback Loop (Learning System)
Continuous learning and adaptation from resonance scan results
"""

import asyncio
import logging
import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import numpy as np

def serialize_for_json(obj):
    """Helper function to serialize objects including numpy arrays and dataclasses"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif hasattr(obj, '__dict__'):  # Handle dataclasses and other objects
        return serialize_for_json(obj.__dict__)
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj

@dataclass
class ScanResult:
    """Structured scan result for storage and analysis"""
    timestamp: str
    signals: List[Dict[str, Any]]
    response: Dict[str, Any]
    features: Dict[str, Any]
    interpretation: Dict[str, Any]
    config: Dict[str, Any]
    user_feedback: Optional[Dict[str, Any]] = None

class FeedbackLoop:
    """Continuous learning system for resonance intelligence"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Database setup
        self.db_path = config.get('database_path', 'scribe_learning.db')
        self.db_connection = None
        
        # Learning parameters
        self.learning_rate = config.get('learning_rate', 0.01)
        self.pattern_update_threshold = config.get('pattern_update_threshold', 10)
        self.feedback_weight = config.get('feedback_weight', 0.3)
        
        # Pattern adaptation
        self.pattern_adaptations = {}
        self.user_corrections = []
        self.performance_metrics = []
        
        self.is_initialized = False
        self.logger.info("Feedback Loop system created")
    
    async def initialize(self):
        """Initialize learning database and systems"""
        try:
            # Setup database
            await self._setup_database()
            
            # Load existing learning data
            await self._load_learning_data()
            
            self.is_initialized = True
            self.logger.info("✅ Feedback Loop system initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize feedback loop: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup learning resources"""
        if self.db_connection:
            self.db_connection.close()
        
        # Save learning data
        await self._save_learning_data()
        
        self.is_initialized = False
        self.logger.info("Feedback Loop system cleaned up")
    
    async def _setup_database(self):
        """Setup SQLite database for learning storage"""
        self.db_connection = sqlite3.connect(self.db_path)
        cursor = self.db_connection.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                signals TEXT NOT NULL,
                response TEXT NOT NULL,
                features TEXT NOT NULL,
                interpretation TEXT NOT NULL,
                config TEXT NOT NULL,
                user_feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_adaptations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_name TEXT NOT NULL,
                adaptations TEXT NOT NULL,
                confidence REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                feedback_type TEXT NOT NULL,
                feedback_data TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scan_id) REFERENCES scan_results (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT NOT NULL,
                metric_value REAL NOT NULL,
                context TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db_connection.commit()
        self.logger.info("Database tables created/verified")
    
    async def store_scan_result(self, scan_result: Dict[str, Any]):
        """Store scan result for learning"""
        if not self.is_initialized:
            raise RuntimeError("Feedback loop not initialized")
        
        try:
            cursor = self.db_connection.cursor()
            
            # Store scan result
            cursor.execute('''
                INSERT INTO scan_results 
                (timestamp, signals, response, features, interpretation, config)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                scan_result['timestamp'],
                json.dumps(serialize_for_json(scan_result['signals'])),
                json.dumps(serialize_for_json(scan_result['response'])),
                json.dumps(serialize_for_json(scan_result['features'])),
                json.dumps(serialize_for_json(scan_result['interpretation'])),
                json.dumps(serialize_for_json(scan_result['config']))
            ))
            
            scan_id = cursor.lastrowid
            
            # Extract and store performance metrics
            await self._extract_performance_metrics(scan_result, scan_id)
            
            self.db_connection.commit()
            self.logger.debug(f"Stored scan result {scan_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to store scan result: {e}")
            raise
    
    async def add_user_feedback(self, scan_id: int, feedback_type: str, 
                              feedback_data: Dict[str, Any]):
        """Add user feedback for learning"""
        try:
            cursor = self.db_connection.cursor()
            
            cursor.execute('''
                INSERT INTO user_feedback (scan_id, feedback_type, feedback_data)
                VALUES (?, ?, ?)
            ''', (scan_id, feedback_type, json.dumps(feedback_data)))
            
            # Update scan result with feedback
            cursor.execute('''
                UPDATE scan_results SET user_feedback = ? WHERE id = ?
            ''', (json.dumps(feedback_data), scan_id))
            
            self.db_connection.commit()
            
            # Process feedback for learning
            await self._process_user_feedback(scan_id, feedback_type, feedback_data)
            
            self.logger.info(f"Added user feedback for scan {scan_id}: {feedback_type}")
            
        except Exception as e:
            self.logger.error(f"Failed to add user feedback: {e}")
            raise
    
    async def _extract_performance_metrics(self, scan_result: Dict[str, Any], scan_id: int):
        """Extract performance metrics from scan result"""
        cursor = self.db_connection.cursor()
        
        interpretation = scan_result.get('interpretation', {})
        confidence_scores = interpretation.get('confidence_scores', {})
        
        # Store confidence metrics
        for metric_type, value in confidence_scores.items():
            cursor.execute('''
                INSERT INTO performance_metrics (metric_type, metric_value, context)
                VALUES (?, ?, ?)
            ''', (f"confidence_{metric_type}", value, f"scan_{scan_id}"))
        
        # Store processing time metrics
        processing_metadata = interpretation.get('interpretation_metadata', {})
        processing_time = processing_metadata.get('processing_time', 0)
        
        cursor.execute('''
            INSERT INTO performance_metrics (metric_type, metric_value, context)
            VALUES (?, ?, ?)
        ''', ("processing_time", processing_time, f"scan_{scan_id}"))
        
        # Store anomaly detection metrics
        anomalies = interpretation.get('anomalies', [])
        cursor.execute('''
            INSERT INTO performance_metrics (metric_type, metric_value, context)
            VALUES (?, ?, ?)
        ''', ("anomaly_count", len(anomalies), f"scan_{scan_id}"))
    
    async def _process_user_feedback(self, scan_id: int, feedback_type: str, 
                                   feedback_data: Dict[str, Any]):
        """Process user feedback for pattern adaptation"""
        try:
            # Get the original scan result
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT features, interpretation FROM scan_results WHERE id = ?
            ''', (scan_id,))
            
            result = cursor.fetchone()
            if not result:
                return
            
            features = json.loads(result[0])
            interpretation = json.loads(result[1])
            
            # Process different types of feedback
            if feedback_type == "material_correction":
                await self._adapt_material_patterns(features, feedback_data)
            elif feedback_type == "environment_correction":
                await self._adapt_environment_patterns(features, feedback_data)
            elif feedback_type == "state_correction":
                await self._adapt_state_patterns(features, feedback_data)
            elif feedback_type == "interpretation_rating":
                await self._update_interpretation_confidence(interpretation, feedback_data)
            
            # Store feedback for trend analysis
            self.user_corrections.append({
                'scan_id': scan_id,
                'feedback_type': feedback_type,
                'feedback_data': feedback_data,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Error processing user feedback: {e}")
    
    async def _adapt_material_patterns(self, features: Dict[str, Any], feedback_data: Dict[str, Any]):
        """Adapt material patterns based on user correction"""
        correct_material = feedback_data.get('correct_material')
        incorrect_material = feedback_data.get('incorrect_material')
        
        if not correct_material:
            return
        
        # Extract current resonance features
        resonance_peaks = features.get('resonance_peaks', {}).get('resonance_peaks', [])
        peak_frequencies = [p['frequency'] for p in resonance_peaks[:5]]
        
        # Update pattern adaptation
        pattern_key = f"material_{correct_material}"
        if pattern_key not in self.pattern_adaptations:
            self.pattern_adaptations[pattern_key] = {
                'peak_frequencies': [],
                'q_factors': [],
                'decay_times': [],
                'adaptation_count': 0
            }
        
        adaptation = self.pattern_adaptations[pattern_key]
        adaptation['peak_frequencies'].extend(peak_frequencies)
        adaptation['adaptation_count'] += 1
        
        # Store in database
        await self._store_pattern_adaptation('material', correct_material, adaptation)
        
        self.logger.info(f"Adapted material pattern for {correct_material}")
    
    async def _adapt_environment_patterns(self, features: Dict[str, Any], feedback_data: Dict[str, Any]):
        """Adapt environment patterns based on user correction"""
        correct_environment = feedback_data.get('correct_environment')
        
        if not correct_environment:
            return
        
        # Extract environment features
        freq_domain = features.get('frequency_domain', {})
        spectral_centroid = freq_domain.get('spectral_centroid', 0)
        spectral_rolloff = freq_domain.get('spectral_rolloff', 0)
        
        # Update pattern adaptation
        pattern_key = f"environment_{correct_environment}"
        if pattern_key not in self.pattern_adaptations:
            self.pattern_adaptations[pattern_key] = {
                'spectral_centroids': [],
                'spectral_rolloffs': [],
                'adaptation_count': 0
            }
        
        adaptation = self.pattern_adaptations[pattern_key]
        adaptation['spectral_centroids'].append(spectral_centroid)
        adaptation['spectral_rolloffs'].append(spectral_rolloff)
        adaptation['adaptation_count'] += 1
        
        # Store in database
        await self._store_pattern_adaptation('environment', correct_environment, adaptation)
        
        self.logger.info(f"Adapted environment pattern for {correct_environment}")
    
    async def _adapt_state_patterns(self, features: Dict[str, Any], feedback_data: Dict[str, Any]):
        """Adapt state patterns based on user correction"""
        correct_state = feedback_data.get('correct_state')
        
        if not correct_state:
            return
        
        # Extract state features
        time_domain = features.get('time_domain', {})
        rms = time_domain.get('rms', 0)
        peak = time_domain.get('peak', 0)
        
        # Update pattern adaptation
        pattern_key = f"state_{correct_state}"
        if pattern_key not in self.pattern_adaptations:
            self.pattern_adaptations[pattern_key] = {
                'rms_values': [],
                'peak_values': [],
                'adaptation_count': 0
            }
        
        adaptation = self.pattern_adaptations[pattern_key]
        adaptation['rms_values'].append(rms)
        adaptation['peak_values'].append(peak)
        adaptation['adaptation_count'] += 1
        
        # Store in database
        await self._store_pattern_adaptation('state', correct_state, adaptation)
        
        self.logger.info(f"Adapted state pattern for {correct_state}")
    
    async def _update_interpretation_confidence(self, interpretation: Dict[str, Any], 
                                             feedback_data: Dict[str, Any]):
        """Update interpretation confidence based on user rating"""
        rating = feedback_data.get('rating')  # 1-5 scale
        
        if not rating:
            return
        
        # Normalize rating to 0-1 confidence
        normalized_confidence = rating / 5.0
        
        # Update confidence weights based on feedback
        confidence_scores = interpretation.get('confidence_scores', {})
        
        for score_type, current_confidence in confidence_scores.items():
            # Adjust confidence based on user feedback
            adjustment = self.learning_rate * (normalized_confidence - current_confidence)
            new_confidence = current_confidence + adjustment
            
            # Store updated confidence
            await self._store_confidence_update(score_type, new_confidence)
        
        self.logger.info(f"Updated interpretation confidence based on rating: {rating}")
    
    async def _store_pattern_adaptation(self, pattern_type: str, pattern_name: str, 
                                      adaptation: Dict[str, Any]):
        """Store pattern adaptation in database"""
        cursor = self.db_connection.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO pattern_adaptations 
            (pattern_type, pattern_name, adaptations, usage_count)
            VALUES (?, ?, ?, ?)
        ''', (
            pattern_type,
            pattern_name,
            json.dumps(adaptation),
            adaptation.get('adaptation_count', 0)
        ))
        
        self.db_connection.commit()
    
    async def _store_confidence_update(self, score_type: str, new_confidence: float):
        """Store confidence update for learning"""
        cursor = self.db_connection.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics (metric_type, metric_value, context)
            VALUES (?, ?, ?)
        ''', (f"adjusted_confidence_{score_type}", new_confidence, "user_feedback"))
        
        self.db_connection.commit()
    
    async def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learning data"""
        try:
            cursor = self.db_connection.cursor()
            
            # Get scan statistics
            cursor.execute('SELECT COUNT(*) FROM scan_results')
            total_scans = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM user_feedback')
            total_feedback = cursor.fetchone()[0]
            
            # Get recent performance metrics
            cursor.execute('''
                SELECT metric_type, AVG(metric_value) as avg_value
                FROM performance_metrics 
                WHERE timestamp > datetime('now', '-7 days')
                GROUP BY metric_type
            ''')
            
            recent_metrics = dict(cursor.fetchall())
            
            # Get pattern adaptation statistics
            cursor.execute('''
                SELECT pattern_type, pattern_name, usage_count, success_rate
                FROM pattern_adaptations
                ORDER BY usage_count DESC
                LIMIT 10
            ''')
            
            top_patterns = [
                {
                    'type': row[0],
                    'name': row[1],
                    'usage_count': row[2],
                    'success_rate': row[3]
                }
                for row in cursor.fetchall()
            ]
            
            # Get feedback trends
            cursor.execute('''
                SELECT feedback_type, COUNT(*) as count
                FROM user_feedback
                WHERE timestamp > datetime('now', '-7 days')
                GROUP BY feedback_type
            ''')
            
            feedback_trends = dict(cursor.fetchall())
            
            return {
                'total_scans': total_scans,
                'total_feedback': total_feedback,
                'recent_performance_metrics': recent_metrics,
                'top_adapted_patterns': top_patterns,
                'feedback_trends': feedback_trends,
                'learning_rate': self.learning_rate,
                'pattern_adaptations_count': len(self.pattern_adaptations)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting learning insights: {e}")
            return {}
    
    async def get_adapted_patterns(self) -> Dict[str, Any]:
        """Get adapted patterns for use in interpretation"""
        try:
            cursor = self.db_connection.cursor()
            
            cursor.execute('''
                SELECT pattern_type, pattern_name, adaptations, confidence
                FROM pattern_adaptations
                WHERE usage_count >= ?
                ORDER BY confidence DESC
            ''', (self.pattern_update_threshold,))
            
            adapted_patterns = {}
            
            for row in cursor.fetchall():
                pattern_type, pattern_name, adaptations_json, confidence = row
                adaptations = json.loads(adaptations_json)
                
                if pattern_type not in adapted_patterns:
                    adapted_patterns[pattern_type] = {}
                
                adapted_patterns[pattern_type][pattern_name] = {
                    'adaptations': adaptations,
                    'confidence': confidence,
                    'usage_count': adaptations.get('adaptation_count', 0)
                }
            
            return adapted_patterns
            
        except Exception as e:
            self.logger.error(f"Error getting adapted patterns: {e}")
            return {}
    
    async def _load_learning_data(self):
        """Load existing learning data from database"""
        try:
            # Load pattern adaptations
            adapted_patterns = await self.get_adapted_patterns()
            self.pattern_adaptations = adapted_patterns
            
            self.logger.info(f"Loaded {len(self.pattern_adaptations)} pattern adaptations")
            
        except Exception as e:
            self.logger.error(f"Error loading learning data: {e}")
    
    async def _save_learning_data(self):
        """Save learning data (already handled by database)"""
        pass
    
    async def get_status(self) -> Dict[str, Any]:
        """Get feedback loop status"""
        try:
            cursor = self.db_connection.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM scan_results')
            scan_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM user_feedback')
            feedback_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM pattern_adaptations')
            adaptation_count = cursor.fetchone()[0]
            
            return {
                'initialized': self.is_initialized,
                'scan_count': scan_count,
                'feedback_count': feedback_count,
                'adaptation_count': adaptation_count,
                'learning_rate': self.learning_rate,
                'pattern_adaptations': len(self.pattern_adaptations),
                'database_path': self.db_path
            }
            
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {
                'initialized': self.is_initialized,
                'error': str(e)
            }
