import os
import re
import json
import gzip
import shutil
import fnmatch
from datetime import datetime


def check_dependencies():
    # Check if 'translations.json' file exists
    if not os.path.isfile('translations.json'):
        print('"translations.json" file not found')
        return False

    # Ask user to input the folder of 3cx installation
    installation_folder = input('Please input the folder of 3cx installation (default: /var/lib/3cxpbx): ')
    if not installation_folder:
        installation_folder = '/var/lib/3cxpbx'

    # If the installation folder does not exist, exit
    if not os.path.isdir(installation_folder):
        print('Installation folder does not exist')
        return False

    wwwroot = os.path.join(installation_folder, 'Data', 'Http', 'wwwroot')
    if not os.path.isdir(wwwroot):
        print('"wwwroot" directory not found')
        return False

    # Search for the file starting with "main." and ending with ".js"
    for file in os.listdir(wwwroot):
        if fnmatch.fnmatch(file, 'main.*.js'):
            main_file = file
            break
    else:
        print('No "main.*.js" file found')
        return False

    # Check if 'i10n' directory exists and 'en.json' and 'pl_PL.json' files exist in it
    i10n_folder = os.path.join(wwwroot, 'l10n')
    if not os.path.isdir(i10n_folder) or not all(os.path.isfile(os.path.join(i10n_folder, file)) for file in ['en.json', 'pl_PL.json']):
        print('"l10n" directory or "en.json", "pl_PL.json" files not found')
        return False

    return True, wwwroot, main_file


def create_backup(wwwroot, main_file):
    if not os.path.isdir('backup'):
        os.makedirs('backup')

    i10n_folder = os.path.join(wwwroot, 'l10n')
    shutil.copy2(os.path.join(wwwroot, main_file), 'backup/{}__{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'), main_file))
    shutil.copy2(os.path.join(i10n_folder, 'en.json'),'backup/{}__{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'), 'en.json'))
    shutil.copy2(os.path.join(i10n_folder, 'pl_PL.json'), 'backup/{}__{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'), 'pl_PL.json'))
    if os.path.isfile(os.path.join(wwwroot, main_file + '.gz')):
        shutil.copy2(os.path.join(wwwroot, main_file + '.gz'), 'backup/{}__{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'), main_file + '.gz'))


