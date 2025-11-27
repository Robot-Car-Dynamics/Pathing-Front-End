#!/usr/bin/env python3
"""
Test script to simulate robot pose API responses.
This creates a mock HTTP server that responds to /api/pose requests
with test JSON data to demo the pose display functionality.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import math

class MockRobotAPIHandler(BaseHTTPRequestHandler):
    """Handler for mock robot API requests"""
    
    # Simulated robot state
    current_x = 0.0
    current_y = 0.0
    time_offset = 0
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/pose':
            self.send_pose_response()
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests (for command sending)"""
        if self.path.startswith('/api/'):
            # Read the command data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            command = json.loads(post_data.decode('utf-8'))
            
            print(f"\n📨 Received command: {command}")
            
            # Simulate command execution
            if command.get('cmd') == 'move':
                distance = float(command.get('d', 0))
                direction = int(command.get('dir', 1))
                self.current_x += distance * direction
                print(f"   ✓ Moving {distance}m {'forward' if direction == 1 else 'backward'}")
                print(f"   New position: ({self.current_x:.2f}, {self.current_y:.2f})")
            
            elif command.get('cmd') == 'turn':
                angle = float(command.get('a', 0))
                print(f"   ✓ Turning to {angle}°")
            
            # Send success response
            response = {
                "H": command.get('id', 'unknown'),
                "status": "success"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Endpoint not found")
    
    def send_pose_response(self):
        """Send a simulated pose response"""
        # Simulate some movement over time for demo purposes
        elapsed = time.time() - MockRobotAPIHandler.time_offset
        
        # Create a circular pattern for demo
        MockRobotAPIHandler.current_x = 2 * math.cos(elapsed * 0.3)
        MockRobotAPIHandler.current_y = 2 * math.sin(elapsed * 0.3)
        
        # Format: {"H":"command_id", "pose":{"x":value, "y":value}}
        response_data = {
            "H": f"pose_{int(elapsed)}",
            "pose": {
                "x": round(MockRobotAPIHandler.current_x, 2),
                "y": round(MockRobotAPIHandler.current_y, 2)
            }
        }
        
        print(f"📍 Sending pose: X={response_data['pose']['x']:.2f}, Y={response_data['pose']['y']:.2f}")
        
        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())
    
    def log_message(self, format, *args):
        """Override to reduce noise in output"""
        pass  # Suppress default logging


def run_test_server(port=8080):
    """Run the mock API server"""
    MockRobotAPIHandler.time_offset = time.time()
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockRobotAPIHandler)
    
    print("=" * 60)
    print("🤖 Mock Robot API Server")
    print("=" * 60)
    print(f"\n✅ Server running on http://localhost:{port}")
    print(f"📍 Pose endpoint: http://localhost:{port}/api/pose")
    print(f"📨 Command endpoint: http://localhost:{port}/api/command")
    print("\n💡 Usage:")
    print("   1. Run this script in one terminal")
    print("   2. In PathPlanner.py, set: api_address = 'http://localhost:8080/api/command'")
    print("   3. Run your GUI application")
    print("   4. Click 'Update Pose' to see simulated position")
    print("   5. Send commands to see them logged here")
    print("\n📊 Pose data simulates circular movement pattern")
    print("   (Updates every time you click 'Update Pose')")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    print("-" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...")
        httpd.shutdown()
        print("✅ Server stopped\n")


if __name__ == "__main__":
    import sys
    
    # Allow custom port as argument
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}, using default 8080")
    
    run_test_server(port)
