#!/usr/bin/python

#Anyssa Buchanan
#My Project: recipeBook
#My web application Recipe Book utilizes mysql database recipeBook to extract the recipes by type, ingredients
# as well as the ability to update and add new recipes. 

import MySQLdb as db
import time
import cgi
import cgitb; cgitb.enable()

print "Content-Type: text/html"
print ""

################################################################################
def getConnectionAndCursor():
    """
    This function will connect to the database and return the
    Connection and Cursor objects.
    """ 
    # connect to the MYSQL database
    conn = db.connect(host="localhost",
                      user="anyssab",
                      passwd="5467",
                      db="anyssab")

    cursor = conn.cursor()
    return conn, cursor

################################################################################
def doHTMLHead(title):

    #implement javascript in order to establish a drop down menu for recipe type
    #by using javascript I was able to create a drop down menu that loaded the results by recipe type, once
    #a type was selected the results load instantly
    #javascript was also used to create a dynamic home page with changing imges every 15 seconds

    print """
    <html>
    <head>
    <script type= "text/javascript">

    function getRecipeT(){

    var elt = document.getElementById("recipeSelect");

    var recipeType = elt.options[elt.selectedIndex].text;

    var newRecipe = document.URL;

    var linktoRecipe = newRecipe + "?recipeType=" + recipeType;

    window.location.href = linktoRecipe;

    }

    // handles first array of picture for the top image changer
    var images = new Array()
    images[0] = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/leafapple.jpg";
    images[1] = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/recipe1.JPG";
    images[2] = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/fluff.jpg";
    
    
    var timerid = setInterval(changeImage,2000);

    var x= 0;

    function changeImage()
    {
        if(x >= images.length) { x = 0; }

        // not sure what this does!
        var img = document.getElementById("img");

        // get image by index number
        img.src = images[x];

        x++;
    }
    
    
    
    
    //econd array of pictures that handles the bottom changing image
    var images2 = new Array()
    images2[0] = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/cupcaketower.jpg";
    images2[1] = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/recipe2.JPG";
    images2[2] = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/frontbabka.jpg";
    
    var timerid2 = setInterval(changeImage2,2000);
    var y= 0;
    function changeImage2()
    {
      if(y >= images2.length) { y = 0; }
    
    // not sure what this does!
        var img1 = document.getElementById("img1");
    
    // get image by index number
        img1.src = images2[y];

        y++;
    }


    </script>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js"></script>
    <title>%s</title>
    </head>
    <body style= "background-color:PapayaWhip;">
    <h1 align="center" style = "font-family:CURSIVE; color:#990012;">%s</h1>
    """ % (title, title)


################################################################################
def doHTMLTail():

    # always show this link to go back to the main page
    print """
    <p>
    <hr>
    <a href="./recipeBookFINAL.py">Return to main page.</a><br>
    This page was generated at %s.<br>
    Designed by Anyssa Buchanan <br>
    Boston University Class of 2015.
    </body>
    </html>

    """ % time.ctime()

################################################################################
    
