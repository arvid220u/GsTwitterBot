# GsTwitterBot
A twython based Twitter bot. Creating tweets by running a Markov algorithm on followers' tweets. Powering @gsgottsnack Twitter account.

## Setup
* Clone, download or fork this repository.
* Locate the GsTwitterBot folder, and rename the file "apikeys_template.py" to "apikeys.py"
* Open the newly renamed "apikeys.py" and fill in your api keys, as obtained from https://apps.twitter.com.
* Run by writing "python3 mainbot.py" in your terminal. (Make sure python 3 is installed, or try with python 2 at your own risk.)

## Compatibility

Should support all python 3+ versions. It may run on python 2.x, but there will probably need to be some modifications, particularly with string encodings.

Has only been tested to work on python 3.2

## Dependencies

Currently relies on [Twython](https://github.com/ryanmcgrath/twython) for connecting to the Twitter APIs in an effortless way.

## Project status
* GsTwitterBot is actively developed by @ArVID220u as a side project, irregularly.
* GsTwitterBot is not in a release-state yet. This means that there are many unstable commits in-between the stable ones. Stable versions may be marked as 'stable' in the commit message. GsTwitterBot will, sometime in the future, be release-ready.
* Not being ready for release also means that some features may be customized for the current running implementation of this bot, the Twitter account @gsgottsnack. If you would attempt to implement your own bot with this code as a base, make sure to read through the whole source code as there can be lines of code not general enough. This will be fixed in the release-ready version in the future, where I'll probably fork out a general version.
* You are very much welcome to contribute to this project. You can do this in form of a fork and then a pull request, or you can contact me directly so I can invite you as a contributor.
