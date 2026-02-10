# srt-translations
Repo contains scripts i coded to translate .srt files to the language you want.

## General
So far, i have created one script to use GoogleTranslate and another one that uses DeepL API (free version).

## Requirements
- Have python installed on your machine

## How to Use
- Create virtual environment (I am using VS Code as editor that provides an easy way to create a virtual env in a few clicks only but you are free to do as you prefer)
- Install the required packages:
  ```
  pip install -r requirements.txt
  ```
- Run the script:
  ```
  python <script-name>.py -i abc.srt -o qwerty.srt -l(optional) "EN-US" -e(optional) "utf8"
  ```
