# -*- coding: UTF-8 -*-
import threading
import requests
import globalPluginHandler
import ui
from tones import beep
import scriptHandler


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()

    @scriptHandler.script(
        gesture="kb:nvda+shift+i", description="get ip information", category="ipan"
    )
    def script_ip(self, gesture):
        ip_thread = threading.Thread(target=self.fetch_ip_info)
        ip_thread.start()

    def fetch_ip_info(self):
        try:
            beep(500, 100)
            response = requests.get("http://ip-api.com/json/", timeout=7)
            response.raise_for_status()
            data = response.json()
            ip_address = data["query"]
            country = data["country"]
            region = data["regionName"]
            city = data["city"]
            isp = data["isp"]
            message = (
                f"IP Address: {ip_address}\n"
                f"Country: {country}\n"
                f"Region: {region}\n"
                f"City: {city}\n"
                f"ISP: {isp}"
            )
            ui.message(message)
        except requests.exceptions.Timeout:
            ui.message("request time out. Please try again later.")
        except Exception as e:
            ui.message("can't get ip info")
