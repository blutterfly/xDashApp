# xDashApp
Develop multi-page `Dash` app.


**Home Page**.  home.py
+ NavBar: Home| Portal| Notes| Blog | Stocks| Songs| Demo 
+ This page contains bullets of each of the page describing its function and contents.
+ Implement by rendering markdown    'docs/home.md'

**Portal Page**.  portal.py
+ NavBar: Home| Back 
+ This page contains URLs of portals
  + Google
  + iCloud
  + Yahoo
  + Github
+ The links will be launched on a new tab   
+ Implement by rendering markdown    'docs/portal.md'

**Notes Page**.  notes.py
+ Display files in notes directory and its subdirs.
+ Display as a list.  When the file is clicked/selected display the contents in a multiline box.
+ Render accordingly based on its extension -- .md, .csv, .txt  


**Stocks Page**.  stocks.py
+ NavBar: Home| Back
+ execute script 'pages/stocks.py'


**About Page**. about.py 
+ NavBar: Home| Back
+ Header Line
+ Contact Card
+ About Card
+ Footer Line
