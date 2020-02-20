# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.

# This source code is licensed under the license found in the LICENSE file in the root directory of this source tree.

from typing import Dict, List, Optional

import pyudev


class DigitHandler:
    STREAMS = {
        # VGA resolution support 30 (default) and 15 fps
        "VGA": {
            "resolution": {"width": 640, "height": 480},
            "fps": {"30fps": 30, "15fps": 15}
        },
        # QVGA resolution support 60 (default) and 30 fps
        "QVGA": {
            "resolution": {"width": 320, "height": 240},
            "fps": {"60fps": 60, "30fps": 30},
        },
    }

    @staticmethod
    def _parse(digit_dev: Dict[str, str]) -> Dict[str, str]:
        digit_info = {'dev_name': digit_dev['DEVNAME'], 'manufacturer': digit_dev['ID_VENDOR'],
                      'model': digit_dev['ID_MODEL'], 'revision': digit_dev['ID_REVISION'],
                      'serial': digit_dev['ID_SERIAL_SHORT']}
        return digit_info

    @staticmethod
    def list_digits() -> List[Dict[str, str]]:
        context = pyudev.Context()
        digits = context.list_devices(subsystem="video4linux", ID_MODEL="DIGIT")
        digits = [dict(DigitHandler._parse(_)) for _ in digits]
        return digits

    @staticmethod
    def find_digit(serial: str) -> Optional[Dict[str, str]]:
        digits = DigitHandler.list_digits()
        for digit in digits:
            if digit['serial'] == serial:
                return digit
        return None