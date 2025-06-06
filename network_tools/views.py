from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import subprocess
import socket
import ssl
import requests
import json
import time
import re
from datetime import datetime

@login_required
def dashboard(request):
    """Dashboard principal das ferramentas de rede"""
    return render(request, 'network_tools/dashboard.html')

@login_required
def ping(request):
    """Ferramenta de Ping"""
    result = None
    if request.method == 'POST':
        host = request.POST.get('host', '').strip()
        count = request.POST.get('count', '4')
        
        if host:
            try:
                # Executar ping
                cmd = ['ping', '-c', count, host]
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                result = {
                    'host': host,
                    'success': process.returncode == 0,
                    'output': process.stdout,
                    'error': process.stderr if process.returncode != 0 else None
                }
            except subprocess.TimeoutExpired:
                result = {
                    'host': host,
                    'success': False,
                    'error': 'Timeout: O comando demorou mais de 30 segundos'
                }
            except Exception as e:
                result = {
                    'host': host,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/ping.html', {'result': result})

@login_required
def traceroute(request):
    """Ferramenta de Traceroute"""
    result = None
    if request.method == 'POST':
        host = request.POST.get('host', '').strip()
        
        if host:
            try:
                # Executar traceroute
                cmd = ['traceroute', host]
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                result = {
                    'host': host,
                    'success': process.returncode == 0,
                    'output': process.stdout,
                    'error': process.stderr if process.returncode != 0 else None
                }
            except subprocess.TimeoutExpired:
                result = {
                    'host': host,
                    'success': False,
                    'error': 'Timeout: O comando demorou mais de 60 segundos'
                }
            except Exception as e:
                result = {
                    'host': host,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/traceroute.html', {'result': result})

@login_required
def port_scanner(request):
    """Ferramenta de Port Scanner"""
    result = None
    if request.method == 'POST':
        host = request.POST.get('host', '').strip()
        ports = request.POST.get('ports', '22,80,443,3389').strip()
        
        if host and ports:
            try:
                port_list = []
                for port_range in ports.split(','):
                    port_range = port_range.strip()
                    if '-' in port_range:
                        start, end = map(int, port_range.split('-'))
                        port_list.extend(range(start, end + 1))
                    else:
                        port_list.append(int(port_range))
                
                scan_results = []
                for port in port_list[:50]:  # Limitar a 50 portas
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(3)
                        result_code = sock.connect_ex((host, port))
                        sock.close()
                        
                        status = 'Aberta' if result_code == 0 else 'Fechada'
                        scan_results.append({'port': port, 'status': status})
                    except Exception:
                        scan_results.append({'port': port, 'status': 'Erro'})
                
                result = {
                    'host': host,
                    'success': True,
                    'ports': scan_results
                }
            except Exception as e:
                result = {
                    'host': host,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/port_scanner.html', {'result': result})

@login_required
def nmap(request):
    """Ferramenta de Nmap"""
    result = None
    if request.method == 'POST':
        host = request.POST.get('host', '').strip()
        scan_type = request.POST.get('scan_type', '-sS')
        
        if host:
            try:
                # Executar nmap
                cmd = ['nmap', scan_type, host]
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                result = {
                    'host': host,
                    'success': process.returncode == 0,
                    'output': process.stdout,
                    'error': process.stderr if process.returncode != 0 else None
                }
            except subprocess.TimeoutExpired:
                result = {
                    'host': host,
                    'success': False,
                    'error': 'Timeout: O comando demorou mais de 2 minutos'
                }
            except Exception as e:
                result = {
                    'host': host,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/nmap.html', {'result': result})

@login_required
def dns_lookup(request):
    """Ferramenta de DNS Lookup"""
    result = None
    if request.method == 'POST':
        domain = request.POST.get('domain', '').strip()
        record_type = request.POST.get('record_type', 'A')
        
        if domain:
            try:
                # Executar dig
                cmd = ['dig', '+short', record_type, domain]
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                result = {
                    'domain': domain,
                    'record_type': record_type,
                    'success': process.returncode == 0,
                    'output': process.stdout.strip(),
                    'error': process.stderr if process.returncode != 0 else None
                }
            except subprocess.TimeoutExpired:
                result = {
                    'domain': domain,
                    'success': False,
                    'error': 'Timeout: O comando demorou mais de 30 segundos'
                }
            except Exception as e:
                result = {
                    'domain': domain,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/dns_lookup.html', {'result': result})

@login_required
def http_headers(request):
    """Ferramenta de HTTP Headers"""
    result = None
    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        
        if url:
            try:
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                
                response = requests.head(url, timeout=30, allow_redirects=True)
                
                result = {
                    'url': url,
                    'success': True,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'final_url': response.url
                }
            except Exception as e:
                result = {
                    'url': url,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/http_headers.html', {'result': result})

@login_required
def ssl_check(request):
    """Ferramenta de SSL Certificate Check"""
    result = None
    if request.method == 'POST':
        hostname = request.POST.get('hostname', '').strip()
        port = int(request.POST.get('port', '443'))
        
        if hostname:
            try:
                context = ssl.create_default_context()
                with socket.create_connection((hostname, port), timeout=30) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        
                        result = {
                            'hostname': hostname,
                            'port': port,
                            'success': True,
                            'subject': dict(x[0] for x in cert['subject']),
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'version': cert['version'],
                            'serial_number': cert['serialNumber'],
                            'not_before': cert['notBefore'],
                            'not_after': cert['notAfter'],
                            'san': cert.get('subjectAltName', [])
                        }
            except Exception as e:
                result = {
                    'hostname': hostname,
                    'port': port,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/ssl_check.html', {'result': result})

@login_required
def geoip(request):
    """Ferramenta de Geolocalização IP"""
    result = None
    if request.method == 'POST':
        ip = request.POST.get('ip', '').strip()
        
        if ip:
            try:
                # Usar API gratuita para geolocalização
                response = requests.get(f'http://ip-api.com/json/{ip}', timeout=30)
                data = response.json()
                
                if data['status'] == 'success':
                    result = {
                        'ip': ip,
                        'success': True,
                        'country': data.get('country'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'zip': data.get('zip'),
                        'lat': data.get('lat'),
                        'lon': data.get('lon'),
                        'timezone': data.get('timezone'),
                        'isp': data.get('isp'),
                        'org': data.get('org'),
                        'as': data.get('as')
                    }
                else:
                    result = {
                        'ip': ip,
                        'success': False,
                        'error': data.get('message', 'Erro desconhecido')
                    }
            except Exception as e:
                result = {
                    'ip': ip,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/geoip.html', {'result': result})

@login_required
def latency(request):
    """Ferramenta de Monitoramento de Latência"""
    result = None
    if request.method == 'POST':
        host = request.POST.get('host', '').strip()
        count = int(request.POST.get('count', '10'))
        
        if host:
            try:
                latencies = []
                for i in range(min(count, 20)):  # Limitar a 20 pings
                    start_time = time.time()
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        result_code = sock.connect_ex((host, 80))
                        sock.close()
                        
                        if result_code == 0:
                            latency_ms = (time.time() - start_time) * 1000
                            latencies.append(round(latency_ms, 2))
                        else:
                            latencies.append(None)
                    except Exception:
                        latencies.append(None)
                    
                    time.sleep(1)  # Aguardar 1 segundo entre pings
                
                valid_latencies = [l for l in latencies if l is not None]
                
                if valid_latencies:
                    result = {
                        'host': host,
                        'success': True,
                        'latencies': latencies,
                        'min': min(valid_latencies),
                        'max': max(valid_latencies),
                        'avg': round(sum(valid_latencies) / len(valid_latencies), 2),
                        'packet_loss': round((len(latencies) - len(valid_latencies)) / len(latencies) * 100, 1)
                    }
                else:
                    result = {
                        'host': host,
                        'success': False,
                        'error': 'Não foi possível conectar ao host'
                    }
            except Exception as e:
                result = {
                    'host': host,
                    'success': False,
                    'error': f'Erro: {str(e)}'
                }
    
    return render(request, 'network_tools/latency.html', {'result': result})

