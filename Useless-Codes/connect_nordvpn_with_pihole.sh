#!/bin/bash
nordvpn connect --group P2P spain #Connects to NordVPN
sleep 5              # Waits a few seconds for the VPN connection to establish
sudo nmcli device modify wlp5s0 ipv4.dns "127.0.0.1"  # Sets DNS to Pi-hole
sudo systemctl restart NetworkManager  # Restarts NetworkManager
