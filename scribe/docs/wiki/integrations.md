# SCRIBE Integration Examples and Patterns

## Integration Overview

This guide provides comprehensive integration examples and patterns for connecting the SCRIBE Resonance AI System with external systems, APIs, and services. Learn how to build robust integrations for various use cases.

## Integration Architecture

### Integration Patterns
```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                        │
├─────────────────────────────────────────────────────────────┤
│                    Integration Layer                          │
├─────────────────────────────────────────────────────────────┤
│                    SCRIBE API Layer                           │
├─────────────────────────────────────────────────────────────┤
│                    SCRIBE Core System                         │
└─────────────────────────────────────────────────────────────┘
```

### Integration Types
- **Direct API Integration**: REST API calls
- **WebSocket Integration**: Real-time communication
- **Message Queue Integration**: Asynchronous processing
- **Database Integration**: Direct data access
- **Cloud Service Integration**: External platform connections

## Direct API Integration

### Python Client Library
```python
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ScanConfig:
    signal_type: str = "sine"
    frequency: float = 440.0
    duration: float = 2.0
    amplitude: float = 0.5

class ScribeClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})
    
    def health_check(self) -> bool:
        """Check if SCRIBE API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def perform_scan(self, config: ScanConfig) -> Dict:
        """Perform a resonance scan"""
        payload = {
            "signal_type": config.signal_type,
            "frequency": config.frequency,
            "duration": config.duration,
            "amplitude": config.amplitude
        }
        
        response = self.session.post(f"{self.base_url}/scan", json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_scan_history(self, limit: int = 10) -> List[Dict]:
        """Get scan history"""
        response = self.session.get(f"{self.base_url}/scans", params={"limit": limit})
        response.raise_for_status()
        
        return response.json().get("scans", [])
    
    def get_scan_details(self, scan_id: int) -> Dict:
        """Get detailed scan information"""
        response = self.session.get(f"{self.base_url}/scans/{scan_id}")
        response.raise_for_status()
        
        return response.json()
    
    def add_feedback(self, scan_id: int, feedback_type: str, feedback_data: Dict) -> Dict:
        """Add feedback to scan"""
        payload = {
            "scan_id": scan_id,
            "feedback_type": feedback_type,
            "feedback_data": feedback_data
        }
        
        response = self.session.post(f"{self.base_url}/feedback", json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def compare_scans(self, scan_ids: List[int]) -> Dict:
        """Compare multiple scans"""
        response = self.session.post(f"{self.base_url}/compare", json=scan_ids)
        response.raise_for_status()
        
        return response.json()

# Usage Example
def main():
    client = ScribeClient(api_key="your-api-key")
    
    if not client.health_check():
        print("SCRIBE API is not available")
        return
    
    # Perform scan
    config = ScanConfig(frequency=440, duration=2.0)
    result = client.perform_scan(config)
    
    print(f"Scan completed with {result['interpretation']['confidence_scores']['overall']:.1%} confidence")
    print(f"Material detected: {result['interpretation'].get('pattern_matches', {}).get('materials', [{}])[0].get('material', 'Unknown')}")
    
    # Add feedback
    client.add_feedback(result['scan_id'], "material_correction", {"correct_material": "oak"})

if __name__ == "__main__":
    main()
```

