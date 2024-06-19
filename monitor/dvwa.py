from http_server import HttpServerMonitor
import logging
import multiprocessing
import os
from datetime import datetime
from scapy.all import sniff, wrpcap, TCP, IP, Raw

# ---------------------------------- Log Info -------------------------------------

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the minimum logging level
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()

# Set the logging level for the handler
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# ---------------------------------------------------------------------------------

http_methods = (
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "TRACE",
    "CONNECT"
)

class DVWAMonitor(HttpServerMonitor):
    def __init__(self, interface='lo', port=8000) -> None:
        super().__init__()
        self.process = None
        self.interface = interface
        self.port = port
        self.output_file = None

    def get_output_filename(self):
        """Generate the output filename based on the current date and system."""
        system_name = "DVWA"  # Replace with your actual system identifier if needed
        current_date = datetime.now().strftime("%y%m%d_%H%M")
        self.output_file = f"output/{current_date}_{system_name}.pcap"

    def packet_callback(self, packet):
        """Callback function to process each captured packet."""
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            if payload.split()[0] in http_methods and packet[TCP].dport == self.port:
                wrpcap(self.output_file, packet, append=True)
                logger.info("summary: " + packet.summary())

    def start_capture(self):
        """Capture HTTP traffic on the specified port using scapy."""
        logger.info(f"Starting capture on port {self.port}, saving to {self.output_file}")
        sniff(
            iface=self.interface,
            filter=f"tcp port {self.port}",
            prn=self.packet_callback,
            store=0,
            timeout=60  # Adjust as needed
        )
        logger.info(f"Capture saved to {self.output_file}")

    def start(self):
        """Start monitoring the HTTP server."""
        logger.info("Starting DVWA Monitor...")
        if not os.path.exists('output'):
            os.makedirs('output')
        self.get_output_filename()
        self.process = multiprocessing.Process(target=self.start_capture, args=())
        self.process.start()

    def stop(self):
        """Stop monitoring the HTTP server."""
        if self.process is not None:
            logger.info("Stopping DVWA Monitoring!")
            self.process.terminate()
            self.process.join()
            self.process = None
        else:
            logger.warning("DVWA Monitor is not running!!!")

# Example usage
if __name__ == '__main__':
    import argparse, time
    parser = argparse.ArgumentParser(description="Monitor DVWA")
    parser.add_argument('-r', '--range', type=int, default=20, help='Sleep time in seconds')

    args = parser.parse_args()
    sleep_time = args.range

    monitor = DVWAMonitor()
    try:
        monitor.start()
        # Run for some time or wait for some condition
        time.sleep(sleep_time)  # Use the parsed sleep time
    finally:
        monitor.stop()