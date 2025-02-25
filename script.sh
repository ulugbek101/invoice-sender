sudo systemctl daemon-reload

sudo systemctl start celery

sudo systemctl enable celery

sudo systemctl status celery

sudo systemctl stop celery

sudo systemctl restart celery

sudo journalctl -u celery

sudo chown -R www-data:www-data /UUmaraliyev/invoice-sender

sudo chmod -R u+x /UUmaraliyev/invoice-sender

