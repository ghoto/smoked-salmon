#!/usr/bin/env python3
import xmlrpc.client
from transmission_rpc import Client as ts_client

def add_torrent_to_rutorrent(server_url, torrent_path, directory, label):
    client = xmlrpc.client.Server(server_url)
    with open(torrent_path, 'rb') as torrent_file:
        torrent_bin = xmlrpc.client.Binary(torrent_file.read())
        client.load.raw_start_verbose('', torrent_bin, 'print=d.hash=', 'd.directory.set=' + directory, 'd.custom1.set=' + label)

def add_torrent_to_transmission(torrent_path, host, port, directory, username, password):
    client = ts_client(host=host, port=port, username=username, password=password)
    with open(torrent_path, 'rb') as torrent_fh:
        client.add_torrent(torrent_fh, download_dir = directory)
