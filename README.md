ThinkBayes
==========

Code repository for Think Bayes: Bayesian Statistics Made Simple
by Allen B. Downey

Available from Green Tea Press at http://thinkbayes.com.

Published by O'Reilly Media, October 2013.

## ROSS INSTRUCTIONS
How to get set up if you are, say, starting from scratch on a new laptop. Instructions below assume that you have already cloned my forked version of this repo and are using `pyenv` and `pyenv-virtualenv`.

```
pyenv install 2.7.16
pyenv virtualenv 2.7.16 think-bayes
pyenv activate think-bayes
pip install code/requirements.txt
```

The convention that I am using for working the end of chapter exercise is to put each in its own file within the `code` directory with the naming convention of `NNchapter_exerciseN.py`. What this means is that in order to see the results of Chapter 2 exercise 1, from the top-level directory of the repo you would ...

```
pyenv activate think-bayes
python code/02chapter_exercise1.py
```

### Warning
The code base from the forked repo is old enough to still rely on Python 2, which as of yesterday is officially not supported. I'm kind of just hoping this doesn't bite me in the short term... :/