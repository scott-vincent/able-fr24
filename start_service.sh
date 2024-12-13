sudo systemctl stop able_fr24
echo Starting ./able_fr24.py
sudo cp able_fr24.service /etc/systemd/system
sudo systemctl enable able_fr24
sudo systemctl start able_fr24
