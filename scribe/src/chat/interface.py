"""
Chat Interface
User interaction layer for SCRIBE resonance intelligence system
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class ChatInterface:
    """Interactive chat interface for SCRIBE system"""
    
    def __init__(self, system_controller):
        self.system = system_controller
        self.logger = logging.getLogger(__name__)
        
        # Chat state
        self.is_running = False
        self.current_session = None
        self.chat_history = []
        
        # Command handlers
        self.commands = {
            'scan': self._handle_scan_command,
            'status': self._handle_status_command,
            'history': self._handle_history_command,
            'help': self._handle_help_command,
            'feedback': self._handle_feedback_command,
            'learning': self._handle_learning_command,
            'compare': self._handle_compare_command,
            'analyze': self._handle_analyze_command,
            'stop': self._handle_stop_command,
            'exit': self._handle_exit_command
        }
        
        self.logger.info("Chat Interface initialized")
    
    async def start(self):
        """Start the chat interface"""
        self.logger.info("🗣️ Starting SCRIBE Chat Interface...")
        
        try:
            # Start the system
            await self.system.start()
            
            self.is_running = True
            self.current_session = datetime.now().isoformat()
            
            print("\n" + "="*60)
            print("🧠 SCRIBE Resonance AI System - Chat Interface")
            print("="*60)
            print("Welcome to SCRIBE! I'm ready to help you explore environments")
            print("through resonance intelligence technology.")
            print("\nType 'help' for available commands or just ask me questions!")
            print("-"*60)
            
            # Main chat loop
            await self._chat_loop()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            self.logger.error(f"Chat interface error: {e}")
            print(f"\n❌ Error: {e}")
        finally:
            await self._shutdown()
    
    async def _chat_loop(self):
        """Main chat interaction loop"""
        while self.is_running:
            try:
                # Get user input
                user_input = input("\n🔍 SCRIBE> ").strip()
                
                if not user_input:
                    continue
                
                # Add to chat history
                self.chat_history.append({
                    'type': 'user',
                    'message': user_input,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Process input
                response = await self._process_input(user_input)
                
                # Display response
                if response:
                    print(f"\n🤖 SCRIBE: {response}")
                    self.chat_history.append({
                        'type': 'assistant',
                        'message': response,
                        'timestamp': datetime.now().isoformat()
                    })
                
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Chat loop error: {e}")
                print(f"❌ Error: {e}")
    
    async def _process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        user_input_lower = user_input.lower()
        
        # Check for commands
        if user_input_lower.startswith('/'):
            command_parts = user_input[1:].split()
            command = command_parts[0]
            args = command_parts[1:] if len(command_parts) > 1 else []
            
            if command in self.commands:
                return await self.commands[command](args)
            else:
                return f"Unknown command: /{command}. Type '/help' for available commands."
        
        # Natural language processing
        elif any(keyword in user_input_lower for keyword in ['scan', 'resonance', 'analyze', 'detect']):
            return await self._handle_natural_scan(user_input)
        
        elif any(keyword in user_input_lower for keyword in ['what', 'how', 'explain', 'tell me']):
            return await self._handle_question(user_input)
        
        elif any(keyword in user_input_lower for keyword in ['compare', 'difference', 'change']):
            return await self._handle_natural_compare(user_input)
        
        elif any(keyword in user_input_lower for keyword in ['status', 'health', 'working']):
            return await self._handle_status_command([])
        
        else:
            return await self._handle_general_query(user_input)
    
    async def _handle_scan_command(self, args: List[str]) -> str:
        """Handle scan command"""
        try:
            print("\n🔊 Initiating resonance scan...")
            
            # Parse scan configuration from args
            scan_config = self._parse_scan_args(args)
            
            # Perform scan
            result = await self.system.perform_resonance_scan(scan_config)
            
            # Generate summary
            interpretation = result.get('interpretation', {})
            insights = interpretation.get('insights', [])
            confidence = interpretation.get('confidence_scores', {}).get('overall', 0)
            
            response = f"✅ Scan completed with {confidence:.1%} confidence\n\n"
            response += "🔍 Key Findings:\n"
            
            for insight in insights[:5]:  # Top 5 insights
                response += f"• {insight}\n"
            
            # Add material/environment info if available
            pattern_matches = interpretation.get('pattern_matches', {})
            
            if pattern_matches.get('materials'):
                best_material = pattern_matches['materials'][0]
                response += f"\n🪵 Material: {best_material['material']} ({best_material['confidence']:.1%})"
            
            if pattern_matches.get('environments'):
                best_env = pattern_matches['environments'][0]
                response += f"\n🏠 Environment: {best_env['environment']} ({best_env['confidence']:.1%})"
            
            if interpretation.get('anomalies'):
                anomalies = interpretation['anomalies']
                response += f"\n⚠️ {len(anomalies)} anomalies detected"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Scan command error: {e}")
            return f"❌ Scan failed: {e}"
    
    async def _handle_status_command(self, args: List[str]) -> str:
        """Handle status command"""
        try:
            status = await self.system.get_system_status()
            
            response = "📊 System Status:\n\n"
            
            # Overall status
            response += f"System Running: {'✅ Yes' if status['system_running'] else '❌ No'}\n"
            response += f"Total Scans: {status['scan_count']}\n"
            
            if status.get('last_scan'):
                response += f"Last Scan: {status['last_scan']}\n"
            
            # Component status
            response += "\n🔧 Components:\n"
            for component, comp_status in status['components'].items():
                status_icon = "✅" if comp_status.get('initialized', False) else "❌"
                response += f"  {status_icon} {component.replace('_', ' ').title()}\n"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Status command error: {e}")
            return f"❌ Status check failed: {e}"
    
    async def _handle_history_command(self, args: List[str]) -> str:
        """Handle history command"""
        try:
            limit = 5  # Default limit
            if args and args[0].isdigit():
                limit = int(args[0])
            
            history = self.system.get_scan_history(limit)
            
            if not history:
                return "📝 No scan history available."
            
            response = f"📝 Recent {len(history)} Scans:\n\n"
            
            for i, scan in enumerate(history, 1):
                timestamp = scan.get('timestamp', 'Unknown')
                interpretation = scan.get('interpretation', {})
                insights = interpretation.get('insights', [])
                
                response += f"{i}. {timestamp}\n"
                if insights:
                    response += f"   Top insight: {insights[0]}\n"
                response += "\n"
            
            return response
            
        except Exception as e:
            self.logger.error(f"History command error: {e}")
            return f"❌ History retrieval failed: {e}"
    
    async def _handle_help_command(self, args: List[str]) -> str:
        """Handle help command"""
        response = "📖 SCRIBE Commands:\n\n"
        
        response += "🔍 Scanning:\n"
        response += "  /scan [options]     - Perform resonance scan\n"
        response += "  /analyze            - Analyze current environment\n"
        response += "  /compare [scan_id]   - Compare with previous scan\n\n"
        
        response += "📊 Information:\n"
        response += "  /status             - Show system status\n"
        response += "  /history [count]     - Show scan history\n"
        response += "  /learning           - Show learning insights\n\n"
        
        response += "🔄 Feedback:\n"
        response += "  /feedback <type>    - Provide feedback on last scan\n"
        response += "                      Types: material, environment, state, rating\n\n"
        
        response += "💬 Natural Language:\n"
        response += "  'What did you detect?' - Get scan results\n"
        response += "  'Is this stable?'      - Check system state\n"
        response += "  'What changed?'        - Compare with previous\n"
        response += "  'Scan the room'        - Perform scan\n\n"
        
        response += "🛑 Control:\n"
        response += "  /stop               - Stop current operations\n"
        response += "  /exit               - Exit the system\n"
        
        return response
    
    async def _handle_feedback_command(self, args: List[str]) -> str:
        """Handle feedback command"""
        if not args:
            return "📝 Usage: /feedback <type> <data>\nTypes: material, environment, state, rating"
        
        feedback_type = args[0].lower()
        
        if feedback_type not in ['material', 'environment', 'state', 'rating']:
            return "❌ Invalid feedback type. Use: material, environment, state, or rating"
        
        # Get last scan for feedback
        history = self.system.get_scan_history(1)
        if not history:
            return "❌ No recent scan to provide feedback on"
        
        last_scan = history[0]
        
        if feedback_type == 'rating':
            return await self._handle_rating_feedback(last_scan, args[1:])
        else:
            return await self._handle_correction_feedback(last_scan, feedback_type, args[1:])
    
    async def _handle_rating_feedback(self, scan: Dict[str, Any], args: List[str]) -> str:
        """Handle rating feedback"""
        if not args or not args[0].isdigit():
            return "📝 Usage: /feedback rating <1-5>"
        
        rating = int(args[0])
        if rating < 1 or rating > 5:
            return "❌ Rating must be between 1 and 5"
        
        try:
            # Add feedback to learning system
            await self.system.feedback_loop.add_user_feedback(
                scan_id=1,  # Would need actual scan ID
                feedback_type="interpretation_rating",
                feedback_data={"rating": rating}
            )
            
            return f"✅ Thank you for the {rating}/5 rating! This helps improve my accuracy."
            
        except Exception as e:
            self.logger.error(f"Rating feedback error: {e}")
            return f"❌ Failed to save rating: {e}"
    
    async def _handle_correction_feedback(self, scan: Dict[str, Any], 
                                         feedback_type: str, args: List[str]) -> str:
        """Handle correction feedback"""
        if not args:
            return f"📝 Usage: /feedback {feedback_type} <correct_value>"
        
        correct_value = ' '.join(args)
        
        try:
            # Get current interpretation
            interpretation = scan.get('interpretation', {})
            pattern_matches = interpretation.get('pattern_matches', {})
            
            current_value = "unknown"
            if feedback_type == 'material' and pattern_matches.get('materials'):
                current_value = pattern_matches['materials'][0].get('material', 'unknown')
            elif feedback_type == 'environment' and pattern_matches.get('environments'):
                current_value = pattern_matches['environments'][0].get('environment', 'unknown')
            elif feedback_type == 'state' and pattern_matches.get('states'):
                current_value = pattern_matches['states'][0].get('state', 'unknown')
            
            # Add feedback to learning system
            feedback_data = {
                'correct_value': correct_value,
                'incorrect_value': current_value,
                f'correct_{feedback_type}': correct_value,
                f'incorrect_{feedback_type}': current_value
            }
            
            await self.system.feedback_loop.add_user_feedback(
                scan_id=1,  # Would need actual scan ID
                feedback_type=f"{feedback_type}_correction",
                feedback_data=feedback_data
            )
            
            return f"✅ Thanks! I'll learn that this is {correct_value} instead of {current_value}."
            
        except Exception as e:
            self.logger.error(f"Correction feedback error: {e}")
            return f"❌ Failed to save correction: {e}"
    
    async def _handle_learning_command(self, args: List[str]) -> str:
        """Handle learning command"""
        try:
            insights = await self.system.feedback_loop.get_learning_insights()
            
            if not insights:
                return "📚 No learning data available yet."
            
            response = "📚 Learning Insights:\n\n"
            response += f"Total Scans: {insights.get('total_scans', 0)}\n"
            response += f"User Feedback: {insights.get('total_feedback', 0)}\n"
            response += f"Pattern Adaptations: {insights.get('pattern_adaptations_count', 0)}\n\n"
            
            # Show top adapted patterns
            top_patterns = insights.get('top_adapted_patterns', [])
            if top_patterns:
                response += "🎯 Top Adapted Patterns:\n"
                for pattern in top_patterns[:5]:
                    response += f"  {pattern['type']}: {pattern['name']} (used {pattern['usage_count']} times)\n"
            
            # Show recent performance
            metrics = insights.get('recent_performance_metrics', {})
            if metrics:
                response += "\n📈 Recent Performance:\n"
                for metric, value in metrics.items():
                    if 'confidence' in metric:
                        response += f"  {metric}: {value:.1%}\n"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Learning command error: {e}")
            return f"❌ Learning insights failed: {e}"
    
    async def _handle_compare_command(self, args: List[str]) -> str:
        """Handle compare command"""
        try:
            history = self.system.get_scan_history(2)
            
            if len(history) < 2:
                return "📝 Need at least 2 scans to compare. Use /scan first."
            
            current_scan = history[-1]
            previous_scan = history[-2]
            
            # Extract key features for comparison
            current_features = current_scan.get('features', {})
            previous_features = previous_scan.get('features', {})
            
            response = "🔍 Scan Comparison:\n\n"
            
            # Compare dominant frequencies
            current_freq = current_features.get('frequency_domain', {}).get('dominant_frequency', 0)
            previous_freq = previous_features.get('frequency_domain', {}).get('dominant_frequency', 0)
            
            if current_freq > 0 and previous_freq > 0:
                freq_change = abs(current_freq - previous_freq)
                freq_percent = (freq_change / previous_freq) * 100
                response += f"🎵 Dominant Frequency: {current_freq:.1f}Hz (change: {freq_percent:.1f}%)\n"
            
            # Compare RMS levels
            current_rms = current_features.get('time_domain', {}).get('rms', 0)
            previous_rms = previous_features.get('time_domain', {}).get('rms', 0)
            
            if current_rms > 0 and previous_rms > 0:
                rms_change = abs(current_rms - previous_rms)
                rms_percent = (rms_change / previous_rms) * 100
                response += f"📊 RMS Level: {current_rms:.4f} (change: {rms_percent:.1f}%)\n"
            
            # Compare resonance peaks
            current_peaks = current_features.get('resonance_peaks', {}).get('resonance_peaks', [])
            previous_peaks = previous_features.get('resonance_peaks', {}).get('resonance_peaks', [])
            
            response += f"🔔 Resonance Peaks: {len(current_peaks)} vs {len(previous_peaks)}\n"
            
            # Check for anomalies
            current_interpretation = current_scan.get('interpretation', {})
            current_anomalies = current_interpretation.get('anomalies', [])
            
            if current_anomalies:
                response += f"⚠️ Current scan has {len(current_anomalies)} anomalies\n"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Compare command error: {e}")
            return f"❌ Comparison failed: {e}"
    
    async def _handle_analyze_command(self, args: List[str]) -> str:
        """Handle analyze command"""
        return await self._handle_scan_command(args)
    
    async def _handle_stop_command(self, args: List[str]) -> str:
        """Handle stop command"""
        return "🛑 Use /exit to stop the system."
    
    async def _handle_exit_command(self, args: List[str]) -> str:
        """Handle exit command"""
        self.is_running = False
        return "👋 Shutting down SCRIBE system..."
    
    async def _handle_natural_scan(self, user_input: str) -> str:
        """Handle natural language scan requests"""
        return await self._handle_scan_command([])
    
    async def _handle_question(self, user_input: str) -> str:
        """Handle general questions"""
        user_input_lower = user_input.lower()
        
        if 'what did you detect' in user_input_lower:
            history = self.system.get_scan_history(1)
            if history:
                scan = history[0]
                interpretation = scan.get('interpretation', {})
                insights = interpretation.get('insights', [])
                
                if insights:
                    return f"🔍 Latest detection: {insights[0]}"
                else:
                    return "📝 No recent detections. Use /scan to analyze the environment."
            else:
                return "📝 No scan data available. Use /scan to analyze the environment."
        
        elif 'how does it work' in user_input_lower:
            return """🧠 SCRIBE works through resonance intelligence:
            
