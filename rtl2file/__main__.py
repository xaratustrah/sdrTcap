#
# RTL2FILE
# Software defined radio based time capture
#
# (2025) xaratustrah@github
#

import argparse
import toml
from rtlsdr import RtlSdr
import os
import signal
import sys
from datetime import datetime
from tqdm import tqdm
from loguru import logger

def parse_arguments():
    parser = argparse.ArgumentParser(description='SDR Configuration')
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration TOML file')
    parser.add_argument('--no-progress', action='store_true', help='Disable progress bar')
    return parser.parse_args()

def load_config(config_path):
    config = toml.load(config_path)
    validate_config(config)
    return config

def validate_config(config):
    required_keys = {
        'file_config': {
            'file_path': str,
            'file_size': (int, float),
            'lframe': int,
        },
        'sdr_config': {
            'sample_rate': (int, float),
            'center_freq': (int, float),
            'freq_correction': int,
            'gain': (int, float, str),
        }
    }
    
    for section, keys in required_keys.items():
        if section not in config:
            raise ValueError(f'Missing section: {section}')
        for key, expected_type in keys.items():
            if key not in config[section]:
                raise ValueError(f'Missing key: {key} in section: {section}')
            if not isinstance(config[section][key], expected_type):
                raise ValueError(f'Invalid type for key: {key} in section: {section}. Expected {expected_type}, got {type(config[section][key])}')

def create_output_directory(file_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(file_path, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def write_samples_to_file(samples, file_number, output_dir):
    file_name = f'{output_dir}/{file_number:08d}.bin'
    with open(file_name, 'ab') as f:
        f.write(samples.tobytes())

def signal_handler(sig, frame, sdr):
    logger.info('Exiting gracefully...')
    sdr.close()
    sys.exit(0)

def main():
    args = parse_arguments()
    config = load_config(args.config)
    
    file_path = config['file_config']['file_path']
    max_file_size = int(config['file_config']['file_size']) * 1024 * 1024  # Convert MB to bytes
    lframe = int(config['file_config']['lframe'])

    sample_rate = float(config['sdr_config']['sample_rate'])
    center_freq = float(config['sdr_config']['center_freq'])
    freq_correction = int(config['sdr_config']['freq_correction'])
    gain = config['sdr_config']['gain']

    output_dir = create_output_directory(file_path)

    sdr = RtlSdr()
    sdr.sample_rate = sample_rate
    sdr.center_freq = center_freq
    sdr.freq_correction = freq_correction
    sdr.gain = gain

    file_number = 1
    file_size = 0

    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, sdr))

    logger.info(f'Starting SDR recording with parameters: sample_rate={sample_rate} Hz, center_freq={center_freq} Hz, freq_correction={freq_correction} PPM, gain={gain}, lframe={lframe}, max_file_size={max_file_size} bytes')

    if args.no_progress:
        progress_bar = lambda total, unit, unit_scale, desc: iter([None])
        update_progress = lambda x: None
        close_progress = lambda x: None
    else:
        progress_bar = tqdm
        update_progress = lambda x: x.update(len(samples_bytes))
        close_progress = lambda x: x.close()

    try:
        pbar = progress_bar(total=max_file_size, unit='B', unit_scale=True, desc=f'Writing file {file_number:08d}.bin')
        while True:
            samples = sdr.read_samples(lframe)
            samples_bytes = samples.tobytes()

            if file_size + len(samples_bytes) > max_file_size:
                close_progress(pbar)
                file_number += 1
                file_size = 0
                pbar = progress_bar(total=max_file_size, unit='B', unit_scale=True, desc=f'Writing file {file_number:08d}.bin')
                #logger.info(f'Starting new file: {file_number:08d}.bin')

            write_samples_to_file(samples, file_number, output_dir)
            file_size += len(samples_bytes)
            update_progress(pbar)

    finally:
        close_progress(pbar)
        sdr.close()
        logger.info('SDR recording stopped.')

if __name__ == '__main__':
    main()
