from .captcha.mocap import Captcha, mocap
from .utils.fake_person import TotallyRealPerson
from .utils.string_utils import string_utils
from .utils.config import config
from .textgen.aigen import textgen
import requests, charlogger, time

class AntiTransNarc():
    def __init__(self, thread_id: int = -1) -> None:
        self.config = config()

        self.session = self.config.get_session()
        self.logger: charlogger.Logger = self.config.get_logger(thread_id=thread_id)
        self.identity = TotallyRealPerson()

        self.session.headers.update({
            "User-Agent": self.identity.user_agent
        })
        self.complaint_url = "https://ago.mo.gov/file-a-complaint/transgender-center-concerns"
        pass

    def run(self) -> None:
        try:
            self.initial_request()
            self.captcha = self.handle_captcha()
            response = self.submit_form()
        except:
            # recurse into oblivion lmao
            self.run()

    def submit_form(self) -> dict:
        """
        Submit the form. Returns a dict such as the following:
        { "success": True, "message": "We'll get those damn transes!!!!" }
        OR:
        { "success": False, "message": "You violent libtard, you're spamming our systems!! How DARE you!" }
        """

        body = self.get_form_body(captcha=self.captcha)
        resp = self.session.post(self.submit_url, data=body)

        if resp.status_code == 200:
            if "success" in resp.text.lower():
                msg = resp.text.split("style=\"margin: 0px 5px 0px 20px;\">")[1].split("</")[0].replace("\n", "")
                self.logger.valid(title="SUCCESS", data=f"Message: {msg}")
                return { "success": True, "message": msg }
            else:
                try:
                    err = resp.text.split("name=\"FormId\" />")[1].split("<div>")[1].split("</")[0]
                except Exception as e:
                    err = f"Unknown error! ({e})"
                self.logger.error(title="ERROR", data=f"Error: {err}")

                if "already" in err:
                    self.logger.warn(title="IP BLOCKED", data="Switch IPs to attempt again!")
                return { "success": True, "message": err }

    def handle_captcha(self) -> Captcha:
        """
        Handle the captcha fetching/solving.
        """
        captcha = None
        # TODO: Variate between audio/OCR solving.
        answer = ""
        tries = 0

        # If the answer is not five characters, fetch a new captcha and try again.
        # Since I'm 99% sure that they are all 5 characters, this will make sure that
        # we aren't just repeatedly flagging the system and getting IPs blocked.
        while len(answer) != 5:
            captcha = mocap.retrieve_captcha(session=self.session)
            self.logger.debug(title="CAPTCHA", data=f"Attempting to solve captcha. Total attempts: {tries}")
            answer = mocap.solve_audio(captcha=captcha)
            tries += 1
        
        captcha.answer = answer
        self.logger.paid(title="CAPTCHA", data=f"Solved captcha in {tries} tries. ({answer})")
        return captcha

    def get_form_body(self, captcha: Captcha) -> dict:
        data = {
            "TextFieldController_4": self.identity.first_name,
            "TextFieldController_5": self.identity.last_name,
            "TextFieldController_1": self.identity.street_address,
            "TextFieldController_2": self.identity.city,
            "DropdownListFieldController": "MO",
            "TextFieldController_6": self.identity.zip,
            "TextFieldController_0": self.identity.email,
            "TextFieldController_3": self.identity.phone_num,
            "ParagraphTextFieldController": self.write_incoherent_rant_about_trans_people(),
            "captcha-a": captcha.answer,
            "captcha-ca": captcha.correct_answ,
            "captcha-iv": captcha.init_vector,
            "captcha-k": captcha.key
        }
        return data
    
    def write_incoherent_rant_about_trans_people(self) -> str:
        """
        Uses a text-generation AI (that I am definitely NOT abusing API bugs in, lol) to write an incoherent rant about trans people.
        Uses prompts located in ./data/prompts.txt, so feel free to add anything you'd like!
        """
        name = f"{self.identity.first_name} {self.identity.last_name}"
        self.logger.info(title="TEXTGEN", data=f"Generating an incoherent rant about trans people from {name}...")
        ai = textgen()
        start_time = time.time() * 1000
        rant = ai.generate_text(name=f"{self.identity.first_name} {self.identity.last_name}", max_rant_size=self.config.max_rant_size).replace("\n", " ")
        end_time = time.time() * 1000
        self.logger.info(title="TEXTGEN", data=f"Generated an incoherent rant about trans people in {int(end_time - start_time)}ms.")
        if self.config.print_rants:
            self.logger.info(title="RANT", data=rant)
        return rant

    def initial_request(self) -> None:
        """
        Gather necesary data like cookies, authorization, etc.

        As far as I know, the only meaningful information gathered from this is an anti-bot cookie.
        """
        resp = self.session.get(self.complaint_url)
        form_action = resp.text.split("<form action=\"")[1].split("\"")[0]
        self.submit_url = "https://ago.mo.gov" + form_action
        self.logger.info(title="DATA", data=f"Got proper submit URL: {self.submit_url}")