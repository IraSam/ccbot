import os
from typing import Dict, Any

from utils.logging_utils import logging_inputs_info


@logging_inputs_info
def get_connection_details(name: str) -> Dict[str, Any]:
    all_variables = os.environ
    matched_keys = [key for key in all_variables if key.lower().startswith(name) and key.count('_') == 1]
    return {key.split('_')[1].lower(): os.environ.get(key) for key in matched_keys}
