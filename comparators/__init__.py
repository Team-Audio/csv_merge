from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, Type
from comparators.base import ComparatorBase

comparators: Dict[str, Type[ComparatorBase]] = {}

_package_dir = Path(__file__).resolve().parent

for (_, module_name, _) in iter_modules([_package_dir]):
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):

        attribute = getattr(module, attribute_name)

        if not isclass(attribute):
            continue

        if not issubclass(attribute, ComparatorBase):
            continue

        if attribute is ComparatorBase:
            continue

        globals()[attribute_name] = attribute

        comparators[attribute_name] = attribute
