apt update
apt upgrade -y
apt install -y nginx python3-pip certbot python3-certbot-nginx supervisor


certbot certonly --nginx -d goztepeli.com -d www.goztepeli.com

pip install -U tornado requests beautifulsoup4
