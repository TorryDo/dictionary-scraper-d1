# wiktionary_scraper
this project is made to parse word's definition from given text file, and save it to json format </br>

### I, Preparation:
- clone this project
- import required dependency
- go to main.py then pass required parameter: </br>
~ word_file_path: file path of your words text file (eg: ".../username/docs/words.txt")</br>
~ workspace_dir_path: directory path, should be empty directory</br>
~ accept_empty_word: False by default, it will ignore null word</br>
~ parallel: 5 by default, allow program run 'n' scraper asynchronously