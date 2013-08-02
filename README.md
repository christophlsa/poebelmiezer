# poebelmiezer

twitter follower management

## Requirements

-   python 3
-   [twitter](https://github.com/sixohsix/twitter)

first time:
    virtualenv -p python3 env
    source env/bin/activate
    pip install twitter
    deactivate

next time:
    source env/bin/activate
    python run.py
    deactivate

Before you start you have to create a settings file. Rename the
`settings.json.sample` to `settings.json`. Then you have to create a
[twitter app](https://dev.twitter.com/apps) with your target twitter account.
This app needs read and write access. Put the app settings in the settings file.