# this shows the main page of the Recipe Book application with
#the multiple search options and intro paragraph 
def showMainPage():

   

    print """
    
    <form align="center">

 
    
    <label style = "font-family:CENTURY GOTHIC"> Recipe Type: </label>
    <select name="recipeType" id="recipeSelect" size="1" onChange = "javascript:getRecipeT();">
    <option value="Bread">Bread</option>
    <option value="Brownies">Brownies</option>
    <option value="Cake">Cake</option>
    <option value="Cupcakes">Cupcakes</option>
    <option value="Cookies">Cookies</option>
    <option value="Fruit">Fruit</option>
    <option value="Pastry">Pastry</option>
    <option value="Pie">Pie</option>
    
    
    </select>


    </form>

    <form align="center">

     <label style = "font-family:CENTURY GOTHIC"> Ingredient Type </label>
    <input type= "text" name ="ingredients">
    <input type= "submit" value = "Search">
    </form>
    """

    

    #button to show all the recipes in the database
    print"""

    <form align="center">

    <button type = "submit" name= "showallRecipes" value = "All Recipes" >View All Recipes</button>
    </form>

    """

    #button to start add recipe process 
    print"""

    <form align="center">

    <button type = "submit" name = "addRecipe" value = "Add Recipe"> Add Your Own Recipe</button>
    </form>

    """

    
    #the first 3 pictures at the top of the web app 
    print """

    
    <p align = "center" >

    <img id = "img" src = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/leafapple.jpg"
    width = 300 height = 300>
    
    <p>


    
    """
    #brief paragraph about myself and my hobby 
    print """
    <p align = "center" style = "font-family:CENTURY GOTHIC">

    My name is Anyssa Buchanan and I'm a rising Senior at Boston University.Outside the
    classroom I've developed a passion for exploring restaurants in the diverse Boston
    neighborhoods,trying unique cuisines as well as enhancing my love of baking. I started
    baking when I was in high school but just last year I realized how much I truly enjoyed
    baking along with trying out new ingredients and recipes.Explore the recipes I have baked
    over the past year and try them out for yourself. You won't be disappointed! 
    <p>
    """
    
    #last 3 pics at the bottom of the web app
    print """
    <p align = "center" >
    
    <img id = "img1" src = "http://cs-webapps.bu.edu/cs108/anyssab/myRecipes/cupcaketower.jpg"
    width = 300 height = 300>

    <p>

    """
    
################################################################################

def getAllRecipes():

    
    """
    Middleware function to get all recipes from the recipeBook table.
    Returns the name of the recipe
    """

    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT recipeID, recipeName
    FROM recipeBook
    """

    # execute the query
    cursor.execute(sql)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data


################################################################################
#shows all the recipes in the databases 

def showAllRecipes(data):

    print """
    <h2 style = "font-family:CURSIVE"> My Recipes</h2>

        <p>
    
    <table border=1>
      <tr>
        <td><font size=+1"><b>Recipe Name</b></font></td>
      </tr>
      
    """
    for row in data:

        (recipeID, recipeName) = row

        print """
       <tr>
           <td><a href="?recipeID=%s">%s</a></td>
        </tr>
        """ % (recipeID, recipeName,)


    print """
    </table>
    """

    #count of the recipes
    print "There are %d recipes in my recipe book. <br>" % len(data)



################################################################################   

#this fucntion retrieves the correct recipes by the type of ingredients used
def getRecipeI(ingredients):

    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT recipeID, recipeName
    FROM recipeBook
    WHERE ingredients LIKE %s
    """

    # execute the query
    parameters = ('%' + ingredients + '%', )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data

################################################################################

#this function retrieves the correct recipes by the type of baked good it is ex: brownie, cake 
def getRecipeT(recipeType):

    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT recipeID, recipeName
    FROM recipeBook
    WHERE recipeType = %s
    """

    # execute the query
    parameters = (recipeType, )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data



################################################################################
#this function gets one recipe by its idNum (recipeID)

def getOneRecipe(idNum):


    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT *
    FROM recipeBook
    WHERE recipeID= %s
    """

    # execute the query
    parameters = (int(idNum), )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data

################################################################################


def showRecipe(data):
    """
    Presentation layer function to display the profile page for one user.

    """
    #assign each attribute into a particular record 

    record = data[0]

    recipeID = record [0]
    recipeName = record [1]
    prepTime = record [2]
    cookTime = record[3]
    ingredients = record [4]
    directions = record [5]
    imageURL = record [6]
    recipeType = record [7]

    #format to display each recipe 
    print """
    <h2 align = "center" style = "font-family:CURSIVE" >
    %s </h2>
    <p align = "center">
    %s
    <p>
    <table align = "center">
        <tr>
            <td>Prep Time:</td>
            <td>%s minutes </td>
        </tr>
        <tr>
            <td>Cook Time:</td>
            <td>%s minutes</td>
        </tr>

    </table>
    <p align = "center" >
    %s
    <p> 
    <p align = "center">
    %s
    <p>
    """ % (record[1], record[6], record [2], record [3], record [4], record [5])

    #button to intialize the update recipe
    print"""
    <form>

    <input type = "submit" name = "beginUpdateRecipe" value = "Update Recipe">
    <input type = "hidden" name = "recipeID" value = "%s">
    </form>

    """ % recipeID