### Async Python Client
```python
import aiohttp
import asyncio
from typing import Dict, List, Optional

class AsyncScribeClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {}
        
        if api_key:
            self.headers["X-API-Key"] = api_key
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def health_check(self) -> bool:
        """Check if SCRIBE API is healthy"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                return response.status == 200
        except aiohttp.ClientError:
            return False
    
    async def perform_scan(self, config: ScanConfig) -> Dict:
        """Perform a resonance scan"""
        payload = {
            "signal_type": config.signal_type,
            "frequency": config.frequency,
            "duration": config.duration,
            "amplitude": config.amplitude
        }
        
        async with self.session.post(f"{self.base_url}/scan", json=payload) as response:
            response.raise_for_status()
            return await response.json()
    
    async def batch_scans(self, configs: List[ScanConfig]) -> List[Dict]:
        """Perform multiple scans concurrently"""
        tasks = [self.perform_scan(config) for config in configs]
        results = await asyncio.gather(*tasks)
        return results

# Usage Example
async def main():
    async with AsyncScribeClient(api_key="your-api-key") as client:
        if not await client.health_check():
            print("SCRIBE API is not available")
            return
        
        # Perform multiple scans
        configs = [
            ScanConfig(frequency=220, duration=2.0),
            ScanConfig(frequency=440, duration=2.0),
            ScanConfig(frequency=880, duration=2.0)
        ]
        
        results = await client.batch_scans(configs)
        
        for i, result in enumerate(results):
            confidence = result['interpretation']['confidence_scores']['overall']
            print(f"Scan {i+1}: {confidence:.1%} confidence")

if __name__ == "__main__":
    asyncio.run(main())
```

## WebSocket Integration

### Real-time Monitoring
```python
import asyncio
import websockets
import json
from typing import Dict, Any

class ScribeWebSocketClient:
    def __init__(self, ws_url: str = "ws://localhost:8000/ws"):
        self.ws_url = ws_url
        self.websocket = None
    
    async def connect(self):
        """Connect to WebSocket"""
        self.websocket = await websockets.connect(self.ws_url)
        print("Connected to SCRIBE WebSocket")
    
    async def subscribe_to_scans(self):
        """Subscribe to real-time scan updates"""
        if not self.websocket:
            await self.connect()
        
        subscribe_message = {
            "type": "subscribe",
            "channel": "scans"
        }
        
        await self.websocket.send(json.dumps(subscribe_message))
        print("Subscribed to scan updates")
    
    async def listen_for_updates(self):
        """Listen for real-time updates"""
        if not self.websocket:
            await self.connect()
        
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
    
    async def handle_message(self, data: Dict[str, Any]):
        """Handle incoming WebSocket messages"""
        message_type = data.get("type")
        
        if message_type == "scan_completed":
            await self.handle_scan_completed(data)
        elif message_type == "system_status":
            await self.handle_system_status(data)
        elif message_type == "alert":
            await self.handle_alert(data)
    
    async def handle_scan_completed(self, data: Dict[str, Any]):
        """Handle scan completion notification"""
        scan_id = data.get("scan_id")
        confidence = data.get("confidence")
        material = data.get("material")
        
        print(f"Scan {scan_id} completed:")
        print(f"  Confidence: {confidence:.1%}")
        print(f"  Material: {material}")
    
    async def handle_system_status(self, data: Dict[str, Any]):
        """Handle system status update"""
        status = data.get("status")
        load = data.get("load")
        
        print(f"System status: {status}, Load: {load:.1%}")
    
    async def handle_alert(self, data: Dict[str, Any]):
        """Handle system alert"""
        alert_type = data.get("type")
        message = data.get("message")
        
        print(f"ALERT [{alert_type}]: {message}")

# Usage Example
async def main():
    client = ScribeWebSocketClient()
    
    try:
        await client.connect()
        await client.subscribe_to_scans()
        await client.listen_for_updates()
    except KeyboardInterrupt:
        print("Disconnecting...")
        if client.websocket:
            await client.websocket.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 📨 Message Queue Integration

### Redis Queue Integration
```python
import redis
import json
import asyncio
from typing import Dict, Any, Optional

