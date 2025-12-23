# syntax=nobidev/dockerfile
FROM kukhanh0812/nginx-proxy:0.0.1
RUN <<-EOF
  apt-get update
  apt-get install libnginx-mod-http-geoip -y
  apt-get install -qq software-properties-common -y
  add-apt-repository ppa:maxmind/ppa -y
  apt update
  apt-get install -y libmaxminddb0 libmaxminddb-dev mmdb-bin geoipupdate libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev python3-pip
EOF

RUN apt-get install -y supervisor
ARG ACCOUNTID_GEO=dev
ARG LISENCE=dev

RUN <<-EOF
  sed -i -E "s/^(AccountID\s+).+/\1${ACCOUNTID_GEO}/g" /etc/GeoIP.conf
  sed -i -E "s/^(LicenseKey\s+).+/\1${LISENCE}/g" /etc/GeoIP.conf  
EOF
RUN geoipupdate
COPY geo-python /geo-python
COPY supervisord.conf /etc/supervisor/supervisord.conf
RUN pip3 install -r /geo-python/requirements.txt

CMD ["supervisord", "-c" ,"/etc/supervisor/supervisord.conf"]