################################################################################
#this function displays the add recipe form     
def showAddRecipeForm():

    
    #form contains each of the recipeBooks attributes, name, preptime, cooktime, ingredients, directions
    #a drop down menu is used to choose recipe type
    print """
    
    <h2 style = "font-family:CURSIVE"> Add Your Own Recipe </h2>
    <form>

     
    <label>Recipe Name:</label><br>
    <input type = "text" name="recipeName"><br>
    
    <label>Prep Time:</label><br>
    <input type = "text" name="prepTime"><br>

    <label>Cook Time:</label><br>
    <input type = "text" name="cookTime"><br>

    <label> Ingredients: </label><br>
    <textarea rows="15" cols="50" name="ingredients">
    </textarea>
    
    <br>

    <label> Directions: </label><br>
    <textarea rows= "15" cols ="50" name="directions">
    </textarea><br>
    
    <label> Image URL: </label><br>
    <textarea rows = "8" cols="20" name= "imageURL">
    </textarea><br>

    <label> Type: </label> <br>
    <select name="recipeType" size="1" >
    <option value="Bread">Bread</option>
    <option value="Brownies">Brownies</option>
    <option value="Cake">Cake</option>
    <option value="Cupcakes">Cupcakes</option>
    <option value="Cookies">Cookies</option>
    <option value="Fruit">Fruit</option>
    <option value="Pastry">Pastry</option>
    <option value="Pie">Pie</option>
    
    
    </select>
    
    <input type = "submit" name= "addRecipeForm" value="Submit"> 

    </form>

    """

################################################################################

#this adds a recipe to recipeBook db via insert SQL command
def addRecipe(recipeName, prepTime, cookTime, ingredients,directions, imageURL, recipeType):

    #connect to database
    conn, cursor = getConnectionAndCursor()


    sql2 = """
    SELECT max(recipeID)
    FROM recipeBook
    """
    
    #execute select max id query 
    cursor.execute(sql2)
    (maxID,) = cursor.fetchone()
    nextID = maxID +1

    

    # build SQL to insert a new person in to the minifb
    sql = """
    INSERT INTO recipeBook VALUES
    ( %s, %s, %s,%s, %s, %s, %s,%s)

    """
    
    
    # execute the insert query
    parameters = (nextID, recipeName, prepTime, cookTime, ingredients,directions, imageURL, recipeType)
    cursor.execute(sql, parameters)

    
   #find the row count
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return rowcount


################################################################################

#function to show the user the update profile form.to edit/update prep, cook time and ingredients 
def showUpdateRecipeForm(data):

    record = data[0]

    recipeID = record [0]
    recipeName = record [1]
    prepTime = record [2]
    cookTime = record[3]
    ingredients = record [4]
    directions = record [5]
    imageURL = record [6]
    recipeType = record [7]

    print"""


    <h2 style = "font-family:CURSIVE"> Update Recipe</h2>
    <form>
    <table>
    
    <tr>
    <td> Recipe Name: </td>
    <td> %s </td>
    </tr>


     <tr>
    <td> Prep Time: </td>
    <td><input type = "text" name="prepTime" value = "%s"></td>
    </tr>

    <tr>
    <td> Cook Time: </td>
    <td><input type = "text" name="cookTime" value = "%s"></td>
    </tr>

    <tr>
    <td> Ingredients: </td>
    <td> %s </td>
    </tr>

    <tr>
    <td> Directions: </td>
    <td> %s </td>

    <tr>
    <td> Image </td>
    <td> %s </td>
    </tr>

    <tr>
    <td> Recipe Type </td>
    <td> %s </td>
    </tr>

    <input type = "submit" name= "completeUpdateRecipe" value="Update Recipe">
    <input type = "hidden" name = "recipeID" value = "%s">

    
    </table>
    </form>

    """ % (record[1], record[2], record[3], record[4], record[5], record[6], record[7], recipeID)



