#!/bin/bash
sudo apt-get update
# Python ve pip'in sistemde kurulu olup olmadığını kontrol et
echo "Python 3 ve pip'in sisteminizde kurulu olup olmadığını kontrol ediyoruz..."

# Python 3 kurulu değilse yükle
if ! command -v python3 &> /dev/null
then
    echo "Python 3 yüklü değil. Python 3 yükleniyor..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
    echo "Python 3 ve pip başarıyla yüklendi."
else
    echo "Python 3 zaten kurulu."
fi

# Pip'in yüklü olup olmadığını kontrol et
if ! command -v pip3 &> /dev/null
then
    echo "pip yüklü değil. pip yükleniyor..."
    sudo apt-get install -y python3-pip
    echo "pip başarıyla yüklendi."
else
    echo "pip zaten kurulu."
fi

# Gerekli Python paketlerini yükle
echo "Gerekli Python paketlerini yüklüyoruz..."
pip3 install selenium web3 python-dotenv webdriver-manager pyvirtualdisplay termcolor
sudo pip3 install --upgrade requests

# Google Chrome'u yükle
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Temizlik yap
rm google-chrome-stable_current_amd64.deb

# xvfb sanal ekran kurulumunu yap
sudo apt-get install xvfb
clear
# .env dosyasını oluştur
echo "Lütfen .env dosyasını oluşturmak için gerekli bilgileri girin:"
echo
# Kullanıcıdan Private Key ve Password bilgilerini al
echo "PRIVATE_KEY bilgisini girin:"
read PRIVATE_KEY
echo "Rainbow Wallet'ta kullanmak üzere bir PASSWORD bilgisi ekleyin. (Minimum 8 karakter, harf ve sayısal karakter kullanılması tavsie edilir):"
read PASSWORD

# .env dosyasını oluştur
echo "PRIVATE_KEY=$PRIVATE_KEY" > .env
echo "PASSWORD=$PASSWORD" >> .env

echo ".env dosyası başarıyla oluşturuldu. Gerekli yazılımlar yüklendi."

# Rivalz-oto-claim.py dosyasını çalıştır
echo "rivalz-oto-claim.py otomasyon dosyasını çalıştırıyoruz..."
python3 rivalz-oto-claim.py

