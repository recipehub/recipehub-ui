## RecipeHub UI [![Build Status](https://travis-ci.org/recipehub/recipehub-ui.png)](https://travis-ci.org/recipehub/recipehub-ui)

* Uses the recipehub-service API to store and version recipes
* Implements social features like following, rating and commenting
* Integrates elasticsearch
* Exposes ReST API used by Angular App

## Authors


* [Ashwin Agrawal](https://github.com/ashwinagrawal1007): Models, utils and search
* [Pratik Vyas](https://github.com/pdvyas): RecipeHub service integration, ReST API and Angular app.

### Installation
#### Install and run [recipehub-service](https://github.com/recipehub/recipehub-service)

* Clone this repository

    ```
    cd /your/projects/dir
    git clone https://github.com/recipehub/recipehub-ui recipehub-ui
    cd recipehub-ui
    ```

* Install virtualenv, virtualenvwrapper

    ```
    sudo pip install virtualenv virtualenvwrapper
    ```

* source virtialenvwrapper.sh in your bashrc / zshrc

    ```
    echo source `which virtualenvwrapper.sh` >> ~/.bashrc
    ```

* Start a new shell or source virtualenvwrapper.sh

    ```
    source `which virtualenvwrapper.sh`
    ```

* Make a virtualenv

    ```
    mkvirtualenv recipehub-ui -a `pwd` && add2virtualenv `pwd`
    ```

* Install requirements

    ```
    workon recipehub-ui
    pip install -r requirements.txt
    ```

### Run

    foreman run python manage.py runserver
    
#### Test

    make test

    They are also run on Travis, https://travis-ci.org/recipehub/recipehub-ui

### License

GNU GPL v3