################################################################################

#this function update a recipe via SQL update command
def updateRecipe(recipeID, prepTime, cookTime):

    #connect to database
    conn, cursor = getConnectionAndCursor()

    #sql command to update profiles
    sql = """
    UPDATE recipeBook
    SET 
    prepTime = %s,
    cookTime = %s
    WHERE recipeID = %s
    """
    
    # execute the insert query
    parameters = (prepTime, cookTime, recipeID)
    cursor.execute(sql, parameters)

    
   #find the row count
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    cursor.close()
    conn.close()
    
    return rowcount

################################################################################
   
if __name__ == "__main__":


    doHTMLHead("My Recipe Book")
    #showMainPage()
    
    # get form field data
    form = cgi.FieldStorage()

   


    #start update recipe process

    if "beginUpdateRecipe" in form:

        recipeID = form["recipeID"].value
        data = getOneRecipe(recipeID)
        showUpdateRecipeForm(data)

    #step 2 in update recipe process, unpack variables

    elif "completeUpdateRecipe" in form:

        recipeID = form["recipeID"].value
        prepTime = form["prepTime"].value
        cookTime = form["cookTime"].value

        #call middleware function to do update the database

        rowcount = updateRecipe(recipeID, prepTime, cookTime)

        
        #count updated rows
        if rowcount == 1:
            print "%d row was updated.<p>" % rowcount

    #add recipe, unpack variables, 

    elif "addRecipeForm" in form:

        recipeName = form ["recipeName"].value
        prepTime = form["prepTime"].value
        cookTime = form["cookTime"].value
        ingredients = form["ingredients"].value
        directions = form["directions"].value
        imageURL = form["imageURL"].value
        recipeType = form["recipeType"].value


        #use html to format 3 of the variables to the correct display format when they are displayed on the web app
        ingredients = """<h2 align ="center"> Ingredients </h2> <p align = "center"> """ + ingredients.replace("\n", "<br>") + """<p>"""
        directions = """<h2 align ="center"> Directions </h2> <p align = "center"> """ + directions.replace("\n", "<br>") + """<p>"""
        imageURL = """ <p align= "center">""" + """<img src = " """ + imageURL + """ "width= 300 height = 300 > <p> """
        

        rowcount = addRecipe(recipeName, prepTime, cookTime, ingredients,directions, imageURL, recipeType)

        #count updated rows
        if rowcount == 1:
            print "%d row was added.<p>" % rowcount

       
     #unpack recipe id to find corresponding recipe           
    elif "recipeID" in form:

        recipeID= form["recipeID"].value
        data = getOneRecipe(recipeID)
        showRecipe(data)
        
        
            
    #search recipes by type of recipe 
    elif "recipeType" in form:

        recipeType = form["recipeType"].value
        data = getRecipeT(recipeType)
        showAllRecipes(data)

    #search recipes by ingredients 

    elif "ingredients" in form:

        ingredients = form["ingredients"].value
        data = getRecipeI(ingredients)
        showAllRecipes(data)

    #show all the recipes in the db 
    elif "showallRecipes" in form:

        data = getAllRecipes()
        showAllRecipes(data)

    #add your own recipe 
    elif "addRecipe" in form:
        showAddRecipeForm()
        
    else:

        showMainPage()
        
    
        

    doHTMLTail()


