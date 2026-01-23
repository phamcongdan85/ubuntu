RCA Docker Demo (remote server)
=================================

This demo runs on server and exposes services on the server's public IP (e.g., 172.20.1.36).

Ports exposed (host:container):
- Grafana: 3017 -> 3000
- RCA API: 8017 -> 8000
- InfluxDB: 8087 -> 8086

Usage (on server):
1) Install Docker & docker-compose
2) Copy this folder to server, e.g. ~/rca_docker_demo
3) Run: docker-compose up -d
4) Visit Grafana: http://<server-ip>:3017 (admin/admin)
5) Call RCA API: POST http://<server-ip>:8017/infer

Notes:
- The compose file maps internal influxdb to container port 8086, and host port 8087.
- The RCA service writes to Influx using the internal service name 'influxdb' (http://influxdb:8086).
