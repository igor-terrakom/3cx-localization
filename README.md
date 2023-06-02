# 3cx-localization

This is a simple python script which can be used to add unsupported localisation to latest version of 3cx (v18).

Script will do following  tasks:

1. replace Polish language with language you like  - in  this example  Croatian
2. replace Polish flag with Croatian
3. replace Polish localization file  in  folder l10n with localisations from  translations.json file

If you want  to use it for  your language you  have to:

1. change Croatian language for your  desired language
2. change Croatian flag to your desired flag. Flag should  be 24px with transparent  background
3. add translations in translations.json file
4. upload 3cx_localization.py & translations.json  file to your 3cx (this  is  for  linux)
5. run python  3cx_localization.py
