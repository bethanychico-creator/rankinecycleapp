#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
from rankine_calculator import calculate_rankine_cycle

class RankineHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse URL and query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/calculate':
            try:
                # Parse query parameters
                params = urllib.parse.parse_qs(parsed_path.query)
                
                # Extract inputs (converting from MPa to Pa for high pressures, keeping Pa for P6)
                P3 = float(params['P3'][0]) * 1e6  # MPa to Pa
                T3 = float(params['T3'][0]) + 273.15  # °C to K
                P4 = float(params['P4'][0]) * 1e6  # MPa to Pa
                T5 = float(params['T5'][0]) + 273.15  # °C to K
                P6 = float(params['P6'][0])  # Already in Pa
                
                # Calculate cycle
                result = calculate_rankine_cycle(P3, T3, P4, T5, P6)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        elif parsed_path.path == '/':
            # Simple health check endpoint
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'message': 'Rankine Calculator API'}).encode())
        
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
    
    def log_message(self, format, *args):
        # Log to stdout for Render logs
        print(f"{self.address_string()} - {format % args}")

if __name__ == '__main__':
    # Use PORT environment variable (Render provides this) or default to 8888
    PORT = int(os.environ.get('PORT', 8888))
    server = HTTPServer(('0.0.0.0', PORT), RankineHandler)
    print(f'Rankine Calculator Server running on port {PORT}')
    print(f'Health check: http://localhost:{PORT}/')
    print(f'Calculate endpoint: http://localhost:{PORT}/calculate?P3=10&T3=600&P4=5&T5=500&P6=100000')
    server.serve_forever()
