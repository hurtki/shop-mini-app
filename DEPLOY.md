# App deploying

# 1. Clone branch `master`:

```bash
git clone -b master https://github.com/hurtki/shop-mini-app.git
cd shop-mini-app
```

# 2. Create `.env` with this variables:

```python
DJANGO_SECRET_KEY="your key" # secret django key

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,[::1]

POSTGRES_USER=django_user        # Username for PostgreSQL

POSTGRES_PASSWORD=1234           # password for PostgreSQL

POSTGRES_DB=django_db            # Name if database

DB_HOST=postgres                 # name of the sevice of database ( DONT CHANGE !!! )

DB_PORT=5432                    # port of database
```

---

# 3. Docker-Compose, containers building

### No SSL certificate deploy

```bash
docker compose -f docker-compose.nossl.yml up --build -d
```

### SSL Certificate deploy

```bash
docker compose up --build -d
```

#### Getting SSL Certificate

- The DNS A record of your domain or subdomain must point to the IP of your server
- Then run:

```sh
docker run --rm \
 -v $(pwd)/certbot/conf:/etc/letsencrypt \
 -v $(pwd)/certbot/www:/var/www/certbot \
 certbot/certbot certonly \
 --webroot \
 --webroot-path=/var/www/certbot \
 --email you@example.com \
 --agree-tos \
 --no-eff-email \
 -d example.com -d www.example.com
```

- **you need to replace `you@example.com` with mail, the notifications about expiring certificate will go there**
- **you need to replace `example.com` and `www.example.com` with your domain**

### DEV deploy

```bash
docker compose -f docker-compose.dev.yml up --build -d
```

More info about dev docker-compose at the bottom

---

# 4. After Containers started, build static files and make migrations from django container shell:

```bash
docker exec -it --user root django sh
python manage.py migrate
python manage.py collectstatic --noinput
exit
```

# 5. Admin user creation

```bash
docker exec -it --user root django sh
python manage.py createsuperuser
```

**Then easy flow of user creation**

```sh
Username: hurtki
Email address:
Password:
Password (again):
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

> To access admin panel, visit `/admin/`, and use there creditionals you used to create admin user.

# Dev Deploying information

| Component | Dev Environment                                                                       | Production Environment                                                      | Purpose / Why?                                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ports     | Ports like 8000 (Django) and 6379 (Redis) are exposed outside                         | Only ports 80 (HTTP) and 443 (HTTPS) are exposed; internal ports are closed | In dev, exposing ports helps with debugging and direct access; in production, minimizing exposed ports improves security and mimics real-world setup |
| Nginx     | Uses lightweight config without SSL (e.g., `tg-shop.dev.conf`)                        | Uses full SSL-enabled config with certbot integration                       | Simplifies dev setup by skipping HTTPS; production requires HTTPS for security and trustworthiness                                                   |
| Certbot   | Not included                                                                          | Included as a separate service to manage SSL certificates                   | SSL certificates are unnecessary in dev but essential in production for encrypted communication                                                      |
| Redis     | Port 6379 exposed for easy external access and debugging                              | Redis runs internally, no ports exposed externally                          | Exposing Redis port in dev allows use of GUI tools and easier troubleshooting; production hides Redis for security                                   |
| Volumes   | Local directories for static files, media, and logs are mounted to allow live updates | Same local mounts plus additional volumes for certbot SSL files             | Allows instant code and asset changes without rebuilding containers in dev; in production also persists SSL certificates and logs                    |
