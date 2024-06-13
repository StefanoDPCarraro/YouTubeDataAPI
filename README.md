# YouTubeDataAPI

How to use:

To test the code yourself you will need to obtain yourself a Google API Key through the Google Cloud Console site.
Once you have the API you have to create a file in this folder named config.py, create in it a variable called API_KEY and give it the String value of your Google API Key
You're then ready to go, just run the main file you want to use(so for example "main_comments.py" for the comments).

The method call is all the way down the code and it recieves 2 parameters, the name of the video(Used to saving it in a JSON file)
and the ID the video you want to extract data from, which you can get from the url of the video(it will always have the same lenghth so if it does not you are selecting something else togheter with the ID)

Progress so far:
Only able to extract comments and save them on JSON file.

Coming soon:
Looking to extract captions, likes and other statistics(in separete files at first).

Final plan:
Make everything happen togheter and save it all in the same file, making it the easiest possible for the user.
