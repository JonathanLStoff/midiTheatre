import logging

# Create a custom logger
LOGGER = logging.getLogger('midiTheatreLogger')

# Set the default log level
LOGGER.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('midiTheatre.log')

# Set log level for handlers
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
LOGGER.addHandler(console_handler)
LOGGER.addHandler(file_handler)

