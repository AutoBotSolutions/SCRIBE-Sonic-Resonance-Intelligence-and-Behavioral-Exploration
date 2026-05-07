"""
SCRIBE API Server
FastAPI-based REST API for SCRIBE Resonance AI System
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime

from core.system_controller import ScribeSystemController
from utils.config import Config
from utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SCRIBE Resonance AI API",
    description="REST API for SCRIBE Resonance Intelligence System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global system controller
system_controller = None
config = None

# Pydantic models for API
class ScanRequest(BaseModel):
    signal_type: str = Field(default="sine", description="Type of signal to emit")
    frequency: float = Field(default=440.0, description="Frequency in Hz")
    duration: float = Field(default=2.0, description="Duration in seconds")
    amplitude: float = Field(default=0.5, description="Amplitude (0.0-1.0)")

class FeedbackRequest(BaseModel):
    scan_id: int = Field(..., description="ID of the scan to provide feedback for")
    feedback_type: str = Field(..., description="Type of feedback")
    feedback_data: Dict[str, Any] = Field(..., description="Feedback content")

class SystemStatus(BaseModel):
    system_running: bool
    components: Dict[str, Dict[str, Any]]
    scan_count: int
    last_scan: Optional[str]

class ScanResult(BaseModel):
    timestamp: str
    scan_id: int
    interpretation: Dict[str, Any]
    features: Dict[str, Any]
    confidence: float

# Dependency to get system controller
async def get_system_controller():
    global system_controller, config
    if system_controller is None:
        config = Config()
        system_controller = ScribeSystemController(config)
        await system_controller.start()
    return system_controller

@app.on_event("startup")
async def startup_event():
    """Initialize the system on API startup"""
    global system_controller, config
    try:
        logger.info("🚀 Starting SCRIBE API Server...")
        config = Config()
        system_controller = ScribeSystemController(config)
        await system_controller.start()
        logger.info("✅ SCRIBE API Server started successfully")
    except Exception as e:
        logger.error(f"❌ Failed to start API server: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on API shutdown"""
    global system_controller
    if system_controller:
        await system_controller.stop()
        logger.info("🛑 SCRIBE API Server stopped")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SCRIBE Resonance AI API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "scribe-api"
    }

@app.get("/status", response_model=SystemStatus)
async def get_system_status(system: ScribeSystemController = Depends(get_system_controller)):
    """Get comprehensive system status"""
    try:
        status = await system.get_system_status()
        return SystemStatus(**status)
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan", response_model=ScanResult)
async def perform_scan(
    scan_request: ScanRequest,
    background_tasks: BackgroundTasks,
    system: ScribeSystemController = Depends(get_system_controller)
):
    """Perform a resonance scan"""
    try:
        logger.info(f"🔊 API scan request: {scan_request.signal_type} at {scan_request.frequency}Hz")
        
        # Convert request to scan config
        scan_config = {
            'signal_type': scan_request.signal_type,
            'frequency': scan_request.frequency,
            'duration': scan_request.duration,
            'amplitude': scan_request.amplitude
        }
        
        # Perform scan
        result = await system.perform_resonance_scan(scan_config)
        
        # Store scan result in background
        background_tasks.add_task(
            system.feedback_loop.store_scan_result,
            result
        )
        
        # Extract key information for response
        interpretation = result.get('interpretation', {})
        confidence_scores = interpretation.get('confidence_scores', {})
        overall_confidence = confidence_scores.get('overall', 0.0)
        
        return ScanResult(
            timestamp=result['timestamp'],
            scan_id=len(system.scan_history),  # Use scan count as ID
            interpretation=interpretation,
            features=result['features'],
            confidence=overall_confidence
        )
        
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scans")
async def get_scan_history(
    limit: int = 10,
    system: ScribeSystemController = Depends(get_system_controller)
):
    """Get scan history"""
    try:
        history = system.get_scan_history(limit)
        return {
            "scans": history,
            "total_count": len(system.scan_history),
            "limit": limit
        }
    except Exception as e:
        logger.error(f"History retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scans/{scan_id}")
