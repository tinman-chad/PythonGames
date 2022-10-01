import sqlite3
from sqlite3 import Error, Connection, ProgrammingError
from pathlib import Path
from pygame.font import Font
from pygame import Surface
from pygame.key import get_pressed, get_repeat, set_repeat
from pygame.key import key_code
import math
from dataclasses import dataclass

@dataclass
class Score:
    row_num: int = 0
    display_name: str = ''
    score: int = 0

#thought about making this a rest client to save the games to a fastapi service but that would require more security... who cares of you screw things up on your local computer.
class ScoreKeeper:
    '''Did not use sqlAlchemy, just because it is important to remember how to do these things for myself.'''
    def __init__(self, tracking: str, is_multi : bool, db_path: Path, font: Font, fontColor = (0, 0, 0), new_game_text : str = ''):
        self.tracking = tracking
        self.is_multi = is_multi
        self.db_path = db_path
        self.font = font
        self.font_color = fontColor
        self.current_display_name = ''
        self.new_game_text = new_game_text
        self.current_page = 0
        #make sure the talbes are set up for score keeping.
        #yes, I know I should have created a local variable for the clean title, maybe later.
        self.dbExecute(f"CREATE TABLE IF NOT EXISTS Games (GameId integer PRIMARY KEY AUTOINCREMENT, Title text NOT NULL)")
        self.dbExecute(f"CREATE TABLE IF NOT EXISTS Scores (ScoreId integer PRIMARY KEY AUTOINCREMENT, GameId integer NOT NULL, UserName text NOT NULL, Score integer NOT NULL)")
        self.game_id = self.dbExecute(f"Select GameId from Games where Title = '{self.scrubValue(self.tracking)}'", True)
        if self.game_id == 0:
            self.dbExecute(f"INSERT INTO Games (Title) values ('{self.scrubValue(self.tracking)}')")
            self.game_id = self.dbExecute(f"Select GameId from Games where Title = '{self.scrubValue(self.tracking)}'", True)

    def dbConnect(self) -> Connection:
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
        except Error as ex:
            print(f'Could not connect to db: {ex}')

        return conn

    def dbExecute(self, sql : str, hasValue: bool = False):
        '''Execute a sql statement and return the first row's first column's value... think get_scalar, but lazier.'''
        try:
            with self.dbConnect() as conn:
                if not hasValue:
                    conn.execute(sql)
                    conn.commit()
                    return None
                c = conn.cursor()
                res = c.execute(sql)
                row = res.fetchone()
                c.close()
                if row:
                    return row[0]
                return 0
        except ProgrammingError:
            return None
        except Error as ex:
            print(f'Could execute sql {self.db_path}, {ex}.')
        
    def scrubValue(self, value: str) -> str:
        '''A method for scrubbing for sql injection related things in sql values used.'''
        return value.replace("'", "''").replace(';', ' ')
    
    def getHighestScore(self) -> int:
        '''Just returns the highest score (no name, for in game hud display)'''
        with self.dbConnect() as conn:
            c = conn.cursor()
            try:
                c.execute(f"select MAX(Score) from Scores where GameId = (Select GameId from Games where Title = ?)", (self.tracking,))
                val = c.fetchone()
                c.close()
                if val:
                    return val[0]
                return 0
            except Error as ex:
                print(f'Could not retrieve high score: {ex}')

    def saveHighScore(self, UserName: str, Score: int) -> int:
        '''returns the highest score (may not be the score passed in.'''
        self.dbExecute(f"Insert into Scores (GameId, UserName, Score) values ({self.game_id}, '{self.scrubValue(UserName)}', {Score});")
        return self.getHighestScore()

    def getHighScoreList(self, page_num : int = 0, page_size : int = 5, score_to_find : int = -1) -> list[Score]: #is it strange I want to apply caching here??? A dict with each page's scores on it... but then reset them if a new score is saved
        '''Returns a dictionary of score to username for display by page size.  Dictionary is not sorted, query makes sure the page is the correct, so get the keys and sort them and loop through the collection. Page size is 0 based.'''
        if page_num < 0:
            raise Error("Pages start at zero.")
        strOffset = ''
        offset = page_num * page_size
        if score_to_find > 0:
            placement = self.dbExecute(f'Select count(ScoreId) as cnt from Scores where GameId = {self.game_id} and score >= {score_to_find}', True)
            if placement > page_size: #what page is it on???
                page_num = (math.ceil(float(placement)/float(page_size)) - 1)
                self.current_page = page_num
                offset = page_num * page_size #if there is a decimal just round up to the next page where the score is.  But page numbers start at zero so minus 1

        if offset > 0:
            strOffset = f' offset {offset}'
        UserNameIdx = 0
        ScoreIdx = 1
        sql = f'select Username, Score from Scores where GameId = {self.game_id} order by score desc limit {page_size}{strOffset}'
        ret = []
        try:
            with self.dbConnect() as conn:
                c = conn.cursor()
                res = c.execute(sql)
                rows = res.fetchall()
                i = 0
                for row in rows:
                    i += 1
                    s = Score(display_name=row[UserNameIdx], score=row[ScoreIdx], row_num=offset+i)
                    ret.append(s)
                c.close()
        except ProgrammingError:
            return None
        except Error as ex:
            print(f'Could execute sql {self.db_path}, {ex}.')
        return ret

    def resetHighScoreList(self):
        '''Dopamine required but too hard to get?  Try removing the competition.'''
        self.dbExecute(f'Delete from Scores where GameId = {self.game_id}; VACUUM;')
    
    def draw_input(self, screen: Surface, current_score: int = 0, key_pressed: str = ''):
        #using the internal display name for remembering the current player so they can just hit enter to save the score.
        if key_pressed == '\b':
            self.current_display_name = self.current_display_name[:-1]
        else:
            self.current_display_name += key_pressed

        if key_pressed == '\r':
            highestScore = self.saveHighScore(self.current_display_name, current_score)
            self.draw_scores(screen, current_score)

        thisScore = self.font.render(f"Your High Score: {current_score}", 1, self.font_color)
        lineHeight = thisScore.get_height()/2
        line_left = (screen.get_width()/2)-(thisScore.get_width()/2)
        padding_y = 20
        current_line_top = screen.get_height() - (screen.get_height() - 200)
        screen.blit(thisScore, (line_left, current_line_top))
        current_line_top -= (padding_y + lineHeight)

        userName = self.font.render(f'Name: {self.current_display_name}', 1, self.font_color)
        screen.blit(userName, (line_left, current_line_top))

    def draw_scores(self, screen: Surface, page: int = 0, current_score: int = -1):
        padding_y = 20
        max_scores = 5
        score_start = self.font.render('HIGH SCORES', 1, self.font_color)
        lineHeight = score_start.get_height()
        current_line_top = screen.get_height() - (screen.get_height() - 200)
        line_left = (screen.get_width()/2)-(score_start.get_width()/2)
        screen.blit(score_start, (line_left, current_line_top))
        current_line_top += (padding_y + lineHeight)
        self.current_page += page
        if page != 0:
            current_score = -1
            print(f'PAGE: {self.current_page}')
        for score in self.getHighScoreList(page_num=self.current_page, page_size=max_scores, score_to_find=current_score):
            thisScore = self.font.render(str(score.row_num) + ". " + str(score.display_name) + ": " + str(score.score), 1, self.font_color)
            screen.blit(thisScore, (line_left, current_line_top))
            current_line_top += (padding_y + lineHeight)

        if self.new_game_text != '':
            current_line_top += (padding_y + lineHeight) #give leadedboard space.
            new_game = self.font.render(self.new_game_text, 1, self.font_color)
            screen.blit(new_game, ((screen.get_width()/2)-(new_game.get_width()/2), current_line_top))