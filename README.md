# Euphrosyne
Euphrosyne is a Twitter bot that pulls hot posts from subreddits
at a given hour and tweets them.

## Installation
#### Setting up your Reddit account
Prepare the Reddit account you will be using by going to *apps* in [*preferences*](https://www.reddit.com/prefs/apps)
and clicking *create app*. 

![reddit_example](https://raw.githubusercontent.com/Montblac/Euphrosyne/main/img/reddit_example.png)

Choose the name of your app and a provide a brief description. 
Fill in the rest of the fields according to the image below.

![reddit_example2](https://raw.githubusercontent.com/Montblac/Euphrosyne/main/img/reddit_example2.png)

Save the keys that you get as you will be using them later.

#### Setting up your Twitter account
Prepare your Twitter account by going to the [developer portal](https://developer.twitter.com/en/docs/developer-portal/overview)
and applying for access to their API. From there, you will answer some short questions and gain access to the developer
dashboard.

![twitter_example](https://raw.githubusercontent.com/Montblac/Euphrosyne/main/img/twitter_example.png)

Once at the dashboard, click on *create app* and fill in the necessary fields. You will be given the API keys which you
will need to allow your program to tweet from your account. Go to the sidebar on the left and click on your project.
Scroll to *App Permissions* and make sure that *Read and Write* is enabled.

![twitter_example2](https://raw.githubusercontent.com/Montblac/Euphrosyne/main/img/twitter_example2.png)
 
 
 ##### Setting up your environment

Clone the repository to your machine.

    git clone https://github.com/Montblac/Euphrosyne.git

Optional: Create a virtual environment in the top level directory to maintain organization.
Avoid using .env as a directory name to prevent naming conflicts.

    python3 -m venv env

Install dependencies using *pip*. If you're using a virtual environment, you will have to activate it first.

    source env/bin/activate
    pip3 install -r requirements.txt

Remove the .example extension from [.env.example](.env.example) and add the API keys and access tokens from the Reddit
and Twitter accounts you will be using.

    export REDDIT_CLIENT_ID=
    export REDDIT_CLIENT_SECRET=
    
    export TWITTER_CONSUMER_KEY=
    export TWITTER_CONSUMER_SECRET=
    export TWITTER_ACCESS_TOKEN=
    export TWITTER_ACCESS_TOKEN_SECRET=

Now you can run the project. If you are using a virtual environment, make sure you have activated the environment.

    python3 euphrosyne.py


## License
[MIT](LICENSE)