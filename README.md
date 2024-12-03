Register MaxMind in website: https://www.maxmind.com/en/home <br />
Build image with  AccountID and Lisence of MaxMind: <br />
  - docker build -t harbor.elofun.net/devops/nginx-geoip:0.1.0 --build-arg ACCOUNTID_GEO=${AccountID} --build-arg LISENCE=${Lisence} . <br />
  
Combine with your Push Gateway: use environment: PUSHGATEWAY_ENDPOINT: "<ip|domain pushgateway>:9091"
  
  
    
