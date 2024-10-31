#!/bin/bash

# Gerekli paketlerin yüklenmesi
echo "Gerekli paketlerin yüklenmesi..."
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install python-dotenv selenium webdriver-manager

# Google Chrome'u yükle
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Temizlik yap
rm google-chrome-stable_current_amd64.deb

# .env dosyasını oluşturma
echo "Lütfen Metamask recovery phrase (kurtarma ifadesi) girin:"
read RECOVERY_PHRASE

echo "Lütfen Metamask şifresi girin:"
read -s PASSWORD  # -s bayrağı, girdinin gizli kalmasını sağlar

# .env dosyasını oluştur
echo "RECOVERY_PHRASE=$RECOVERY_PHRASE" > .env
echo "PASSWORD=$PASSWORD" >> .env

echo ".env dosyası oluşturuldu. Kurulum tamamlandı."

# Otomasyonu başlatma
echo "Otomasyon başlatılıyor..."
python3 automate.py
