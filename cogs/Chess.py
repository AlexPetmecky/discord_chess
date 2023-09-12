import discord
#from cairocffi import cairo
from discord.ext import commands
import chess
import chess.svg

import io
from PIL import Image
class Buttons(discord.ui.View):
    buttonTypes = [
        {
            "label":"clickmeeeee",
            "style":discord.ButtonStyle.blurple,
            "interactionResponse":"res"


        }
    ]


    def __init__(self,*,timeout=180,component):
        super().__init__(timeout=timeout)
        self.component=component
        print("Component: "+str(component))

    #@discord.ui.button(label=buttonTypes[self.component]["label"], style=buttonTypes[self.component]["style"])
    #async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
    #    await interaction.response.send_message("You clicked me1")


    @discord.ui.button(label="Join Game",style=discord.ButtonStyle.blurple)
    async def startChess(self,interaction:discord.Interaction , button:discord.ui.Button):

        #Chess.addPlayer(str(interaction.user))
        print("Message Content: "+interaction.message.content)
        originSender = interaction.message.content.split()[0]
        #print(originSender)
        newUser = str(interaction.user)
        print("NEW USER: "+newUser)
        gameState = Chess.add_player(originSender=originSender,newPlayer=newUser)
        #gameState holds either false or a chessGame object
        if gameState:
            await interaction.response.send_message(str(interaction.user) +" has joined the game")
            await Chess.activate_game(gameState)#b/c gamestate is holding a chessGame obj

        else:
            await interaction.response.send_message("Error, this game cannot be joined")


class chessGame():
    player1=None
    player2=None
    context=None
    client =None

    def __init__(self,initplayer,context,client):
        self.player1 =str(initplayer)
        self.board = chess.Board()
        self.context = context
        self.client = client

    def setPlayer2(self,player):
        if self.player1 == str(player):
            return "Already in this game"
        else:
            self.player2 = str(player)
            return "startgame"


    def get_moves(self):
        moves =  self.board.legal_moves
        moveList = []
        for move in moves:
            moveList.append(move.uci())
        return moveList

    def play_move(self,move):
        #mfu = chess.Move.from_uci(move)
        #print("turn: "+str(self.board.turn))
        #self.board.push(move.fromuci())
        self.board.push(chess.Move.from_uci(move))
        #print("turn: " + str(self.board.turn))
        return self.game_end_check()


    def game_end_check(self):
        if self.board.is_checkmate():
            return {"msg":"win"}

        if self.board.is_stalemate():
            return {"msg":"stalemate"}

        return {"msg":"cont"}


    def make_move(self):
        pass

    def generate_embed(self,c):
        if c == "w":
            title = "Chess Board "+str(self.player1)+"'s turn"
            description = str(self.board) + "\n available moves: "+ str(self.get_moves())
        else:
            title = "Chess Board " + str(self.player2) + "'s turn"
            description = str(self.board) + "\n available moves: " + str(self.get_moves())
        embed = discord.Embed(title=title,description=description)
        return embed

    def generate_win_embed(self,user):
        desc = user+" has won the game!"
        embed = discord.Embed(title="Winner!",description=desc)
        return embed
    def generate_stalemate_embed(self):
        embed = discord.Embed(title="Stalemate!",description="The game ends in a tie")
        return embed


    def check(self,m):
        print(m.author)
    def checkMsg(self,color,msg):
        #print("Color: "+str(color))
        #print("msg: "+str(msg))
        if color == 'w':
            username = msg.guild.get_member(msg.author.id)
            print(username)
            if str(username) == self.player1:

                if msg.content == "quit":
                    return {"msg":"quit"}

                if msg.content in self.get_moves():
                    res = self.play_move(msg.content)
                    if res["msg"] == "win":
                        return {"msg":"win","notes":str(username)}
                    if res["msg"] == "stalemate":
                        return {"msg": "tie"}
                    return {"msg":"played"}
                else:
                    return {"msg":"invalidMove"}
            else:
                #this player cannot play
                print
                return {"msg":"wronguser","notes":self.player1}
        else:
            #color ==" b"
            username = msg.guild.get_member(msg.author.id)
            if str(username) == self.player2:

                if msg.content == "quit":
                    return {"msg": "quit"}

                if msg.content in self.get_moves():
                    res = self.play_move(msg.content)
                    if res["msg"] == "win":
                        return {"msg":"win","notes":str(username)}
                    if res["msg"] == "stalemate":
                        return {"msg": "tie"}
                    return {"msg":"played"}
                    #return {"msg": "played"}
                else:
                    return{"msg": "invalidMove"}
            else:
                # this player cannot play
                print
                return {"msg": "wronguser", "notes": self.player2}
            pass






