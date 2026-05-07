"""
Resonance Interpretation Engine (AI Core)
Extracts meaningful insights from resonance patterns using ML and rule-based approaches
"""

import numpy as np
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class InterpretationConfig:
    """Configuration for resonance interpretation"""
    confidence_threshold: float = 0.7
    pattern_matching_threshold: float = 0.8
    anomaly_detection_threshold: float = 2.0  # Standard deviations
    learning_rate: float = 0.01
    model_update_frequency: int = 100  # Scans

class ResonanceInterpretationEngine:
    """AI-powered resonance pattern interpretation"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Interpretation parameters
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        self.pattern_threshold = config.get('pattern_matching_threshold', 0.8)
        self.anomaly_threshold = config.get('anomaly_detection_threshold', 2.0)
        
        # Pattern databases
        self.material_patterns = self._initialize_material_patterns()
        self.environment_patterns = self._initialize_environment_patterns()
        self.state_patterns = self._initialize_state_patterns()
        
        # Learning state
        self.scan_count = 0
        self.pattern_history = []
        self.anomaly_history = []
        
        # Rule-based interpretation rules
        self.interpretation_rules = self._initialize_interpretation_rules()
        
        self.is_initialized = False
        self.logger.info("Resonance Interpretation Engine created")
    
    def _initialize_material_patterns(self) -> Dict[str, Dict]:
        """Initialize known material resonance patterns"""
        return {
            'wood': {
                'characteristics': {
                    'resonance_peaks': [200, 400, 800, 1600],  # Typical harmonics
                    'q_factor_range': (10, 50),
                    'decay_time_range': (0.5, 2.0),
                    'harmonic_content': 0.7
                },
                'confidence_weight': 0.8
            },
            'metal': {
                'characteristics': {
                    'resonance_peaks': [500, 1000, 1500, 2000],
                    'q_factor_range': (50, 200),
                    'decay_time_range': (2.0, 5.0),
                    'harmonic_content': 0.9
                },
                'confidence_weight': 0.9
            },
            'glass': {
                'characteristics': {
                    'resonance_peaks': [1000, 2000, 3000, 4000],
                    'q_factor_range': (100, 500),
                    'decay_time_range': (0.1, 0.5),
                    'harmonic_content': 0.8
                },
                'confidence_weight': 0.85
            },
            'concrete': {
                'characteristics': {
                    'resonance_peaks': [100, 200, 300, 400],
                    'q_factor_range': (5, 20),
                    'decay_time_range': (0.2, 1.0),
                    'harmonic_content': 0.3
                },
                'confidence_weight': 0.7
            }
        }
    
    def _initialize_environment_patterns(self) -> Dict[str, Dict]:
        """Initialize known environment resonance patterns"""
        return {
            'small_room': {
                'characteristics': {
                    'room_mode_freqs': [50, 100, 150, 200],  # Room modes
                    'reverberation_time': (0.3, 0.8),
                    'frequency_rolloff': 2000,
                    'spatial_variance': 0.3
                },
                'confidence_weight': 0.8
            },
            'large_room': {
                'characteristics': {
                    'room_mode_freqs': [30, 60, 90, 120],
                    'reverberation_time': (0.8, 2.0),
                    'frequency_rolloff': 1500,
                    'spatial_variance': 0.5
                },
                'confidence_weight': 0.8
            },
            'open_space': {
                'characteristics': {
                    'room_mode_freqs': [],  # No distinct modes
                    'reverberation_time': (0.0, 0.2),
                    'frequency_rolloff': 3000,
                    'spatial_variance': 0.1
                },
                'confidence_weight': 0.7
            },
            'enclosed_space': {
                'characteristics': {
                    'room_mode_freqs': [80, 160, 240, 320],
                    'reverberation_time': (1.0, 3.0),
                    'frequency_rolloff': 1000,
                    'spatial_variance': 0.7
                },
                'confidence_weight': 0.85
            }
        }
    
    def _initialize_state_patterns(self) -> Dict[str, Dict]:
        """Initialize known state/condition patterns"""
        return {
            'stable': {
                'characteristics': {
                    'frequency_stability': 0.9,
                    'amplitude_consistency': 0.9,
                    'noise_level': 0.1,
                    'pattern_repetition': 0.8
                },
                'confidence_weight': 0.8
            },
            'stressed': {
                'characteristics': {
                    'frequency_stability': 0.3,
                    'amplitude_consistency': 0.4,
                    'noise_level': 0.6,
                    'pattern_repetition': 0.2
                },
                'confidence_weight': 0.7
            },
            'altered': {
                'characteristics': {
                    'frequency_shift': 0.5,
                    'new_resonances': True,
                    'missing_resonances': True,
                    'amplitude_change': 0.6
                },
                'confidence_weight': 0.8
            },
            'resonating': {
                'characteristics': {
                    'high_q_factor': True,
                    'sustained_decay': True,
                    'harmonic_enrichment': True,
                    'amplitude_amplification': True
                },
                'confidence_weight': 0.9
            }
        }
    
    def _initialize_interpretation_rules(self) -> List[Dict]:
        """Initialize rule-based interpretation rules"""
        return [
            {
                'name': 'resonance_peak_shift',
                'condition': lambda features: self._check_peak_shift(features),
                'interpretation': 'material_density_change',
                'confidence': 0.8
            },
            {
                'name': 'long_decay',
                'condition': lambda features: self._check_long_decay(features),
                'interpretation': 'reflective_environment',
                'confidence': 0.7
            },
            {
                'name': 'distortion_present',
                'condition': lambda features: self._check_distortion(features),
                'interpretation': 'structural_irregularity',
                'confidence': 0.8
            },
            {
                'name': 'high_q_factor',
                'condition': lambda features: self._check_high_q(features),
                'interpretation': 'resonant_material',
                'confidence': 0.7
            },
            {
                'name': 'frequency_shift',
                'condition': lambda features: self._check_frequency_shift(features),
                'interpretation': 'temperature_or_pressure_change',
                'confidence': 0.6
            }
        ]
    
    async def initialize(self):
        """Initialize interpretation engine"""
        try:
            # Load any saved patterns or models
            await self._load_saved_patterns()
            
            self.is_initialized = True
            self.logger.info("✅ Resonance Interpretation Engine initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize interpretation engine: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup interpretation resources"""
        # Save learned patterns
        await self._save_patterns()
        
        self.is_initialized = False
        self.logger.info("Resonance Interpretation Engine cleaned up")
    
    async def interpret_resonance(self, features: Dict[str, Any], 
                                 scan_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive resonance interpretation
        
        Args:
            features: Extracted signal features from processing layer
            scan_history: Previous scan results for comparison
            
        Returns:
            Dictionary containing interpretation results and insights
        """
        if not self.is_initialized:
            raise RuntimeError("Interpretation engine not initialized")
        
        interpretation_start = datetime.now()
        self.logger.info("🧠 Starting resonance interpretation...")
        
        try:
            self.scan_count += 1
            
            # 1. Rule-based interpretation
            rule_interpretations = await self._apply_rule_based_interpretation(features)
            
            # 2. Pattern matching
            material_matches = await self._match_material_patterns(features)
            environment_matches = await self._match_environment_patterns(features)
            state_matches = await self._match_state_patterns(features)
            
            # 3. Anomaly detection
            anomalies = await self._detect_anomalies(features, scan_history)
            
            # 4. Temporal analysis (if history available)
            temporal_insights = await self._analyze_temporal_changes(features, scan_history)
            
            # 5. Confidence calculation
            confidence_scores = await self._calculate_confidence(
                rule_interpretations, material_matches, environment_matches, 
                state_matches, anomalies
            )
            
            # 6. Generate insights summary
            insights = await self._generate_insights(
                rule_interpretations, material_matches, environment_matches,
                state_matches, anomalies, temporal_insights, confidence_scores
            )
            
            # 7. Learning update
            await self._update_learning(features, insights)
            
            # Create interpretation result
            interpretation_result = {
                'timestamp': interpretation_start.isoformat(),
                'scan_number': self.scan_count,
                'rule_interpretations': rule_interpretations,
                'pattern_matches': {
                    'materials': material_matches,
                    'environments': environment_matches,
                    'states': state_matches
                },
                'anomalies': anomalies,
                'temporal_insights': temporal_insights,
                'confidence_scores': confidence_scores,
                'insights': insights,
                'interpretation_metadata': {
                    'processing_time': (datetime.now() - interpretation_start).total_seconds(),
                    'patterns_considered': len(self.material_patterns) + len(self.environment_patterns) + len(self.state_patterns),
                    'rules_applied': len(self.interpretation_rules)
                }
            }
            
            processing_time = (datetime.now() - interpretation_start).total_seconds()
            self.logger.info(f"✅ Resonance interpretation completed in {processing_time:.3f}s")
            
            return interpretation_result
            
        except Exception as e:
            self.logger.error(f"Resonance interpretation failed: {e}")
            raise
    
    async def _apply_rule_based_interpretation(self, features: Dict[str, Any]) -> List[Dict]:
        """Apply rule-based interpretation rules"""
        interpretations = []
        
        for rule in self.interpretation_rules:
            try:
                if rule['condition'](features):
                    interpretation = {
                        'rule_name': rule['name'],
                        'interpretation': rule['interpretation'],
                        'confidence': rule['confidence'],
                        'evidence': self._extract_rule_evidence(rule, features)
                    }
                    interpretations.append(interpretation)
                    self.logger.debug(f"Rule matched: {rule['name']}")
            except Exception as e:
                self.logger.warning(f"Error applying rule {rule['name']}: {e}")
        
        return interpretations
    
    async def _match_material_patterns(self, features: Dict[str, Any]) -> List[Dict]:
        """Match resonance features against known material patterns"""
        matches = []
        
        for material, pattern in self.material_patterns.items():
            try:
                match_score = self._calculate_pattern_match(features, pattern['characteristics'])
                
                if match_score >= self.pattern_threshold:
                    match = {
                        'material': material,
                        'match_score': match_score,
                        'confidence': match_score * pattern['confidence_weight'],
                        'evidence': self._extract_material_evidence(features, pattern['characteristics'])
                    }
                    matches.append(match)
                    self.logger.debug(f"Material match: {material} (score: {match_score:.3f})")
            except Exception as e:
                self.logger.warning(f"Error matching material {material}: {e}")
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches
    
    async def _match_environment_patterns(self, features: Dict[str, Any]) -> List[Dict]:
        """Match resonance features against known environment patterns"""
        matches = []
        
        for environment, pattern in self.environment_patterns.items():
            try:
                match_score = self._calculate_pattern_match(features, pattern['characteristics'])
                
                if match_score >= self.pattern_threshold:
                    match = {
                        'environment': environment,
                        'match_score': match_score,
                        'confidence': match_score * pattern['confidence_weight'],
                        'evidence': self._extract_environment_evidence(features, pattern['characteristics'])
                    }
                    matches.append(match)
                    self.logger.debug(f"Environment match: {environment} (score: {match_score:.3f})")
            except Exception as e:
                self.logger.warning(f"Error matching environment {environment}: {e}")
        
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches
    
    async def _match_state_patterns(self, features: Dict[str, Any]) -> List[Dict]:
        """Match resonance features against known state patterns"""
        matches = []
        
        for state, pattern in self.state_patterns.items():
            try:
                match_score = self._calculate_pattern_match(features, pattern['characteristics'])
                
                if match_score >= self.pattern_threshold:
                    match = {
                        'state': state,
                        'match_score': match_score,
                        'confidence': match_score * pattern['confidence_weight'],
                        'evidence': self._extract_state_evidence(features, pattern['characteristics'])
                    }
                    matches.append(match)
                    self.logger.debug(f"State match: {state} (score: {match_score:.3f})")
            except Exception as e:
                self.logger.warning(f"Error matching state {state}: {e}")
        
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches
    
    async def _detect_anomalies(self, features: Dict[str, Any], 
                             scan_history: Optional[List[Dict]]) -> List[Dict]:
        """Detect anomalies in resonance patterns"""
        anomalies = []
        
        if not scan_history or len(scan_history) < 3:
            return anomalies  # Not enough history for anomaly detection
        
        try:
            # Extract current features for comparison
            current_features = self._extract_comparable_features(features)
            historical_features = [self._extract_comparable_features(scan.get('features', {})) 
                                 for scan in scan_history[-10:]]
            
            # Calculate statistical baselines
            feature_means = {}
            feature_stds = {}
            
            for feature_name in current_features.keys():
                values = [hist.get(feature_name, 0) for hist in historical_features]
                feature_means[feature_name] = np.mean(values)
                feature_stds[feature_name] = np.std(values)
            
            # Detect anomalies (values > threshold standard deviations from mean)
            for feature_name, current_value in current_features.items():
                if feature_name in feature_means and feature_stds[feature_name] > 0:
                    z_score = abs(current_value - feature_means[feature_name]) / feature_stds[feature_name]
                    
                    if z_score > self.anomaly_threshold:
                        anomaly = {
                            'feature': feature_name,
                            'current_value': current_value,
                            'baseline_mean': feature_means[feature_name],
                            'z_score': z_score,
                            'severity': 'high' if z_score > 3 else 'medium',
                            'description': f"Unusual {feature_name} detected"
                        }
                        anomalies.append(anomaly)
                        self.logger.warning(f"Anomaly detected: {feature_name} (z-score: {z_score:.2f})")
            
        except Exception as e:
            self.logger.error(f"Anomaly detection error: {e}")
        
        return anomalies
    
    async def _analyze_temporal_changes(self, features: Dict[str, Any],
                                     scan_history: Optional[List[Dict]]) -> Dict[str, Any]:
        """Analyze temporal changes in resonance patterns"""
        if not scan_history or len(scan_history) < 2:
            return {'status': 'insufficient_history'}
        
        try:
            # Compare with most recent scans
            recent_scans = scan_history[-5:]  # Last 5 scans
            changes = {}
            
            # Track frequency shifts
            current_peaks = [p['frequency'] for p in features.get('resonance_peaks', {}).get('resonance_peaks', [])[:5]]
            
            for i, scan in enumerate(recent_scans):
                scan_features = scan.get('features', {})
                scan_peaks = [p['frequency'] for p in scan_features.get('resonance_peaks', {}).get('resonance_peaks', [])[:5]]
                
                if scan_peaks and current_peaks:
                    # Calculate frequency shift
                    peak_shifts = []
                    for current_peak in current_peaks:
                        closest_scan_peak = min(scan_peaks, key=lambda x: abs(x - current_peak))
                        shift = abs(current_peak - closest_scan_peak) / closest_scan_peak if closest_scan_peak > 0 else 0
                        peak_shifts.append(shift)
                    
                    avg_shift = np.mean(peak_shifts) if peak_shifts else 0
                    changes[f'scan_{i+1}_ago'] = {
                        'frequency_shift': avg_shift,
                        'peak_count_change': len(current_peaks) - len(scan_peaks),
                        'amplitude_change': features.get('time_domain', {}).get('rms', 0) - scan_features.get('time_domain', {}).get('rms', 0)
                    }
            
            # Determine trend
            if changes:
                avg_frequency_shift = np.mean([c['frequency_shift'] for c in changes.values()])
                trend = 'stable' if avg_frequency_shift < 0.05 else 'changing'
            else:
                trend = 'unknown'
            
            return {
                'status': 'analyzed',
                'trend': trend,
                'changes': changes,
                'average_frequency_shift': avg_frequency_shift if changes else 0
            }
            
        except Exception as e:
            self.logger.error(f"Temporal analysis error: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def _calculate_confidence(self, rules: List[Dict], materials: List[Dict],
                                  environments: List[Dict], states: List[Dict],
                                  anomalies: List[Dict]) -> Dict[str, float]:
        """Calculate overall confidence scores"""
        confidences = {
            'rule_based': np.mean([r['confidence'] for r in rules]) if rules else 0.0,
            'material_matching': np.mean([m['confidence'] for m in materials]) if materials else 0.0,
            'environment_matching': np.mean([e['confidence'] for e in environments]) if environments else 0.0,
            'state_matching': np.mean([s['confidence'] for s in states]) if states else 0.0,
            'anomaly_detection': min(1.0, len(anomalies) * 0.2)  # More anomalies = higher confidence in detection
        }
        
        # Overall confidence (weighted average)
        weights = {
            'rule_based': 0.3,
            'material_matching': 0.2,
            'environment_matching': 0.2,
            'state_matching': 0.2,
            'anomaly_detection': 0.1
        }
        
        overall_confidence = sum(confidences[key] * weights[key] for key in confidences.keys())
        confidences['overall'] = overall_confidence
        
        return confidences
    
    async def _generate_insights(self, rules: List[Dict], materials: List[Dict],
                               environments: List[Dict], states: List[Dict],
                               anomalies: List[Dict], temporal: Dict[str, Any],
                               confidences: Dict[str, float]) -> List[str]:
        """Generate human-readable insights"""
        insights = []
        
        # Material insights
        if materials:
            best_material = materials[0]
            insights.append(f"Material detected: {best_material['material']} with {best_material['confidence']:.1%} confidence")
        
        # Environment insights
        if environments:
            best_environment = environments[0]
            insights.append(f"Environment type: {best_environment['environment']} with {best_environment['confidence']:.1%} confidence")
        
        # State insights
        if states:
            best_state = states[0]
            insights.append(f"System state: {best_state['state']} with {best_state['confidence']:.1%} confidence")
        
        # Rule-based insights
        for rule in rules[:3]:  # Top 3 rules
            insights.append(f"Rule-based: {rule['interpretation']} ({rule['confidence']:.1%} confidence)")
        
        # Anomaly insights
        if anomalies:
            insights.append(f"⚠️ {len(anomalies)} anomalies detected")
            for anomaly in anomalies[:2]:  # Top 2 anomalies
                insights.append(f"  - {anomaly['description']}")
        
        # Temporal insights
        if temporal.get('status') == 'analyzed':
            trend = temporal['trend']
            if trend == 'stable':
                insights.append("📊 System appears stable over recent scans")
            else:
                insights.append("📈 System showing changes over recent scans")
        
        # Overall confidence
        overall_conf = confidences['overall']
        if overall_conf >= self.confidence_threshold:
            insights.append(f"✅ High confidence interpretation ({overall_conf:.1%})")
        else:
            insights.append(f"⚠️ Low confidence interpretation ({overall_conf:.1%}) - more data needed")
        
        return insights
    
    def _calculate_pattern_match(self, features: Dict[str, Any], pattern: Dict[str, Any]) -> float:
        """Calculate how well features match a pattern"""
        match_scores = []
        
        for characteristic, expected_value in pattern.items():
            try:
                if characteristic == 'resonance_peaks':
                    score = self._compare_peak_patterns(features, expected_value)
                elif characteristic == 'q_factor_range':
                    score = self._compare_range(features, expected_value, 'q_factor')
                elif characteristic == 'decay_time_range':
                    score = self._compare_range(features, expected_value, 'decay_time')
                elif characteristic == 'harmonic_content':
                    score = self._compare_harmonic_content(features, expected_value)
                elif characteristic == 'room_mode_freqs':
                    score = self._compare_room_modes(features, expected_value)
                elif characteristic == 'reverberation_time':
                    score = self._compare_range(features, expected_value, 'decay_time')
                elif characteristic == 'frequency_rolloff':
                    score = self._compare_frequency_rolloff(features, expected_value)
                elif isinstance(expected_value, bool):
                    score = self._compare_boolean_feature(features, characteristic, expected_value)
                else:
                    score = self._compare_numeric_feature(features, characteristic, expected_value)
                
                match_scores.append(score)
            except Exception as e:
                self.logger.debug(f"Error comparing {characteristic}: {e}")
                match_scores.append(0.0)
        
        return np.mean(match_scores) if match_scores else 0.0
    
    def _compare_peak_patterns(self, features: Dict[str, Any], expected_peaks: List[float]) -> float:
        """Compare resonance peak patterns"""
        actual_peaks = features.get('resonance_peaks', {}).get('resonance_peaks', [])
        if not actual_peaks or not expected_peaks:
            return 0.0
        
        # Compare top peaks
        top_actual = [p['frequency'] for p in actual_peaks[:len(expected_peaks)]]
        
        matches = 0
        tolerance = 0.1  # 10% tolerance
        
        for expected in expected_peaks:
            for actual in top_actual:
                if abs(actual - expected) / expected <= tolerance:
                    matches += 1
                    break
        
        return matches / len(expected_peaks)
    
    def _compare_range(self, features: Dict[str, Any], expected_range: Tuple[float, float], 
                      feature_name: str) -> float:
        """Compare feature value against expected range"""
        # This is a simplified implementation - would need to extract actual values from features
        return 0.5  # Placeholder
    
    def _compare_harmonic_content(self, features: Dict[str, Any], expected: float) -> float:
        """Compare harmonic content"""
        harmonics = features.get('harmonics', {})
        hnr = harmonics.get('harmonic_to_noise_ratio', 0)
        
        # Normalize and compare
        normalized_hnr = min(1.0, hnr / 10)  # Assuming HNR max around 10
        return 1.0 - abs(normalized_hnr - expected)
    
    def _compare_room_modes(self, features: Dict[str, Any], expected_modes: List[float]) -> float:
        """Compare room mode frequencies"""
        # Simplified implementation
        return 0.5  # Placeholder
    
    def _compare_frequency_rolloff(self, features: Dict[str, Any], expected: float) -> float:
        """Compare frequency rolloff"""
        freq_domain = features.get('frequency_domain', {})
        rolloff = freq_domain.get('spectral_rolloff', 0)
        
        return 1.0 - min(1.0, abs(rolloff - expected) / expected)
    
    def _compare_boolean_feature(self, features: Dict[str, Any], feature_name: str, expected: bool) -> float:
        """Compare boolean feature"""
        # Simplified implementation
        return 0.5  # Placeholder
    
    def _compare_numeric_feature(self, features: Dict[str, Any], feature_name: str, expected: float) -> float:
        """Compare numeric feature"""
        # Navigate nested dictionary to find feature
        value = self._get_nested_feature(features, feature_name)
        if value is None:
            return 0.0
        
        return 1.0 - min(1.0, abs(value - expected) / max(abs(expected), 0.1))
    
    def _get_nested_feature(self, features: Dict[str, Any], feature_name: str):
        """Get feature value from nested dictionary"""
        # Simplified implementation - would need proper navigation
        return None
    
    # Rule condition methods
    def _check_peak_shift(self, features: Dict[str, Any]) -> bool:
        """Check for resonance peak shift"""
        # Simplified implementation
        return False
    
    def _check_long_decay(self, features: Dict[str, Any]) -> bool:
        """Check for long decay time"""
        envelope = features.get('envelope', {})
        decay_time = envelope.get('decay_time', 0)
        return decay_time > 2.0
    
    def _check_distortion(self, features: Dict[str, Any]) -> bool:
        """Check for distortion presence"""
        noise = features.get('noise_analysis', {})
        thd = noise.get('total_harmonic_distortion', 0)
        return thd > 0.1
    
    def _check_high_q(self, features: Dict[str, Any]) -> bool:
        """Check for high Q factor"""
        resonance = features.get('resonance_peaks', {})
        dominant = resonance.get('dominant_resonance', {})
        q_factor = dominant.get('q_factor', 0) if dominant else 0
        return q_factor > 50
    
    def _check_frequency_shift(self, features: Dict[str, Any]) -> bool:
        """Check for frequency shift"""
        # Would need historical comparison
        return False
    
    def _extract_rule_evidence(self, rule: Dict, features: Dict[str, Any]) -> Dict[str, Any]:
        """Extract evidence for rule interpretation"""
        return {'feature_values': 'extracted'}  # Placeholder
    
    def _extract_material_evidence(self, features: Dict[str, Any], pattern: Dict) -> Dict[str, Any]:
        """Extract evidence for material matching"""
        return {'matching_features': 'extracted'}  # Placeholder
    
    def _extract_environment_evidence(self, features: Dict[str, Any], pattern: Dict) -> Dict[str, Any]:
        """Extract evidence for environment matching"""
        return {'matching_features': 'extracted'}  # Placeholder
    
    def _extract_state_evidence(self, features: Dict[str, Any], pattern: Dict) -> Dict[str, Any]:
        """Extract evidence for state matching"""
        return {'matching_features': 'extracted'}  # Placeholder
    
    def _extract_comparable_features(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Extract features suitable for statistical comparison"""
        comparable = {}
        
        # Extract key numeric features
        time_domain = features.get('time_domain', {})
        comparable['rms'] = time_domain.get('rms', 0)
        comparable['peak'] = time_domain.get('peak', 0)
        
        freq_domain = features.get('frequency_domain', {})
        comparable['spectral_centroid'] = freq_domain.get('spectral_centroid', 0)
        comparable['dominant_frequency'] = freq_domain.get('dominant_frequency', 0)
        
        resonance = features.get('resonance_peaks', {})
        comparable['peak_count'] = len(resonance.get('resonance_peaks', []))
        
        return comparable
    
    async def _update_learning(self, features: Dict[str, Any], insights: Dict[str, Any]):
        """Update learning from current interpretation"""
        # Store pattern for future learning
        pattern_entry = {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'insights': insights
        }
        
        self.pattern_history.append(pattern_entry)
        
        # Keep only recent patterns
        if len(self.pattern_history) > 1000:
            self.pattern_history = self.pattern_history[-1000:]
    
    async def _load_saved_patterns(self):
        """Load saved patterns and learning data"""
        # Placeholder for loading from database/file
        pass
    
    async def _save_patterns(self):
        """Save learned patterns"""
        # Placeholder for saving to database/file
        pass
    
    async def get_status(self) -> Dict[str, Any]:
        """Get interpretation engine status"""
        return {
            'initialized': self.is_initialized,
            'scan_count': self.scan_count,
            'pattern_history_size': len(self.pattern_history),
            'material_patterns': len(self.material_patterns),
            'environment_patterns': len(self.environment_patterns),
            'state_patterns': len(self.state_patterns),
            'interpretation_rules': len(self.interpretation_rules)
        }
