sudo systemctl stop able_fr24
echo Starting ./find_able.py
sudo cp able_fr24.service /etc/systemd/system
sudo systemctl enable able_fr24
sudo systemctl start able_fr24