def replace_pl_language(wwwroot, main_file):
    with open(os.path.join(wwwroot, main_file), 'r') as f:
        content = f.read()

    content = content.replace('Polski', 'Hrvatski')

    flag_pl = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48Y2lyY2xlIGN4PSIyNTYiIGN5PSIyNTYiIHI9IjI1NiIgZmlsbD0iI2YwZjBmMCIvPjxwYXRoIGQ9Ik01MTIgMjU2YzAgMTQxLjM4NC0xMTQuNjE2IDI1Ni0yNTYgMjU2UzAgMzk3LjM4NCAwIDI1NiIgZmlsbD0iI2Q4MDAyNyIvPjwvc3ZnPg=="
    flag_hr = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAMAAADXqc3KAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAJzUExURQAAAE1NTUxMTD8/P0NDQ0lJSVZXV2RnZ21xcVZXWEVFRVBRUXR3d0ZGRkhISGlra0pKSn1/f1ZWVmRkZG1tbXd3dlFRUGpqan9/fldXV2dnZnBwbqaoqM/Dw+XDw+69vaaoqbS0tPDCwv9/f/8/P/8eHv8REd7Ly/+AgP8aGv8AAOnMzP9SUu4LFe8MFNkjMOQbJOsNGPcHDME4R5pUa6IhUZwmU2OGiGN3hVcqeXYwcptdadomLP4FBm9wjiCXwGkvcX0ZWUmMjDeBlmddWlBUiUePrp9UavC/v/8WFqtCWiyc12ZLh5AaVoBcd3ZReXAsZmtbi49pgeoeJKapqf/Hx/9zc/90dP90c/F5fcZfb+hOV/lnav8wMf88PflobOBKVMtrevx3eM/Pz//////m5f8oJ/9jY//z8/81Nf9hYf/09P82Nv9OTf/6+eXl5f/t7f+fn/+Dg/9vb/+Li/+EhP+Jif+trf/4+O7u7v/y8v/s7P+Zmf/ExP+env8dHf+/v//p6f/m5v9FRf9paf/Pz/9ISP9nZ//Q0P9JSf9lZf/39/9kZP9ycv+urv9eXv9xcf+vr/9fX/9+fv/5+P/z8v+cm/8SEv/Nzf+hof/Gxf/w7//9/Kiop8bG5nNzwHR0wJp5sPmMj/+Yl/94eP+Zl+yJlId1tnN0wMTE3CsroBERkxMTlBITlBwVkX9couDM3fk5PPdfZNPG3mNBlhUTk4yMzBcXlhYXljUrmVcvi1IxjywlmRUWls3N1mFhuRQUlRMWlxQVlhYWls7O3WFiuRUVlWJiuS8vocbG3YuLzFFRsTIyoycnnsTEysbG18HB2neR+u4AAAAcdFJOUwAAAAU7isru/Moxn+oEZOJ49sru/Oqf4vbK7vxXaeIYAAAAAWJLR0Rkwtq4CQAAAAlwSFlzAAAOwwAADsMBx2+oZAAAAAd0SU1FB+cGARABG38xSIIAAAFPSURBVBgZRcHBahNRAIXh89+5gzOTlGgiIl0pCK59j4KbLqQrl4I+jgUfwa0+idAncKFITeOic2fGVnO8NyH1+5CE2JPDH2eyFCVQA/cB2dXaniQLwQyWFHKxsZMNzCoeAdqzfem/yVGCY7ZSRTFBOP6ORGjqx/VWLQcbhdsft1OEJVutuLPRluUlEZ7zVVdPOJD01D+hfgmI/5Jk+1M8WqCMO0GZjyLzpGxGsa1gUDYn0Knouu5z2867TjsdUXsNvKbo1tqJHlS4Y++bisHBvYpVW5w3zTMVvak/AJIDfHlBNkm23xAfvAfEwSjZfveLajU7RxIOZDfK/DZdRfc0MMqKEXpJrT30Dp7Gs7rWQroZUi8tdK8+GycHydPpb4e2Xczni7YNHk8nSwhmtN1HMjl7NYxOdpCd+ut0clHtXJyk6z7ZQhIiewiy185k6R9sVpqc2HV/3QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMy0wNi0wMVQxNjowMToxNiswMDowMHsCMQEAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjMtMDYtMDFUMTY6MDE6MTYrMDA6MDAKX4m9AAAAKHRFWHRkYXRlOnRpbWVzdGFtcAAyMDIzLTA2LTAxVDE2OjAxOjI3KzAwOjAwdbKkNQAAAABJRU5ErkJggg=="
    content = content.replace(flag_pl, flag_hr)

    with open(os.path.join(wwwroot, main_file), 'w') as f:
        f.write(content)

    # After modifying main_file, create a gzip version of it
    with open(os.path.join(wwwroot, main_file), 'rb') as f_in:
        with gzip.open(os.path.join(wwwroot, main_file + '.gz'), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def replace_pl_localisation(wwwroot):
    i10n_folder = os.path.join(wwwroot, 'l10n')
    # Cache for storing translations from 'translations.json'
    with open(os.path.join(wwwroot, 'translations.json'), 'r') as f:
        translation_cache = json.load(f)

    def translate_text(text):
        if isinstance(text, str):
            # Check if the text is a URL or path
            if re.match(r'^https?:\/\/', text) or re.match(r'^\/', text):
                return text

            # Check if the text is in the cache
            if text in translation_cache:
                return translation_cache[text]

            return text
        elif isinstance(text, list):
            return [translate_text(item) for item in text]
        elif isinstance(text, dict):
            return {k: translate_text(v) for k, v in text.items()}
        else:
            return text

    with open(os.path.join(i10n_folder, 'en.json'), "r") as f:
        data = json.load(f)

    translated = translate_text(data)

    with open(os.path.join(i10n_folder, 'pl_PL.json'), "w") as f:
        json.dump(translated, f, ensure_ascii=False, indent=4)


ret_val, wwwroot, main_file = check_dependencies()
if ret_val:
    create_backup(wwwroot, main_file)
    replace_pl_language(wwwroot, main_file)
    replace_pl_localisation(wwwroot)
