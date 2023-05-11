# xkcdfinder
Source code behind the xkcdfinder.com website

Install Python dependencies with "**pip install -r requirements.txt**" at project root. Inside the **/site** directory, run "**npm install** to install JavaScript dependencies.

When inside the **/site** directory, you can run "**npm run dev**" to preview the site on your localhost. You can also run "**npm run build**" to build the site.

You'll need to login to nomic for the comic dot plot visualization. Run "**nomic login**" and follow the steps.

Once you have build the website, you'll probably want to populate the vector database. You'll need to create a **keys.json** file that contains your openai and pinecone vector database api keys. It will look like this:
```json
{"pinecone":"pinecone api key", "openai":"openai api key"}
```
Then you can run **populate.py** to populate the pinecone vector database. On the [xkcdfinder.com](https://xkcdfinder.com) website, I run this script periodically to keep the vector database updated. On the initial run, this script will take a long time to run as you will need to index 2000+ xkcds.

If you have built the site and populated the database, you can run **server.py** to run the server on your localhost. The site should now function exactly the same on your localhost as on the xkcdfinder.com website.
