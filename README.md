# Gmail-API-autoreply

Auto reply to unread emails using Gmail API python. 

# Get started 

First to get started follow this [https://developers.google.com/gmail/api/quickstart/python]

Once you get your token.pickle file you're good to go. 

Just run your script manually to reply to emails. (You do not need Procfile, requirements.txt and app.py for this part)

Note: This only replies when you run the script.


# Automate replying

To automate this you'll need to get used to the heroku workflow. Push the folder containing all these file(including your token.pickle) to a heroku project. 

After pushing the project, you will need to use the free scheduler add-on available on heroku. Here's more about it https://devcenter.heroku.com/articles/scheduler

This is how you can run scripts on heroku - https://www.youtube.com/watch?v=aTSw6rXmtsM&t=48s
