from src.utils.config import config
from src import AntiTransNarc
import threading

class main():
    def __init__(self) -> None:
        self.config = config()

        if self.config.thread_count > 1:
            for _ in range(self.config.thread_count):
                def run_thread(thread_id: int):
                    thread_id = thread_id + 1
                    while True:
                        AntiTransNarc(thread_id=thread_id).run()
                threading.Thread(target=run_thread, args=(_,), daemon=True).start()
            input("")
        else:
            self.run(-1)
    
    def run(self, thread_id: int):
        while True:
            AntiTransNarc(thread_id=thread_id).run()
            if self.config.wait_to_continue:
                input("Press enter to continue.")
        

if __name__ == "__main__":
    main()