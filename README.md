# 3cx-localization

This is a simple Python script that can be used to add unsupported localization to the latest version of 3CX (v18).

The script will perform the following tasks:

1. Replace the Polish language with the language you desire (in this example, Croatian).
2. Replace the Polish flag with the Croatian flag.
3. Replace the Polish localization file in the 'l10n' folder with localizations from the 'translations.json' file.

If you want to use it for your language, you need to:

1. Change the Croatian language to your desired language.
2. Change the Croatian flag to your desired flag. The flag should be 24px with a transparent background.
3. Add translations in the 'translations.json' file.
4. Upload the '3cx_localization.py' and 'translations.json' files to your 3CX (for Linux).
5. Run 'python 3cx_localization.py'.