1. 🔊 I emit controlled acoustic signals
2. 🎙️ I capture environmental responses
3. 📊 I analyze the signal patterns
4. 🧠 I interpret what the patterns mean
5. 📚 I learn and improve over time

Think of it like active sonar, but for understanding materials and environments!"""
        
        elif 'stable' in user_input_lower:
            history = self.system.get_scan_history(1)
            if history:
                scan = history[0]
                interpretation = scan.get('interpretation', {})
                state_matches = interpretation.get('pattern_matches', {}).get('states', [])
                
                if state_matches:
                    best_state = state_matches[0]
                    confidence = best_state['confidence']
                    if confidence > 0.7 and best_state['state'] == 'stable':
                        return f"✅ Environment appears stable ({confidence:.1%} confidence)"
                    else:
                        return f"⚠️ Environment shows changes or instability ({confidence:.1%} confidence)"
                else:
                    return "📝 Need more data to determine stability. Try another scan."
            else:
                return "📝 No recent scan data. Use /scan to check stability."
        
        else:
            return "🤔 I can help you analyze environments through resonance! Try asking:\n• 'What did you detect?'\n• 'Is this environment stable?'\n• 'How does it work?'\n• Or use /scan to start analyzing!"
    
    async def _handle_natural_compare(self, user_input: str) -> str:
        """Handle natural language compare requests"""
        return await self._handle_compare_command([])
    
    async def _handle_general_query(self, user_input: str) -> str:
        """Handle general queries"""
        return """🤖 I'm SCRIBE, a resonance intelligence system!

I can help you:
🔍 Analyze environments through acoustic resonance
📊 Detect materials and structural properties
⚠️ Identify changes and anomalies
📚 Learn and improve from feedback

Try these commands:
• /scan - Analyze current environment
• /status - Check system status
• /help - See all commands
• Or ask: "What did you detect?" """
    
    def _parse_scan_args(self, args: List[str]) -> Dict[str, Any]:
        """Parse scan command arguments"""
        config = {}
        
        # Simple argument parsing for now
        # Could be extended to support more complex configurations
        for i, arg in enumerate(args):
            if arg.startswith('--duration='):
                config['duration'] = float(arg.split('=')[1])
            elif arg.startswith('--frequency='):
                config['frequency'] = float(arg.split('=')[1])
            elif arg.startswith('--type='):
                config['signal_type'] = arg.split('=')[1]
        
        return config
    
    async def _shutdown(self):
        """Shutdown the chat interface and system"""
        try:
            self.is_running = False
            await self.system.stop()
            self.logger.info("Chat interface shutdown complete")
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
