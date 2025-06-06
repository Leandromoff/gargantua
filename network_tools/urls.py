from django.urls import path
from . import views

app_name = 'network_tools'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ping/', views.ping, name='ping'),
    path('traceroute/', views.traceroute, name='traceroute'),
    path('port_scanner/', views.port_scanner, name='port_scanner'),
    path('nmap/', views.nmap, name='nmap'),
    path('dns_lookup/', views.dns_lookup, name='dns_lookup'),
    path('http_headers/', views.http_headers, name='http_headers'),
    path('ssl_check/', views.ssl_check, name='ssl_check'),
    path('geoip/', views.geoip, name='geoip'),
    path('latency/', views.latency, name='latency'),
]

