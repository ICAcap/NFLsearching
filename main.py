# import libraries here
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import mysql.connector
import requests
import os
from resources import player
from dotenv import load_dotenv

load_dotenv()

# instances initialization
app = FastAPI()
player_resource = player.PlayerResource()

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
# define MySQL connection parameters
db_config = {
    "host": "c6156-nfl-searching-query-microservice-db.ckoq7q2zprcp.us-east-2.rds.amazonaws.com",
    "user": "tw6156",
    "password": "linguine_falafel_pita",
    "database": "dbNFLstat",
}

"""
GET operations here
"""

@app.get("/")
async def root():
    return {"message": "From Tangwen Zhu (tz2570), microservice - NFL searching, work in progress"}

"""
show the player game stats information based on the player_id, and other optional information: week, and (season) year
as an html table webpage (if the connnection to the database is fine and the data can be found)
https://fastapi.tiangolo.com/advanced/custom-response/#return-an-htmlresponse-directly
"""
@app.get("/v1/players/{player_id}/stat", response_class = HTMLResponse)
async def player_stat_by_id(player_id: str, week: int=None, season: int=None):

    print(f"You are looking at player: {player_id}, more info below:")

    try:
        # connect to the MySQL server
        connection = mysql.connector.connect(**db_config)
        # create a cousor object for query
        # https://www.geeksforgeeks.org/python-sqlite-cursor-object/#
        cursor = connection.cursor()

        # define sql query here
        query = f"SELECT * FROM player_stat WHERE player_id = '{player_id}'"

        # if the year and week parameter are valid
        if week != None:
            query += f" AND week = '{week}'"

        if season != None:
            query += f" AND season = '{season}'"

        # execute query
        cursor.execute(query)

        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchall.html
        rows = cursor.fetchall() # get the result rows

        # shut down cursor and connection
        cursor.close()
        connection.close()

        # process the rows for the webpage result presentation

        # case 1 -  the player stat data doesn't exist:
        if len(rows) == 0:
            message = f"Sorry, no data found for this player under player_id : {player_id}, under week: '{week}', and season: '{season}', please check the inputs"
            return Response(content=message, media_type="text/plain", status_code=200)

        # case 2 - the player stat data exists
        else:
            # construct an HTML table
            message = "<html><body>"
            message += "Here is the performance data you requested:"
            message += "<table border='1'>"

            # header row
            message += "<tr>"
            for column_name in cursor.column_names:
                message += f"<th>{column_name}</th>"
            message += "</tr>"

            # data rows
            for row in rows:
                message += "<tr>"
                for value in row:
                    message += f"<td>{value}</td>"
                message += "</tr>"
            message += "</table></body></html>"

        return HTMLResponse(content=message, status_code=200)

    # connection error
    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

"""
Show the basic information of a player by the player_id
"""
@app.get("/players/{player_id}", response_class = HTMLResponse)
async def player_by_id(player_id: str):
    try:
        player = player_resource.get_player_by_id(player_id)

        # the player is found in the table
        if player:
            player = list(player[0])
            # print(player) # debugging purpose
            message = "<html><body>"
            message += "Here is the player basic information you requested:"

            columns_name = list(player_resource.player_basic.columns.keys())
            # print(columns_name) # debugging purpose

            player_zip = zip(columns_name, player)
            for tup in player_zip:
                message += f"<h3>{tup[0]}:</h3> {tup[1]}"

            message += "</html></body>"

            rsp = Response(content=message)
            return rsp

        else:
            rsp = Response(content="Sorry, the player you are looking for is not in the database.", media_type="text/plain")
            return rsp

    except Exception as e:
        # other exceptions if encounterd
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

#external_api_call
@app.get("/players/{player_id}/news", response_class=HTMLResponse)
async def get_news_by_id(player_id: str):
    api_key = os.getenv("API_KEY")
    url = f"https://api.sportsdata.io/v3/nfl/scores/json/NewsByPlayerID/{player_id}?key={api_key}"

    try:
        rsp = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if rsp.status_code == 200:
            # Return the content of the response
            return HTMLResponse(content=rsp.text, status_code=200)
        else:
            return Response(content="Sorry, the player you are looking for is not in the database.", media_type="text/plain", status_code=rsp.status_code)

    except requests.exceptions.RequestException as e:
        # Create a FastAPI response object with an error message
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)



"""
add a new player to the player_basic table on database, make use of the player base model in resource
"""
@app.post("/players")
async def add_player(player: player.PlayerModel):
    try:
        # add player to the database
        result = player_resource.add_player(player)
        player_id = player.player_id

        # check if the player was successfully added by showing the basic info page
        # https://fastapi.tiangolo.com/async/
        GET_response = await player_by_id(player_id)
        return GET_response

    except Exception as e:
        # other exception if encountered
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)



"""
a function to modify a player basic information from the player_basic table by player_id
"""
@app.put("/players/modify/{player_id}")
async def modify_player(player: player.PlayerModel, player_id):
    try:
        # modify the data of the player
        player_resource.modify_player(player, player_id)

        # show the modified infos using the GET operation
        # https://fastapi.tiangolo.com/async/
        GET_response = await player_by_id(player_id)
        return GET_response

    except Exception as e:
        # other exception if encountered
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)


"""
a function to delete a player from the player_basic table by player_id
"""
@app.delete("/players")
async def delete_player(player_id: str):
    try:
        # delete a player by the id
        player_resource.delete_player(player_id)

        message = "Done."
        return Response(content=message, media_type="text/plain", status_code=200)

    except Exception as e:
        # other exception if encountered
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) # local machine
    #

