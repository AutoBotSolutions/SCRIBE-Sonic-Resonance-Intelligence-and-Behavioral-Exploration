"""
SCRIBE Monitoring and Analytics System
Real-time system monitoring, performance tracking, and analytics
"""

import asyncio
import time
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import numpy as np
from prometheus_client import Counter, Histogram, Gauge, start_http_server

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: str
    scan_duration: float
    processing_time: float
    confidence_score: float
    anomaly_count: int
    signal_quality: float
    system_load: float

@dataclass
class SystemHealth:
    """System health metrics"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    audio_device_status: bool
    database_status: bool
    error_rate: float

class AnalyticsEngine:
    """Advanced analytics and monitoring for SCRIBE system"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Metrics storage
        self.performance_history = []
        self.health_history = []
        self.alert_history = []
        
        # Prometheus metrics
        self.scan_counter = Counter('scribe_scans_total', 'Total scans performed')
        self.scan_duration = Histogram('scribe_scan_duration_seconds', 'Scan duration')
        self.confidence_gauge = Gauge('scribe_confidence_score', 'Latest confidence score')
        self.anomaly_counter = Counter('scribe_anomalies_total', 'Total anomalies detected')
        self.system_load_gauge = Gauge('scribe_system_load', 'System load percentage')
        
        # Alert thresholds
        self.alert_thresholds = {
            'scan_duration': 5.0,  # seconds
            'confidence_score': 0.5,
            'anomaly_rate': 0.3,
            'error_rate': 0.05,
            'system_load': 0.8,
            'memory_usage': 0.9
        }
        
        # Analytics state
        self.is_monitoring = False
        self.monitoring_task = None
        
        self.logger.info("Analytics Engine initialized")
    
    async def start_monitoring(self, port: int = 8001):
        """Start monitoring and metrics collection"""
        try:
            # Start Prometheus metrics server
            start_http_server(port)
            self.logger.info(f"📊 Prometheus metrics server started on port {port}")
            
            # Start background monitoring
            self.is_monitoring = True
            self.monitoring_task = asyncio.create_task(self._monitoring_loop())
            
            self.logger.info("✅ Analytics monitoring started")
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            raise
    
    async def stop_monitoring(self):
        """Stop monitoring and metrics collection"""
        self.is_monitoring = False
        
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("🛑 Analytics monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect system health metrics
                health = await self._collect_system_health()
                self.health_history.append(health)
                
                # Update system load gauge
                self.system_load_gauge.set(health.cpu_usage)
                
                # Check for alerts
                await self._check_alerts(health)
                
                # Cleanup old data (keep last 24 hours)
                await self._cleanup_old_data()
                
                # Sleep for monitoring interval
                await asyncio.sleep(30)  # 30 second intervals
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def record_scan_metrics(self, scan_result: Dict[str, Any]):
        """Record metrics from a completed scan"""
        try:
            # Extract timing information
            interpretation = scan_result.get('interpretation', {})
            processing_metadata = interpretation.get('interpretation_metadata', {})
            
            metrics = PerformanceMetrics(
                timestamp=datetime.now().isoformat(),
                scan_duration=processing_metadata.get('processing_time', 0),
                processing_time=processing_metadata.get('processing_time', 0),
                confidence_score=interpretation.get('confidence_scores', {}).get('overall', 0),
                anomaly_count=len(interpretation.get('anomalies', [])),
                signal_quality=self._calculate_signal_quality(scan_result),
                system_load=self._get_current_system_load()
            )
            
            # Store metrics
            self.performance_history.append(metrics)
            
            # Update Prometheus metrics
            self.scan_counter.inc()
            self.scan_duration.observe(metrics.scan_duration)
            self.confidence_gauge.set(metrics.confidence_score)
            self.anomaly_counter.inc(metrics.anomaly_count)
            
            self.logger.debug(f"Recorded scan metrics: confidence={metrics.confidence_score:.2f}, duration={metrics.scan_duration:.3f}s")
            
        except Exception as e:
            self.logger.error(f"Failed to record scan metrics: {e}")
    
    def _calculate_signal_quality(self, scan_result: Dict[str, Any]) -> float:
        """Calculate signal quality score from scan result"""
        try:
            response_metadata = scan_result.get('response', {}).get('metadata', {})
            features = scan_result.get('features', {})
            
            # Factors affecting signal quality
            snr = response_metadata.get('amplitude_stats', {}).get('dynamic_range', 0)
            peak_count = len(features.get('resonance_peaks', {}).get('resonance_peaks', []))
            spectral_centroid = features.get('frequency_domain', {}).get('spectral_centroid', 0)
            
            # Normalize factors (0-1 scale)
            snr_score = min(1.0, snr / 40)  # 40dB dynamic range as reference
            peak_score = min(1.0, peak_count / 10)  # 10 peaks as reference
            spectral_score = min(1.0, spectral_centroid / 5000)  # 5kHz as reference
            
            # Weighted average
            quality = (snr_score * 0.4 + peak_score * 0.3 + spectral_score * 0.3)
            
            return quality
            
        except Exception as e:
            self.logger.error(f"Signal quality calculation error: {e}")
            return 0.5  # Default medium quality
    
    def _get_current_system_load(self) -> float:
        """Get current system load"""
        try:
            import psutil
            return psutil.cpu_percent() / 100.0
        except ImportError:
            return 0.0  # Default if psutil not available
    
    async def _collect_system_health(self) -> SystemHealth:
        """Collect system health metrics"""
        try:
            import psutil
            
            # CPU and memory
            cpu_usage = psutil.cpu_percent() / 100.0
            memory = psutil.virtual_memory()
            memory_usage = memory.percent / 100.0
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent / 100.0
            
            # Service status (simplified)
            audio_device_status = True  # Would need actual check
            database_status = True     # Would need actual check
            
            # Error rate (from recent performance history)
            error_rate = self._calculate_recent_error_rate()
            
            return SystemHealth(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                audio_device_status=audio_device_status,
                database_status=database_status,
                error_rate=error_rate
            )
            
        except ImportError:
            # Fallback if psutil not available
            return SystemHealth(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                audio_device_status=True,
                database_status=True,
                error_rate=0.0
            )
        except Exception as e:
            self.logger.error(f"Health collection error: {e}")
            return SystemHealth(0, 0, 0, False, False, 1.0)
    
    def _calculate_recent_error_rate(self) -> float:
        """Calculate error rate from recent scans"""
        if not self.performance_history:
            return 0.0
        
        # Look at last 100 scans
        recent_scans = self.performance_history[-100:]
        
        # Count scans with low confidence as "errors"
        error_count = sum(1 for scan in recent_scans if scan.confidence_score < 0.5)
        
        return error_count / len(recent_scans) if recent_scans else 0.0
    
    async def _check_alerts(self, health: SystemHealth):
        """Check for alert conditions"""
        alerts = []
        
        # Check each threshold
        if health.cpu_usage > self.alert_thresholds['system_load']:
            alerts.append({
                'type': 'system_load',
                'severity': 'warning',
                'message': f"High CPU usage: {health.cpu_usage:.1%}",
                'timestamp': datetime.now().isoformat()
            })
        
        if health.memory_usage > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'memory_usage',
                'severity': 'critical',
                'message': f"High memory usage: {health.memory_usage:.1%}",
                'timestamp': datetime.now().isoformat()
            })
        
        if health.error_rate > self.alert_thresholds['error_rate']:
            alerts.append({
                'type': 'error_rate',
                'severity': 'warning',
                'message': f"High error rate: {health.error_rate:.1%}",
                'timestamp': datetime.now().isoformat()
            })
        
        # Store alerts
        for alert in alerts:
            self.alert_history.append(alert)
            self.logger.warning(f"ALERT: {alert['message']}")
    
    async def _cleanup_old_data(self):
        """Clean up old metrics data"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        # Clean performance history
        self.performance_history = [
            m for m in self.performance_history
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        # Clean health history
        self.health_history = [
            h for h in self.health_history
            if datetime.fromisoformat(h.timestamp) > cutoff_time
        ]
        
        # Keep only last 1000 alerts
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
    
    async def get_analytics_summary(self) -> Dict[str, Any]:
        """Get comprehensive analytics summary"""
        try:
            # Recent performance summary
            if self.performance_history:
                recent_performance = self.performance_history[-100:]
                avg_confidence = np.mean([p.confidence_score for p in recent_performance])
                avg_duration = np.mean([p.scan_duration for p in recent_performance])
                total_anomalies = sum([p.anomaly_count for p in recent_performance])
            else:
                avg_confidence = 0.0
                avg_duration = 0.0
                total_anomalies = 0
            
            # System health summary
            if self.health_history:
                current_health = self.health_history[-1]
                avg_cpu = np.mean([h.cpu_usage for h in self.health_history[-60:]])  # Last hour
                avg_memory = np.mean([h.memory_usage for h in self.health_history[-60:]])
            else:
                current_health = SystemHealth(0, 0, 0, True, True, 0)
                avg_cpu = 0.0
                avg_memory = 0.0
            
            # Alert summary
            recent_alerts = [
                a for a in self.alert_history
                if datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(hours=1)
            ]
            
            return {
                'timestamp': datetime.now().isoformat(),
                'performance_summary': {
                    'total_scans': len(self.performance_history),
                    'average_confidence': avg_confidence,
                    'average_scan_duration': avg_duration,
                    'total_anomalies': total_anomalies,
                    'recent_scans': len(recent_performance)
                },
                'system_health': {
                    'current_cpu': current_health.cpu_usage,
                    'current_memory': current_health.memory_usage,
                    'average_cpu': avg_cpu,
                    'average_memory': avg_memory,
                    'services_healthy': current_health.audio_device_status and current_health.database_status
                },
                'alerts': {
                    'recent_count': len(recent_alerts),
                    'recent_alerts': recent_alerts[-10:],  # Last 10 alerts
                    'total_alerts': len(self.alert_history)
                },
                'metrics_endpoints': {
                    'prometheus': 'http://localhost:8001/metrics'
                }
            }
            
        except Exception as e:
            self.logger.error(f"Analytics summary error: {e}")
            return {'error': str(e)}
    
    async def get_performance_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance trends over time"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter recent performance data
            recent_metrics = [
                m for m in self.performance_history
                if datetime.fromisoformat(m.timestamp) > cutoff_time
            ]
            
            if not recent_metrics:
                return {'message': 'No data available for specified time range'}
            
            # Calculate trends
            timestamps = [datetime.fromisoformat(m.timestamp) for m in recent_metrics]
            confidences = [m.confidence_score for m in recent_metrics]
            durations = [m.scan_duration for m in recent_metrics]
            
            # Simple trend analysis (linear regression)
            def calculate_trend(values):
                if len(values) < 2:
                    return 0.0
                
                x = np.arange(len(values))
                coeffs = np.polyfit(x, values, 1)
                return coeffs[0]  # Slope
            
            confidence_trend = calculate_trend(confidences)
            duration_trend = calculate_trend(durations)
            
            return {
                'time_range_hours': hours,
                'data_points': len(recent_metrics),
                'trends': {
                    'confidence': {
                        'slope': confidence_trend,
                        'direction': 'improving' if confidence_trend > 0 else 'declining',
                        'current_avg': np.mean(confidences[-10:]) if len(confidences) >= 10 else np.mean(confidences)
                    },
                    'duration': {
                        'slope': duration_trend,
                        'direction': 'slowing' if duration_trend > 0 else 'improving',
                        'current_avg': np.mean(durations[-10:]) if len(durations) >= 10 else np.mean(durations)
                    }
                },
                'period_start': timestamps[0].isoformat(),
                'period_end': timestamps[-1].isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Performance trends error: {e}")
            return {'error': str(e)}
    
    async def export_metrics(self, format: str = 'json') -> Dict[str, Any]:
        """Export metrics data"""
        try:
            if format.lower() == 'json':
                return {
                    'performance_history': [asdict(m) for m in self.performance_history],
                    'health_history': [asdict(h) for h in self.health_history],
                    'alert_history': self.alert_history,
                    'export_timestamp': datetime.now().isoformat()
                }
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            self.logger.error(f"Metrics export error: {e}")
            return {'error': str(e)}
