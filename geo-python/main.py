from socketserver import BaseRequestHandler, UDPServer
from prometheus_client import CollectorRegistry, Counter, push_to_gateway
import json
import os


ENDPOINT = os.environ['PUSHGATEWAY_ENDPOINT']
PUSHGATEWAY_URL = f'http://{ENDPOINT}'

registry = CollectorRegistry()
client_requests = Counter(
    'client_requests_total',
    'Number of requests by client IP and country',
    ['ip', 'country'],
    registry=registry
)
status_codes = Counter(
    'status_codes_total',
    'Number of requests by status code',
    ['status'],
    registry=registry
)

class SyslogUDPHandler(BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        try:
            json_start = data.find("{")
            if json_start != -1:
                log = json.loads(data[json_start:])
                ip = log.get("remote_addr")
                status = log.get("status")
                country = log.get("geoip_country_code")

                client_requests.labels(ip, country).inc()
                status_codes.labels(status).inc()
            else:
                print(f"Log does not contain JSON: {data}")
        except json.JSONDecodeError:
            print(f"Failed to parse log: {data}")
        except Exception as e:
            print(f"Error handling log: {e}")
        finally:
            push_metrics()

def push_metrics():
    push_to_gateway(PUSHGATEWAY_URL, job='nginx_logs', registry=registry)
    print('Send OK !')

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 514
    server = UDPServer((HOST, PORT), SyslogUDPHandler)
    print(f"Syslog server running on port {PORT}...")
    server.serve_forever()