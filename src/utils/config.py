import json, charlogger, requests, random

class config():
    def __init__(self) -> None:
        self.load()
        self.use_proxies = self._config_json.get("use_proxies")
        self.thread_count = self._config_json.get("threads")
        self.wait_to_continue = self._config_json.get("wait_to_continue") and self.thread_count <= 1
        self.max_rant_size = self._config_json.get("max_rant_size")
        self.print_rants = self._config_json.get("print_rants")
        pass

    def add_proxies(self, session: requests.Session) -> requests.Session:
        if self._config_json.get("use_proxies"):
            proxy_list = [x.strip() for x in open(f"data/{self._config_json.get('proxy_file')}", "r", encoding="utf8").readlines()]

            self.proxy = f"{self._config_json.get('proxy_type')}://{random.choice(proxy_list)}"
            session.proxies.update({
                "http": self.proxy,
                "https": self.proxy
            })
        
        return session


    def get_logger(self, thread_id: int) -> charlogger.Logger:
        if thread_id == -1:
            return charlogger.Logger(
                debug=self._config_json.get("debug")
            )
        else:
            self.prefix_str = f"{thread_id + 1}"
            if thread_id < 100:
                if thread_id < 10:
                    self.prefix_str = f"00{thread_id}"
                else:
                    self.prefix_str = f"0{thread_id}"
            return charlogger.Logger(
                debug=self._config_json.get("debug"),
                defaultPrefix=f"THREAD {self.prefix_str}"
            )

    def load(self) -> dict:
        self._config_json = json.loads(open("data/config.json", "r").read())