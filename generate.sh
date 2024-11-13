#!/usr/bin/env bash

./htmlize.py "./Zadanie dla JJunior AI Developera - tresc artykulu.txt"

export ARTICLE_HTML="$(cat ./article.html)"

envsubst < szablon.html > podglad.html
