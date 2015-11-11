# Installation
## Dev

* Clone this repository

    ```
    cd /your/projects/dir
    git clone https://github.com/recipehub/ui recipehub-ui
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
    mkvirtualenv recipehub-ui-dev -a `pwd` && add2virtualenv `pwd`
    ```
