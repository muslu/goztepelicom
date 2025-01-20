apt update
apt upgrade -y
apt install -y nginx nginx-extras python3-pip certbot python3-certbot-nginx supervisor net-tools unzip wget curl redis

systemctl enable redis-server && systemctl restart redis-server &&  systemctl status redis-server && netstat -pulten | grep redis


certbot certonly --nginx -d goztepeli.com -d www.goztepeli.com

pip install -U tornado requests beautifulsoup4 redis