class ScribeRedisIntegration:
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.scan_queue = "scribe:scan_requests"
        self.result_queue = "scribe:scan_results"
        self.status_queue = "scribe:system_status"
    
    def enqueue_scan_request(self, config: ScanConfig, request_id: str) -> str:
        """Enqueue a scan request"""
        message = {
            "request_id": request_id,
            "config": {
                "signal_type": config.signal_type,
                "frequency": config.frequency,
                "duration": config.duration,
                "amplitude": config.amplitude
            },
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Push to queue
        self.redis_client.lpush(self.scan_queue, json.dumps(message))
        
        return request_id
    
    def dequeue_scan_request(self) -> Optional[Dict[str, Any]]:
        """Dequeue a scan request"""
        message = self.redis_client.brpop(self.scan_queue, timeout=1)
        
        if message:
            return json.loads(message[1])
        
        return None
    
    def publish_scan_result(self, request_id: str, result: Dict[str, Any]):
        """Publish scan result"""
        message = {
            "request_id": request_id,
            "result": result,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.redis_client.lpush(self.result_queue, json.dumps(message))
    
    def get_scan_result(self, request_id: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """Get scan result by request ID"""
        end_time = asyncio.get_event_loop().time() + timeout
        
        while asyncio.get_event_loop().time() < end_time:
            # Check result queue
            messages = self.redis_client.lrange(self.result_queue, 0, -1)
            
            for msg in messages:
                data = json.loads(msg)
                if data.get("request_id") == request_id:
                    # Remove from queue
                    self.redis_client.lrem(self.result_queue, 1, msg)
                    return data.get("result")
            
            asyncio.sleep(0.1)
        
        return None
    
    def publish_system_status(self, status: Dict[str, Any]):
        """Publish system status"""
        self.redis_client.publish(self.status_queue, json.dumps(status))
    
    def subscribe_to_status(self, callback):
        """Subscribe to system status updates"""
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(self.status_queue)
        
        for message in pubsub.listen():
            if message["type"] == "message":
                status_data = json.loads(message["data"])
                callback(status_data)

# Usage Example
def status_callback(status_data):
    """Handle status updates"""
    status = status_data.get("status")
    load = status_data.get("load")
    print(f"Status update: {status}, Load: {load:.1%}")

def main():
    integration = ScribeRedisIntegration()
    
    # Subscribe to status updates
    import threading
    status_thread = threading.Thread(
        target=integration.subscribe_to_status,
        args=(status_callback,)
    )
    status_thread.daemon = True
    status_thread.start()
    
    # Enqueue scan request
    config = ScanConfig(frequency=440, duration=2.0)
    request_id = "scan-001"
    
    integration.enqueue_scan_request(config, request_id)
    print(f"Enqueued scan request: {request_id}")
    
    # Wait for result
    result = integration.get_scan_result(request_id, timeout=30)
    
    if result:
        confidence = result['interpretation']['confidence_scores']['overall']
        print(f"Scan completed: {confidence:.1%} confidence")
    else:
        print("Scan timed out")

if __name__ == "__main__":
    main()
```

### RabbitMQ Integration
```python
import pika
import json
import asyncio
from typing import Dict, Any, Callable

class ScribeRabbitMQIntegration:
    def __init__(self, host: str = "localhost"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        
        # Declare queues
        self.channel.queue_declare(queue="scribe.scan.requests", durable=True)
        self.channel.queue_declare(queue="scribe.scan.results", durable=True)
        self.channel.queue_declare(queue="scribe.system.status", durable=True)
        
        # Declare exchange for fanout
        self.channel.exchange_declare(exchange="scribe.events", exchange_type="fanout")
    
    def publish_scan_request(self, config: ScanConfig, request_id: str):
        """Publish scan request"""
        message = {
            "request_id": request_id,
            "config": {
                "signal_type": config.signal_type,
                "frequency": config.frequency,
                "duration": config.duration,
                "amplitude": config.amplitude
            },
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.channel.basic_publish(
            exchange="",
            routing_key="scribe.scan.requests",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistent
        )
    
    def consume_scan_requests(self, callback: Callable):
        """Consume scan requests"""
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(
            queue="scribe.scan.requests",
            on_message_callback=wrapper
        )
        
        print("Waiting for scan requests...")
        self.channel.start_consuming()
    
    def publish_scan_result(self, request_id: str, result: Dict[str, Any]):
        """Publish scan result"""
        message = {
            "request_id": request_id,
            "result": result,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.channel.basic_publish(
            exchange="",
            routing_key="scribe.scan.results",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    
    def publish_system_event(self, event_type: str, data: Dict[str, Any]):
        """Publish system event"""
        message = {
            "event_type": event_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.channel.basic_publish(
            exchange="scribe.events",
            routing_key="",
            body=json.dumps(message)
        )
    
    def close(self):
        """Close connection"""
        self.connection.close()

# Usage Example
def handle_scan_request(message):
    """Handle incoming scan request"""
    request_id = message.get("request_id")
    config_data = message.get("config")
    
    print(f"Processing scan request: {request_id}")
    
    # Process scan (implementation would call SCRIBE API)
    # result = process_scan(config_data)
    
    # For demo, create mock result
    result = {
        "scan_id": 123,
        "interpretation": {
            "confidence_scores": {"overall": 0.85},
            "insights": ["Mock scan completed"]
        }
    }
    
    # Publish result
    integration.publish_scan_result(request_id, result)

def main():
    global integration
    integration = ScribeRabbitMQIntegration()
    
    try:
        # Publish scan request
        config = ScanConfig(frequency=440, duration=2.0)
        integration.publish_scan_request(config, "req-001")
        
        # Consume requests (in production, this would run in a separate process)
        # integration.consume_scan_requests(handle_scan_request)
        
        # Publish system event
        integration.publish_system_event("system_started", {"version": "1.0.0"})
        
    finally:
        integration.close()

if __name__ == "__main__":
    main()
```

## 🗄️ Database Integration

### Direct Database Access
```python
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import contextmanager

class ScribeDatabaseIntegration:
    def __init__(self, db_path: str = "scribe_learning.db"):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def get_scan_results(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get scan results directly from database"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, timestamp, signals, response, features, interpretation, config
                FROM scan_results
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            results = []
            for row in cursor.fetchall():
                result = {
                    "scan_id": row["id"],
                    "timestamp": row["timestamp"],
                    "signals": json.loads(row["signals"]),
                    "response": json.loads(row["response"]),
                    "features": json.loads(row["features"]),
                    "interpretation": json.loads(row["interpretation"]),
                    "config": json.loads(row["config"])
                }
                results.append(result)
            
            return results
    
    def get_scan_by_id(self, scan_id: int) -> Optional[Dict]:
        """Get specific scan by ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, timestamp, signals, response, features, interpretation, config
                FROM scan_results
                WHERE id = ?
            """, (scan_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "scan_id": row["id"],
                    "timestamp": row["timestamp"],
                    "signals": json.loads(row["signals"]),
                    "response": json.loads(row["response"]),
                    "features": json.loads(row["features"]),
                    "interpretation": json.loads(row["interpretation"]),
                    "config": json.loads(row["config"])
                }
            
            return None
    
    def get_learning_insights(self) -> Dict:
        """Get learning insights from database"""
        with self.get_connection() as conn:
            # Get total scans
            cursor = conn.execute("SELECT COUNT(*) as count FROM scan_results")
            total_scans = cursor.fetchone()["count"]
            
            # Get feedback count
            cursor = conn.execute("SELECT COUNT(*) as count FROM user_feedback")
            total_feedback = cursor.fetchone()["count"]
            
            # Get pattern adaptations
            cursor = conn.execute("SELECT COUNT(*) as count FROM pattern_adaptations")
            total_adaptations = cursor.fetchone()["count"]
            
            # Get recent performance
            cursor = conn.execute("""
                SELECT AVG(
                    json_extract(interpretation, '$.confidence_scores.overall')
                ) as avg_confidence
                FROM scan_results
                WHERE timestamp > datetime('now', '-24 hours')
            """)
            recent_confidence = cursor.fetchone()["avg_confidence"] or 0
            
            return {
                "total_scans": total_scans,
                "total_feedback": total_feedback,
                "total_adaptations": total_adaptations,
                "recent_confidence": recent_confidence
            }
    
    def add_external_scan_data(self, scan_data: Dict) -> int:
        """Add external scan data to database"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO scan_results 
                (timestamp, signals, response, features, interpretation, config)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                json.dumps(scan_data["signals"]),
                json.dumps(scan_data["response"]),
                json.dumps(scan_data["features"]),
                json.dumps(scan_data["interpretation"]),
                json.dumps(scan_data["config"])
            ))
            
            scan_id = cursor.lastrowid
            conn.commit()
            
            return scan_id

# Usage Example
def main():
    db_integration = ScribeDatabaseIntegration()
    
    # Get recent scans
    recent_scans = db_integration.get_scan_results(limit=10)
    print(f"Found {len(recent_scans)} recent scans")
    
    # Get learning insights
    insights = db_integration.get_learning_insights()
    print(f"Learning insights: {insights}")
    
    # Add external scan data
    external_scan = {
        "signals": [{"type": "sine", "frequency": 440}],
        "response": {"audio_data": [0.1, 0.2, 0.3]},
        "features": {"time_domain": {"rms": 0.2}},
        "interpretation": {"confidence_scores": {"overall": 0.8}},
        "config": {"signal_type": "sine"}
    }
    
    scan_id = db_integration.add_external_scan_data(external_scan)
    print(f"Added external scan with ID: {scan_id}")

if __name__ == "__main__":
    main()
```

## ☁️ Cloud Service Integration

### AWS Integration
```python
import boto3
import json
import asyncio
from typing import Dict, Any

class ScribeAWSIntegration:
    def __init__(self, region: str = "us-west-2"):
        self.region = region
        self.s3_client = boto3.client("s3", region_name=region)
        self.lambda_client = boto3.client("lambda", region_name=region)
        self.sqs_client = boto3.client("sqs", region_name=region)
        self.dynamodb_client = boto3.resource("dynamodb", region_name=region)
    
    def upload_scan_to_s3(self, scan_data: Dict, bucket: str, key: str):
        """Upload scan data to S3"""
        scan_json = json.dumps(scan_data)
        
        self.s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=scan_json,
            ContentType="application/json"
        )
        
        print(f"Uploaded scan to S3: s3://{bucket}/{key}")
    
    def invoke_scribe_lambda(self, scan_config: ScanConfig) -> Dict:
        """Invoke SCRIBE Lambda function"""
        payload = {
            "signal_type": scan_config.signal_type,
            "frequency": scan_config.frequency,
            "duration": scan_config.duration,
            "amplitude": scan_config.amplitude
        }
        
        response = self.lambda_client.invoke(
            FunctionName="scribe-scan-function",
            InvocationType="RequestResponse",
            Payload=json.dumps(payload)
        )
        
        result = json.loads(response["Payload"].read())
        return result
    
    def send_scan_request_to_sqs(self, scan_config: ScanConfig, queue_url: str):
        """Send scan request to SQS queue"""
        message = {
            "config": {
                "signal_type": scan_config.signal_type,
                "frequency": scan_config.frequency,
                "duration": scan_config.duration,
                "amplitude": scan_config.amplitude
            },
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
    
    def store_scan_in_dynamodb(self, scan_data: Dict, table_name: str):
        """Store scan data in DynamoDB"""
        table = self.dynamodb_client.Table(table_name)
        
        item = {
            "scan_id": scan_data["scan_id"],
            "timestamp": scan_data["timestamp"],
            "confidence": scan_data["interpretation"]["confidence_scores"]["overall"],
            "material": scan_data["interpretation"].get("pattern_matches", {}).get("materials", [{}])[0].get("material", "unknown"),
            "features": scan_data["features"],
            "interpretation": scan_data["interpretation"]
        }
        
        table.put_item(Item=item)
        print(f"Stored scan {scan_data['scan_id']} in DynamoDB")

# Usage Example
def main():
    aws_integration = ScribeAWSIntegration()
    
    # Upload scan to S3
    scan_data = {
        "scan_id": 123,
        "timestamp": "2026-05-06T19:00:00Z",
        "interpretation": {"confidence_scores": {"overall": 0.85}}
    }
    
    aws_integration.upload_scan_to_s3(
        scan_data, 
        "scribe-scans", 
        f"scans/2026/05/06/scan-{scan_data['scan_id']}.json"
    )
    
    # Invoke Lambda function
    config = ScanConfig(frequency=440, duration=2.0)
    result = aws_integration.invoke_scribe_lambda(config)
    print(f"Lambda result: {result}")

if __name__ == "__main__":
    main()
```

### Google Cloud Integration
```python
from google.cloud import storage
from google.cloud import pubsub_v1
from google.cloud import bigquery
import json
import asyncio

class ScribeGCPIntegration:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.storage_client = storage.Client(project=project_id)
        self.publisher = pubsub_v1.PublisherClient()
        self.bigquery_client = bigquery.Client(project=project_id)
    
    def upload_scan_to_gcs(self, scan_data: Dict, bucket_name: str, blob_name: str):
        """Upload scan data to Google Cloud Storage"""
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        scan_json = json.dumps(scan_data)
        blob.upload_from_string(scan_json, content_type="application/json")
        
        print(f"Uploaded scan to GCS: gs://{bucket_name}/{blob_name}")
    
    def publish_scan_request(self, scan_config: ScanConfig, topic_name: str):
        """Publish scan request to Pub/Sub"""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        
        message = {
            "config": {
                "signal_type": scan_config.signal_type,
                "frequency": scan_config.frequency,
                "duration": scan_config.duration,
                "amplitude": scan_config.amplitude
            },
            "timestamp": asyncio.get_event_loop().time()
        }
        
        data = json.dumps(message).encode("utf-8")
        future = self.publisher.publish(topic_path, data)
        
        print(f"Published scan request: {future.result()}")
    
    def store_scan_in_bigquery(self, scan_data: Dict, dataset_id: str, table_id: str):
        """Store scan data in BigQuery"""
        table_ref = self.bigquery_client.dataset(dataset_id).table(table_id)
        
        rows_to_insert = [
            {
                "scan_id": scan_data["scan_id"],
                "timestamp": scan_data["timestamp"],
                "confidence": scan_data["interpretation"]["confidence_scores"]["overall"],
                "material": scan_data["interpretation"].get("pattern_matches", {}).get("materials", [{}])[0].get("material", "unknown"),
                "features_json": json.dumps(scan_data["features"]),
                "interpretation_json": json.dumps(scan_data["interpretation"])
            }
        ]
        
        errors = self.bigquery_client.insert_rows_json(table_ref, rows_to_insert)
        
        if errors:
            print(f"BigQuery insert errors: {errors}")
        else:
            print(f"Stored scan {scan_data['scan_id']} in BigQuery")

# Usage Example
def main():
    gcp_integration = ScribeGCPIntegration("your-project-id")
    
    # Upload to GCS
    scan_data = {
        "scan_id": 123,
        "timestamp": "2026-05-06T19:00:00Z",
        "interpretation": {"confidence_scores": {"overall": 0.85}}
    }
    
    gcp_integration.upload_scan_to_gcs(
        scan_data,
        "scribe-scans",
        f"scans/2026/05/06/scan-{scan_data['scan_id']}.json"
    )
    
    # Publish to Pub/Sub
    config = ScanConfig(frequency=440, duration=2.0)
    gcp_integration.publish_scan_request(config, "scan-requests")

if __name__ == "__main__":
    main()
```

## Integration Patterns

### Circuit Breaker Pattern
```python
import time
from typing import Callable, Any
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            
            return result
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            
            raise e

# Usage Example
def resilient_scribe_call(client: ScribeClient, config: ScanConfig):
    """Make resilient SCRIBE API call"""
    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=30)
    
    try:
        result = circuit_breaker.call(client.perform_scan, config)
        return result
    except Exception as e:
        print(f"SCRIBE call failed: {e}")
        return None
```

### Retry Pattern
```python
import time
import random
from typing import Callable, Any

class RetryPolicy:
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_attempts - 1:
                    delay = min(self.base_delay * (2 ** attempt) + random.uniform(0, 1), self.max_delay)
                    time.sleep(delay)
        
        raise last_exception

# Usage Example
def retry_scribe_call(client: ScribeClient, config: ScanConfig):
    """Make SCRIBE API call with retry"""
    retry_policy = RetryPolicy(max_attempts=3, base_delay=1.0)
    
    try:
        result = retry_policy.execute(client.perform_scan, config)
        return result
    except Exception as e:
        print(f"SCRIBE call failed after retries: {e}")
        return None
```

### Cache-Aside Pattern
```python
import time
from typing import Dict, Any, Optional

class CacheAside:
    def __init__(self, ttl: int = 300):  # 5 minutes TTL
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            
            if time.time() - entry["timestamp"] < self.ttl:
                return entry["value"]
            else:
                del self.cache[key]
        
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        self.cache[key] = {
            "value": value,
            "timestamp": time.time()
        }
    
    def invalidate(self, key: str):
        """Invalidate cache entry"""
        if key in self.cache:
            del self.cache[key]

# Usage Example
def cached_scribe_call(client: ScribeClient, config: ScanConfig):
    """Make cached SCRIBE API call"""
    cache = CacheAside(ttl=300)  # 5 minutes
    cache_key = f"scan_{config.frequency}_{config.duration}"
    
    # Try cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        print("Returning cached result")
        return cached_result
    
    # Make API call
    result = client.perform_scan(config)
    
    # Cache result
    cache.set(cache_key, result)
    
    return result
```

## Integration Monitoring

### Integration Health Check
```python
import asyncio
from typing import Dict, List

class IntegrationHealthMonitor:
    def __init__(self):
        self.integrations = {}
        self.health_status = {}
    
    def register_integration(self, name: str, health_check_func: Callable):
        """Register integration with health check function"""
        self.integrations[name] = health_check_func
    
    async def check_all_health(self) -> Dict[str, bool]:
        """Check health of all integrations"""
        results = {}
        
        for name, health_check in self.integrations.items():
            try:
                is_healthy = await health_check()
                results[name] = is_healthy
            except Exception as e:
                results[name] = False
                print(f"Health check failed for {name}: {e}")
        
        self.health_status = results
        return results
    
    async def monitor_continuously(self, interval: int = 60):
        """Monitor integrations continuously"""
        while True:
            await self.check_all_health()
            await asyncio.sleep(interval)
    
    def get_unhealthy_integrations(self) -> List[str]:
        """Get list of unhealthy integrations"""
        return [name for name, healthy in self.health_status.items() if not healthy]

# Usage Example
async def scribe_health_check():
    """Health check for SCRIBE API"""
    client = ScribeClient()
    return client.health_check()

async def redis_health_check():
    """Health check for Redis"""
    try:
        redis_client = redis.Redis()
        redis_client.ping()
        return True
    except:
        return False

def main():
    monitor = IntegrationHealthMonitor()
    
    # Register integrations
    monitor.register_integration("scribe", scribe_health_check)
    monitor.register_integration("redis", redis_health_check)
    
    # Check health
    asyncio.run(monitor.check_all_health())
    
    # Get unhealthy integrations
    unhealthy = monitor.get_unhealthy_integrations()
    if unhealthy:
        print(f"Unhealthy integrations: {unhealthy}")

if __name__ == "__main__":
    main()
```

## Best Practices

### Error Handling
- Implement proper error handling for all integrations
- Use circuit breakers to prevent cascading failures
- Implement retry logic with exponential backoff
- Log all integration errors for debugging

### Performance Optimization
- Use connection pooling for database connections
- Implement caching for frequently accessed data
- Use async/await for I/O operations
- Monitor integration performance metrics

### Security
- Secure all API keys and credentials
- Use HTTPS for all external communications
- Implement proper authentication and authorization
- Validate all external data

### Monitoring
- Monitor integration health and performance
- Set up alerts for integration failures
- Track integration usage and costs
- Implement proper logging and auditing

---

**Last Updated**: 2026-05-06  
**Integration Guide Version**: 1.0.0  
**Status**: Production Ready
