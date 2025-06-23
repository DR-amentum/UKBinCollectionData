import argparse
import importlib
import importlib.util
import os
import sys
import logging
from uk_bin_collection.uk_bin_collection.get_bin_data import (
    setup_logging,
    LOGGING_CONFIG,
)

_LOGGER = logging.getLogger(__name__)


def import_council_module(module_name, src_path="councils"):
    """Dynamically import a council processor module from file."""
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, src_path, f"{module_name}.py")

    if not os.path.exists(full_path):
        _LOGGER.error("Council module file not found: %s", full_path)
        return None

    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



class UKBinCollectionApp:
    def __init__(self):
        self.setup_arg_parser()
        self.parsed_args = None

    def setup_arg_parser(self):
        """Setup the argument parser for the script."""
        self.parser = argparse.ArgumentParser(
            description="UK Bin Collection Data Parser"
        )
        self.parser.add_argument(
            "module", type=str, help="Name of council module to use"
        )
        self.parser.add_argument(
            "URL", type=str, help="URL to parse - should be wrapped in double quotes"
        )
        self.parser.add_argument(
            "-p",
            "--postcode",
            type=str,
            help="Postcode to parse - should include a space and be wrapped in double quotes",
            required=False,
        )
        self.parser.add_argument(
            "-n", "--number", type=str, help="House number to parse", required=False
        )
        self.parser.add_argument(
            "-s",
            "--skip_get_url",
            action="store_true",
            help="Skips the generic get_url - uses one in council class",
            required=False,
        )
        self.parser.add_argument(
            "-u", "--uprn", type=str, help="UPRN to parse", required=False
        )
        self.parser.add_argument(
            "-w",
            "--web_driver",
            type=str,
            help="URL for remote Selenium web driver - should be wrapped in double quotes",
            required=False,
        )
        self.parser.add_argument(
            "--headless",
            dest="headless",
            action="store_true",
            help="Should Selenium be headless. Defaults to true. Can be set to false to debug council",
        )
        self.parser.add_argument(
            "--not-headless",
            dest="headless",
            action="store_false",
            help="Should Selenium be headless. Defaults to true. Can be set to false to debug council",
        )
        self.parser.set_defaults(headless=True)
        self.parser.add_argument(
            "--local_browser",
            dest="local_browser",
            action="store_true",
            help="Should Selenium be run on a remote server or locally. Defaults to false.",
            required=False,
        )
        self.parser.add_argument(
            "-d",
            "--dev_mode",
            action="store_true",
            help="Enables development mode - creates/updates entries in the input.json file for the council on each run",
            required=False,
        )
        self.parsed_args = None

    def set_args(self, args):
        try:
            self.parsed_args, _ = self.parser.parse_known_args(args)
        except SystemExit as e:
            import traceback
            import sys
            import logging
            _LOGGER = logging.getLogger(__name__)
            _LOGGER.error("💥 argparse failed with SystemExit: %s", e)
            _LOGGER.error("💥 args = %s", args)
            _LOGGER.error("💥 traceback:\n%s", "".join(traceback.format_exception(*sys.exc_info())))
            raise ValueError("Invalid CLI arguments passed to UKBinCollectionApp")


    def run(self):
        """Run the application with the provided arguments."""
        council_module = import_council_module(self.parsed_args.module)
        return self.client_code(
            council_module.CouncilClass(),
            self.parsed_args.URL,
            postcode=self.parsed_args.postcode,
            paon=self.parsed_args.number,
            uprn=self.parsed_args.uprn,
            skip_get_url=self.parsed_args.skip_get_url,
            web_driver=self.parsed_args.web_driver,
            headless=self.parsed_args.headless,
            local_browser=self.parsed_args.local_browser,
            dev_mode=self.parsed_args.dev_mode,
            council_module_str=self.parsed_args.module,
        )

    def client_code(self, get_bin_data_class, address_url, **kwargs):
        """
        Call the template method to execute the algorithm. Client code does not need
        to know the concrete class of an object it works with, as long as it works with
        objects through the interface of their base class.
        """
        return get_bin_data_class.template_method(address_url, **kwargs)


def run():
    """Set up logging and run the application."""
    global _LOGGER
    _LOGGER = setup_logging(LOGGING_CONFIG, None)
    app = UKBinCollectionApp()
    app.set_args(sys.argv[1:])
    print(app.run())


if __name__ == "__main__":
    run()