async def get_scan_details(
    scan_id: int,
    system: ScribeSystemController = Depends(get_system_controller)
):
    """Get detailed scan information"""
    try:
        history = system.get_scan_history(scan_id + 1)  # Get enough scans to include the requested one
        
        if scan_id >= len(history):
            raise HTTPException(status_code=404, detail="Scan not found")
        
        scan = history[scan_id]
        return scan
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scan details retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def add_feedback(
    feedback: FeedbackRequest,
    system: ScribeSystemController = Depends(get_system_controller)
):
    """Add user feedback for learning"""
    try:
        await system.feedback_loop.add_user_feedback(
            scan_id=feedback.scan_id,
            feedback_type=feedback.feedback_type,
            feedback_data=feedback.feedback_data
        )
        
        return {
            "message": "Feedback added successfully",
            "scan_id": feedback.scan_id,
            "feedback_type": feedback.feedback_type
        }
        
    except Exception as e:
        logger.error(f"Feedback addition failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/insights")
async def get_learning_insights(system: ScribeSystemController = Depends(get_system_controller)):
    """Get learning insights and statistics"""
    try:
        insights = await system.feedback_loop.get_learning_insights()
        return insights
    except Exception as e:
        logger.error(f"Learning insights retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/patterns")
async def get_adapted_patterns(system: ScribeSystemController = Depends(get_system_controller)):
    """Get adapted patterns from learning"""
    try:
        patterns = await system.feedback_loop.get_adapted_patterns()
        return patterns
    except Exception as e:
        logger.error(f"Pattern retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare")
async def compare_scans(
    scan_ids: List[int],
    system: ScribeSystemController = Depends(get_system_controller)
):
    """Compare multiple scans"""
    try:
        if len(scan_ids) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 scans to compare")
        
        # Get scan data
        history = system.get_scan_history(max(scan_ids) + 1)
        
        if max(scan_ids) >= len(history):
            raise HTTPException(status_code=404, detail="One or more scans not found")
        
        scans_to_compare = [history[i] for i in scan_ids]
        
        # Perform comparison analysis
        comparison = await _perform_scan_comparison(scans_to_compare)
        
        return {
            "scan_ids": scan_ids,
            "comparison": comparison,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scan comparison failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def _perform_scan_comparison(scans: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Perform detailed comparison between scans"""
    if len(scans) < 2:
        return {}
    
    comparison = {
        "scan_count": len(scans),
        "time_span": {
            "start": scans[0].get('timestamp'),
            "end": scans[-1].get('timestamp')
        },
        "feature_changes": {},
        "interpretation_changes": {}
    }
    
    # Compare features
    for i, scan in enumerate(scans[1:], 1):
        prev_scan = scans[i-1]
        current_features = scan.get('features', {})
        prev_features = prev_scan.get('features', {})
        
        # Frequency changes
        current_freq = current_features.get('frequency_domain', {}).get('dominant_frequency', 0)
        prev_freq = prev_features.get('frequency_domain', {}).get('dominant_frequency', 0)
        
        if current_freq > 0 and prev_freq > 0:
            freq_change = abs(current_freq - prev_freq)
            freq_percent = (freq_change / prev_freq) * 100
            comparison["feature_changes"][f"scan_{i-1}_to_{i}"] = {
                "frequency_change_hz": freq_change,
                "frequency_change_percent": freq_percent
            }
    
    return comparison

@app.get("/metrics")
async def get_system_metrics(system: ScribeSystemController = Depends(get_system_controller)):
    """Get system performance metrics"""
    try:
        # Get basic metrics
        status = await system.get_system_status()
        
        metrics = {
            "system_metrics": {
                "total_scans": status["scan_count"],
                "system_running": status["system_running"],
                "components_count": len(status["components"])
            },
            "performance_metrics": {
                "api_response_time": "measured_at_gateway",
                "scan_processing_time": "measured_per_scan",
                "system_uptime": "since_startup"
            },
            "learning_metrics": await system.feedback_loop.get_learning_insights()
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reset")
async def reset_system(system: ScribeSystemController = Depends(get_system_controller)):
    """Reset system (clear history and learning data)"""
    try:
        # Clear scan history
        system.scan_history.clear()
        system.current_scan_data = None
        
        # Note: In a production system, you might want to be more careful
        # about resetting learning data. This is a full reset.
        
        return {
            "message": "System reset successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"System reset failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
