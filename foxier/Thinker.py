"""
This module with handle all checks:
    What letters are in hand
    What letters are on the board
    What target spots (Triple word scores) are
"""
import prepare_requestWWF
import makerequest
import time
import logging
from solver import findWordPlays, WordOrientation


class gameManager(object):
    """docstring for gameManager"""
    def __init__(self, accessTokenManager):
        super().__init__()
        self.getToken = accessTokenManager.getAccessToken
        self.client = makerequest.getClient()
        self.__ZyngaID = int()

    def getZyngaID(self):
        """
        Get Zynga ID of player.

        Needs 2 games to be present to find ID by matching
        """
        if not self.__ZyngaID:
            weekAgo = int(time.time() - 604800)
            gameIndx = self.getGameIndex(weekAgo)
            if len(gameIndx.games) < 2:
                raise Exception('Need more than 2 games to find ID')
            targetSet = set(gameIndx.games[0].usersById.keys())
            for game in gameIndx.games:
                targetSet = targetSet & set(game.usersById.keys())
                if len(targetSet) == 1:
                    break
            if len(targetSet) != 1:
                raise Exception('Unexpected IDs')
            self.__ZyngaID = targetSet.pop()  # Do I need exception above?
            logging.info('ID for user is: %s', self.__ZyngaID)
        return self.__ZyngaID

    # Methods
    def foxPatrol(self):
        """
        Returns int Game ID of target game

        Currently grabs first active game
        """
        gameIndx = self.getGameIndex(time.time() - 604800)
        gameID = int()
        for game in gameIndx.games:
            logging.info('Over Value: %s and type is %s', game.over, type(game.over))
            if game.currentMoveUserId == self.getZyngaID() and not game.over:
                logging.info('Game ID patrolled: %s', game.id)
                gameID = game.id
                break
        if gameID:
            self.foxAttack(gameID)
        # Need to handle case of no games?
        # Maybe make recursive calls that look futher and further back in time

    def foxAttack(self, gameID): # A bit hacky, optimize
        """
        Make a move in a game
        """
        resultState = object()  # some empty game state object
        state = self.getGameState(gameID)
        rack = state.racks[self.getZyngaID()]
        movesList = findWordPlays(state.board, rack)
        orderedListByPointValue = movesList.sort(
            key=lambda attempt: attempt[2])
        orderedWordAttempts = [attempt[1] for attempt in orderedListByPointValue]
        invalidWords = self.client.dictionaryLookup(
            self.getToken(), orderedWordAttempts)
        validWords = self.setSymmDifferenceOfList(
            invalidWords, orderedWordAttempts)
        for i in range(0, len(orderedWordAttempts)):
            if orderedWordAttempts[i] in validWords:
                moveSub = orderedListByPointValue[i][0]
                resultState = self.client.makeMove(
                    self.getToken(), state, moveSub)
                break
        if not resultState:
              pass #SWAP play is needed

    # Helpers
    def getGameIndex(self, secondOffset=0):
        """
        Return index of games.
        If SecondOffset is non-zero
            Then games up to CurrTime - SecondOffset will be return
        """
        logging.info('Getting Game index')
        if not secondOffset:
            games = self.client.getGameIndex(self.getToken())
            return games
        timeInPast = int(time.time() - secondOffset)
        games = self.client.getGamesWithUpdates(
            self.getToken(), timeInPast)
        logging.debug('looked %s seconds in the past', timeInPast)
        return games

    def getGameState(self, gameID):
        state = self.client.getGameState(self.getToken(), gameID)
        # Handle invalid game state and errors that are returned
        logging.info('Game State for ID %s retrieved', gameID)
        return state

    def makeMove(self, gameState, move):
        newState = self.client.makeMove(self.getToken(), gameState, move)
        return newState

    def setSymmDifferenceOfList(list1, list2):
        """
        Takes two list and returns a set of their symm differences
        """
        set1 = set(list1)
        set2 = set(list2)
        symmdiff = set1 ^ set2
        return symmdiff


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', filename='MyFirstLog.log', filemode='w', level=logging.INFO)
    accTokMng = prepare_requestWWF.accessFactory('FBlogin@fake.com', 'password')
    # Remove in production
    token = ''
    with open('temp.txt', 'r') as f:
        token = f.read()
    accTokMng.AccTokenJSON = accTokMng.parseToken(token)
    # Remove in production
    gM = gameManager(accTokMng)
    #get game indx
    #week ago is -604800 seconds
    gameID = gM.foxPatrol()
    #View meta data for games and see which are activiley my turn
