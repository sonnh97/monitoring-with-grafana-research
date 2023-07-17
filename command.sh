curl --location --output /root/statsd.conf https://raw.githubusercontent.com/databand-ai/airflow-dashboards/main/statsd/statsd.conf
docker run --name fdev_statsd_exporter -d -p 9103:9103 -p 9126:9126 -p 9126:9126/udp -v /root/airflow/monitoring/statsd_mapping.yml:/tmp/statsd_mapping.yml prom/statsd-exporter --statsd.mapping-config=/tmp/statsd_mapping.yml --statsd.listen-udp=":9126" --statsd.listen-tcp=":9126" --web.listen-address=":9103"
docker run --name fuat_pti_statsd_exporter -d -p 9102:9102 -p 9125:9125 -p 9125:9125/udp -v /root/airflow/monitoring/statsd_mapping.yml:/tmp/statsd_mapping.yml prom/statsd-exporter --statsd.mapping-config=/tmp/statsd_mapping.yml --statsd.listen-udp=":9125" --statsd.listen-tcp=":9125" --web.listen-address=":9102"
docker run --name prometheus -d -p 9092:9090 -v /root/airflow/monitoring/prometheus.yml:/etc/config/prometheus.yml prom/prometheus --config.file=/etc/config/prometheus.yml --web.enable-lifecycle --web.enable-remote-write-receiver
docker run --name pushgateway -d -p 9091:9091 prom/pushgateway
docker run --name grafana -d -p 3000:3000 -e "https_proxy=http://squid-rh8.vndirect.com.vn:80" -e "GF_INSTALL_PLUGINS=praj-ams-datasource" grafana/grafana-enterprise
docker run --name loki -d -v /root/airflow/monitoring/loki-config.yaml:/mnt/config/loki-config.yaml -p 3100:3100 grafana/loki:2.8.0 -config.file=/mnt/config/loki-config.yaml
docker run --name tempo -d -p 8004:80 -p 55680:4316 -p 55681:4317  -v /root/airflow/monitoring/tempo.yaml:/etc/tempo.yaml grafana/tempo -config.file=/etc/tempo.yaml --target=all --auth.enabled=false --distributor.log-received-traces=true --enable-go-runtime-metrics=true
docker run --name fake-tracing -e ENDPOINT=10.210.39.204:4317 -e HTTP_PROXY=http://squid-rh8.vndirect.com.vn:80 -e HTTPS_PROXY=http://squid-rh8.vndirect.com.vn:80 ghcr.io/grafana/xk6-client-tracing:v0.0.2