class Chess(commands.Cog):
    games = []
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Chess Cog Loaded")

    @commands.command()
    async def startChess(self, ctx):
        newChessGame = chessGame(initplayer=ctx.message.author,context=ctx,client=self.client)
        self.games.append(newChessGame)
        await ctx.send(str(ctx.message.author)+" wants to start a chess game", view=Buttons(component=0))
        await ctx.send("Chess game player 1: "+newChessGame.player1)


    @commands.Cog.listener()
    async def display(self,ctx):
        await ctx.send("GOT HERE")
    @staticmethod
    async def activate_game(game):

        ctx = game.context
        client = game.client
            #await ctx.send(game.board)
        #await ctx.send(embed=game.generate_embed("w"))
            #await ctx.send(file = game.renderBoard())
        #await ctx.send(game.get_moves())
        #game.play_move("g1h3","b")
       # await ctx.send(game.board)
        #await ctx.send(game.get_moves())
        #game.play_move("g8f6","b")
        #await ctx.send(game.board)
        #await ctx.send(game.get_moves())

        turn=2
        await ctx.send(embed=game.generate_embed('w'))
        while True:
            if turn % 2==0:
                #white plays p1
                #await ctx.send(embed=game.generate_embed('w'))
                msg = await client.wait_for("message")
                response = game.checkMsg("w",msg)
                #print(response)
                while response["msg"] == "wronguser":
                    await ctx.send("Wrong user. Waiting for "+response["notes"])
                    msg = await client.wait_for("message")
                    response = game.checkMsg("w",msg)

                while response["msg"] == "invalidMove":
                    await ctx.send("Invalid Move, try again")
                    msg = await client.wait_for("message")
                    response = game.checkMsg("w", msg)


                if response["msg"] == "played":
                    turn += 1
                    await ctx.send(embed=game.generate_embed('b'))
                if response["msg"] == "win":
                    await ctx.send(embed = game.generate_win_embed(response["notes"]))
                    break
                if response["msg"] == "stalemate":
                    await ctx.send(embed=game.generate_stalemate_embed(response["notes"]))
                    break

                if response["msg"] == "quit":
                    await ctx.send("Quitting")
                    break

            else:
                #black plays p2
                #await ctx.send(embed=game.generate_embed('b'))
                msg = await client.wait_for("message")
                response = game.checkMsg("b", msg)

                while response["msg"] == "wronguser":
                    await ctx.send("Wrong user. Waiting for " + response["notes"])
                    msg = await client.wait_for("message")
                    response = game.checkMsg("b", msg)

                while response["msg"] == "invalidMove":
                    await ctx.send("Invalid Move, try again")
                    msg = await client.wait_for("message")
                    response = game.checkMsg("b", msg)

                if response["msg"] == "played":
                    turn += 1
                    await ctx.send(embed=game.generate_embed('w'))
                    #turn += 1
                if response["msg"] == "win":
                    await ctx.send(embed = game.generate_win_embed(response["notes"]))
                    break
                if response["msg"] == "stalemate":
                    await ctx.send(embed=game.generate_stalemate_embed(response["notes"]))
                    break
                if response["msg"] == "quit":
                    await ctx.send("Quitting")
                    break




        #turn=2

        #while True:
        #    game.get_moves()



        #    if turn % 2 == 0:
               #player1 goes

                #turn +=1

        #    else:
                #player2 goes
         #       turn +=1



    @staticmethod
    def add_player(originSender,newPlayer):
        playerSet = False
        #gameToActivate = False
        for game in Chess.games:
            if game.player1 == str(originSender):
                game.setPlayer2(newPlayer)
                playerSet = game
                print("Current game: " + game.player1 + " " + game.player2)
                break

        return playerSet


    #def addPlayer(self,player):
     #   if player not in self.players:
     #       self.players.append(player)
     #       return str(player)+" has joined chess with "+self.players[0]
     #   else:
     #       return "Already Joined"




async def setup(client):
    await client.add_cog(Chess(client))