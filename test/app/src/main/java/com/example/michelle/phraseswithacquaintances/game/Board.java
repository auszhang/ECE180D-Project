package com.example.michelle.phraseswithacquaintances.game;

import android.content.Context;
import android.util.Log;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Board {

    public Tile[][] board;

    private String[] dictionary;
	private ArrayList<Letter> letterBag;
	private int skipCount;
	private int turnCount;
	private Player[] players;
	private Context mContext;
    private static final int DICTIONARY_LENGTH = 109584;

	private ArrayList<String> wordsPlayed = new ArrayList<String>();
	private ArrayList<Integer> wordStart = new ArrayList<Integer>();
	private ArrayList<Integer> wordEnd = new ArrayList<Integer>();
	private ArrayList<Integer> commonNum = new ArrayList<Integer>();
	private ArrayList<Character> orientation = new ArrayList<Character>();
	private ArrayList<String> letterValues = new ArrayList<String>();
	private int turnScore = 0;
	private int oppScore = 0;
	private String messageReceived = new String();
	private String messageToSend = new String();


	/**
	 * instantiates the players, letter bag, board, turn count, skip count and
	 * dictionary
	 *
	 * also draws letters for each player
	 *
	 * @param playerCount
	 * @throws IOException
	 */
	public Board(int playerCount, Context context) throws IOException {
		mContext = context;
	    board = new Tile[9][9];
		turnCount = 0;
		skipCount = 0;

		letterBag = new ArrayList<Letter>();
		for (int k = 1; k <= 12; k++) {
			if (k <= 1) {
				letterBag.add(new Letter('k', 5));
				letterBag.add(new Letter('j', 8));
				letterBag.add(new Letter('x', 8));
				letterBag.add(new Letter('q', 10));
				letterBag.add(new Letter('z', 10));
			} // still need to add blank letters later
			if (k <= 2) {
				letterBag.add(new Letter('b', 3));
				letterBag.add(new Letter('c', 3));
				letterBag.add(new Letter('m', 3));
				letterBag.add(new Letter('p', 3));
				letterBag.add(new Letter('f', 4));
				letterBag.add(new Letter('h', 4));
				letterBag.add(new Letter('v', 4));
				letterBag.add(new Letter('w', 4));
				letterBag.add(new Letter('y', 4));
			}
			if (k <= 3) {
				letterBag.add(new Letter('g', 2));
			}
			if (k <= 4) {
				letterBag.add(new Letter('l', 1));
				letterBag.add(new Letter('s', 1));
				letterBag.add(new Letter('u', 1));
				letterBag.add(new Letter('d', 2));
			}
			if (k <= 6) {
				letterBag.add(new Letter('n', 1));
				letterBag.add(new Letter('r', 1));
				letterBag.add(new Letter('t', 1));
			}
			if (k <= 8) {
				letterBag.add(new Letter('o', 1));
			}
			if (k <= 9) {
				letterBag.add(new Letter('a', 1));
				letterBag.add(new Letter('i', 1));
			}
			if (k <= 12) {
				letterBag.add(new Letter('e', 1));
			}
		}

		players = new Player[playerCount];
		for (int i = 0; i < playerCount; i++) {
			players[i] = (new Player("Player" + i));
			giveLetters(i);
		}

		InputStream is1, is2, is3, is4;
		try {
            dictionary = new String[DICTIONARY_LENGTH];
			is1 = mContext.getAssets().open("dictionarya_f.txt");
			is2 = mContext.getAssets().open("dictionaryg_m.txt");
			is3 = mContext.getAssets().open("dictionaryn_t.txt");
			is4 = mContext.getAssets().open("dictionaryu_z.txt");
			InputStreamReader in = new InputStreamReader(is1);
			BufferedReader bf = new BufferedReader(in);
			int counter = 0;
			String line = "";
			while((line = bf.readLine())!=null){
			    dictionary[counter]=line;
			    counter++;
            }
            in = new InputStreamReader(is2);
			bf = new BufferedReader(in);
            while((line = bf.readLine())!=null){
                dictionary[counter]=line;
                counter++;
            }
            in = new InputStreamReader(is3);
            bf = new BufferedReader(in);
            while((line = bf.readLine())!=null){
                dictionary[counter]=line;
                counter++;
            }
            in = new InputStreamReader(is4);
            bf = new BufferedReader(in);
            while((line = bf.readLine())!=null){
                dictionary[counter]=line;
                counter++;
            }
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

    /**
     * generates message to transmit over Bluetooth
     * @return message
     */
    public String generateMessage() {
        String a = new String();
        for(int i = 0; i < wordsPlayed.size(); i++) {
            System.out.println(wordsPlayed.get(i));
            System.out.println(letterValues.get(i));
        }
        for(int i = 0; i < wordsPlayed.size(); i++) {
            a += orientation.get(i);
            a += Integer.toString(commonNum.get(i));
            a += Integer.toString(wordStart.get(i));
            a += Integer.toString(wordEnd.get(i));
            for(int j = 0; j < wordsPlayed.get(i).length(); j++) {
                a += wordsPlayed.get(i).charAt(j);
                a += letterValues.get(i).charAt(j);
            }
            a += '!';
        }
        a += '@';
        a += Integer.toString(turnScore);
        return a;
    }

    /**
     * decodes received message from Bluetooth
     * @param receivedMessage
     */
    public void decodeMessage(String receivedMessage) {
        for(int i = 0; i < receivedMessage.length(); i++) {
            if(receivedMessage.charAt(i) == 'v') {
                i++;
                int commNum = Character.getNumericValue(receivedMessage.charAt(i));
                i++;
                int wStart = Character.getNumericValue(receivedMessage.charAt(i));
                i++;
                int wEnd = Character.getNumericValue(receivedMessage.charAt(i));
                i++;
                while(receivedMessage.charAt(i) != '!') {
                    //if(wStart > wEnd) break;
                    char letter = receivedMessage.charAt(i);
                    i++;
                    int point = Character.getNumericValue(receivedMessage.charAt(i));
                    i++;
                    board[wStart][commNum].setLetter(new Letter(letter,point));
                    wStart++;
                }
            }
            else if(receivedMessage.charAt(i) == 'h'){
                i++;
                int commNum = Character.getNumericValue(receivedMessage.charAt(i));
                System.out.println(commNum);
                i++;
                int wStart = Character.getNumericValue(receivedMessage.charAt(i));
                System.out.println(wStart);
                i++;
                int wEnd = Character.getNumericValue(receivedMessage.charAt(i));
                System.out.println(wEnd);
                i++;
                while(receivedMessage.charAt(i) != '!') {
                    //if(wStart > wEnd) break;
                    char letter = receivedMessage.charAt(i);
                    i++;
                    int point = Character.getNumericValue(receivedMessage.charAt(i));
                    i++;
                    board[commNum][wStart].setLetter(new Letter(letter,point));
                    wStart++;
                }
            }
            else if(receivedMessage.charAt(i) == '@') {
                i++;
                oppScore += Integer.parseInt(receivedMessage.substring(i));
                turnCount++;
                return;
            }
            else return;
        }
    }

    /**
     * if word is playable, plays word, then counts and adds score, then
     * increments turn counter
     *
     * @param word
     * @param rowFrom exclusive
     * @param colFrom exclusive
     * @param rowTo inclusive
     * @param colTo inclusive
     */
    public boolean playWord(List<Letter> word, int rowFrom, int colFrom, int rowTo, int colTo) {
        boolean isValid = true;
        System.out.println(wordToString(word));
        if(!isHorizontal(rowFrom,colFrom,rowTo,colTo)) {
            int col = colFrom;
        }
        if (!isValidWord(wordToString(word))) {
            isValid = false;
            return isValid;
        }
        if (!isHorizontal(rowFrom, colFrom, rowTo, colTo)) {
            orientation.add('v');
            wordStart.add(rowFrom);
            wordEnd.add(rowTo);
            commonNum.add(colFrom);
            String points = new String();
            for (int i = rowFrom, index = 0; i < rowTo + 1 && index < word.size(); i++) {
                board[i][colFrom].setLetter(word.get(index));
                int c = board[i][colFrom].getTileScore();
                points += Integer.toString(c);
                index++;
            }
            letterValues.add(points);
            int addscore = countScore(word, tilesFromIndexes("row", rowFrom, rowTo, colFrom));
            getCurrentPlayer().addPoints(addscore);
            turnScore += addscore;

        } else if (isHorizontal(rowFrom, colFrom, rowTo, colTo)) {
            orientation.add('h');
            wordStart.add(colFrom);
            wordEnd.add(colTo);
            commonNum.add(rowFrom);
            String points = new String();
            System.out.println(word.size());
            for (int i = colFrom, index = 0; i < colTo + 1 && index < word.size(); i++) {
                board[rowFrom][i].setLetter(word.get(index));
                int c = board[rowFrom][i].getTileScore();
                points += Integer.toString(c);
                index++;
            }
            letterValues.add(points);
            int addscore = countScore(word, tilesFromIndexes("col", colFrom, colTo, rowFrom));
            getCurrentPlayer().addPoints(addscore);
            turnScore += addscore;
        }

        return true;
    }

    /**
     * takes in a 2D array, and adds the score of the unique
     * @param inBoard
     */
    public int playWord(Letter[][] inBoard){
        int score = 0;
        int wordMult = 1;
        boolean wordFound = false;
        boolean isHoriz = false;
        boolean isVert = false;
        boolean primHoriz = false;
        boolean primVert = false;
        boolean isWordMult = false;
        boolean isValid = true;
        int wordCount = 1;

        wordsPlayed = new ArrayList<String>();
        wordStart = new ArrayList<Integer>();
        wordEnd = new ArrayList<Integer>();
        commonNum = new ArrayList<Integer>();
        orientation = new ArrayList<Character>();
        messageToSend = new String();
        letterValues = new ArrayList<String>();
        turnScore = 0;

        ArrayList<List<Letter>> wordList = new ArrayList<List<Letter>>();
        ArrayList<Integer> rowsfrom = new ArrayList<Integer>();
        ArrayList<Integer> colsfrom = new ArrayList<Integer>();
        ArrayList<Integer> rowsto = new ArrayList<Integer>();
        ArrayList<Integer> colsto = new ArrayList<Integer>();

        //scan to find where letters placed & determine orientation
        int rowfrom = 0;
        int colfrom = 0;
        int rowto = 0;
        int colto = 0;
        int wstart = 0;
        int wend = 0;

        //find first letter & get coordinates
        for (int row = 0; row < 9; row++){
            for (int col = 0; col < 9; col++){
                if (board[row][col].isEmpty() && !inBoard[row][col].isEmpty() && !wordFound){
                    rowfrom = row;
                    colfrom = col;
                    wordFound = true;
                    break;
                }
            }
        }

        if(!wordFound) {
            isValid = false;
            return 1;
        }
        //determine orientation
        if(rowfrom < 8) {
            if(!board[rowfrom+1][colfrom].isEmpty() || !inBoard[rowfrom+1][colfrom].isEmpty()) isVert = true;
            System.out.println(10);
        }
        if(rowfrom > 0) {
            if(!board[rowfrom-1][colfrom].isEmpty() || !inBoard[rowfrom-1][colfrom].isEmpty()) isVert = true;
            System.out.println(20);
        }
        if(colfrom < 8) {
            if(!board[rowfrom][colfrom+1].isEmpty() || !inBoard[rowfrom][colfrom+1].isEmpty()) isHoriz = true;
            System.out.println(30);
        }
        if(colfrom > 0) {
            if(!board[rowfrom][colfrom-1].isEmpty() || !inBoard[rowfrom][colfrom-1].isEmpty()) isHoriz = true;
            System.out.println(40);
        }

        //generate word using orientation
        List<Letter> word = new ArrayList<Letter>();

        //if both horizontal and vertical (i.e. first placed tile involved in 2 words), figure out which direction tiles placed & set other to false
        if(isHoriz && isVert) {
            System.out.println(colfrom);
            System.out.println(rowfrom);
            System.out.println("hi");
            if(colfrom < 8) {
                for(int i = colfrom + 1; i < 9; i++) {
                    if(!inBoard[rowfrom][i].isEmpty()) {
                        isVert = false;
                    }
                }
            }
            if(rowfrom < 8) {
                for(int i = rowfrom + 1; i < 9; i++) {
                    if(!inBoard[i][colfrom].isEmpty()) {
                        isHoriz = false;
                    }
                }
            }
            if(!isHoriz && !isVert) return 1;
            if(isHoriz && isVert) isHoriz = false;
        }

        if(isHoriz) {
            int row = rowfrom;
            int col = colfrom;
            while(col < 9 && board[row][col].isEmpty() && !inBoard[row][col].isEmpty()) {
                col++;
            }
            colto = col;
            rowto = rowfrom;
        }
        else if(isVert){
            int row = rowfrom;
            int col = colfrom;
            while(row < 9 && board[row][col].isEmpty() && !inBoard[row][col].isEmpty()) {
                row++;
            }
            colto = colfrom;
            rowto = row;
        }
        else return 1;

        if(isHoriz) {

            wstart = colfrom;
            while(wstart > 0 && !board[rowfrom][wstart-1].isEmpty() && inBoard[rowfrom][wstart-1].isEmpty()) {
                wstart--;
            }
            wend = colfrom + 1;
            while(wend < 9 && (!board[rowfrom][wend].isEmpty() || !inBoard[rowfrom][wend].isEmpty())) {
                wend++;
            }

            for(int i = wstart; i < wend; i++) {
                if(!board[rowfrom][i].isEmpty()) word.add(board[rowfrom][i].getLetter());
                else word.add(inBoard[rowfrom][i]);
            }
        }

        else if(isVert){
            for(int row = rowfrom; row < 8; row++) {
                for(int col = 0; col < 8; col++) {
                    if(board[row][col].isEmpty() && !inBoard[row][col].isEmpty()) {
                        if(col != colfrom) {
                            isValid = false;
                            return 2;
                        }
                    }
                }
            }

            wstart = rowfrom;
            wend = rowfrom+1;
            while(wstart > 0 && (!board[wstart-1][colfrom].isEmpty() || !inBoard[wstart-1][colfrom].isEmpty())) {
                wstart--;
            }
            while(wend < 9 && (!board[wend][colfrom].isEmpty() || !inBoard[wend][colfrom].isEmpty())) {
                Letter a = board[wend][colfrom].getLetter();
                Letter b = inBoard[wend][colfrom];
                System.out.println(a);
                System.out.println(b);
                wend++;
            }

            for(int i = wstart; i < wend; i++) {
                if(!board[i][colfrom].isEmpty()) word.add(board[i][colfrom].getLetter());
                else word.add(inBoard[i][colfrom]);
            }
        }

        else return 1;

        if(turnCount == 0) {
            if(isHoriz) {
                if(rowfrom != 4 || colfrom > 4 || colto <=4) {
                    isValid = false;
                    return 3;
                }
            }
            else {
                if(colfrom != 4 || rowfrom > 4 || rowto <=4) {
                    isValid = false;
                    return 3;
                }
            }
        }

        System.out.println(word);
        wordList.add(word);

        if(isHoriz) {
            rowsfrom.add(rowfrom);
            rowsto.add(rowto);
            colsfrom.add(wstart);
            colsto.add(wend);
            for(int i = wstart; i < wend; i++) {
                if(!inBoard[rowfrom][i].isEmpty()) {
                    List<Letter> extraWord = new ArrayList<Letter>();
                    int rowup = rowfrom;
                    int rowdown = rowfrom;
                    while(rowup > 0 && !board[rowup-1][i].isEmpty()) {
                        rowup--;
                    }
                    while(rowdown < 8 && !board[rowdown+1][i].isEmpty()) {
                        rowup++;
                    }
                    if(rowup != rowfrom || rowdown != rowfrom) {
                        rowsfrom.add(rowup);
                        colsfrom.add(i);
                        rowsto.add(rowdown);
                        colsto.add(i);
                        for(int j = rowup; j <= rowdown; j++) {
                            if(j == rowfrom) extraWord.add(inBoard[j][i]);
                            else extraWord.add(board[j][i].getLetter());
                        }
                        wordList.add(extraWord);
                        System.out.println(wordToString(extraWord));
                    }
                }
            }
        }

        if(isVert) {
            rowsfrom.add(wstart);
            rowsto.add(wend);
            colsfrom.add(colfrom);
            colsto.add(colto);
            for(int i = wstart; i < wend; i++) {
                if(!inBoard[i][colfrom].isEmpty()) {
                    List<Letter> extraWord = new ArrayList<Letter>();
                    int colleft = colfrom;
                    int colright = colfrom;
                    while(colleft > 0 && !board[i][colleft - 1].isEmpty()) {
                        colleft--;
                    }
                    while(colright < 8 && !board[i][colright + 1].isEmpty()) {
                        colright++;
                    }
                    if(colleft != colfrom || colright != colfrom) {
                        rowsfrom.add(i);
                        colsfrom.add(colleft);
                        rowsto.add(i);
                        colsto.add(colright);
                        for(int j = colleft; j < colright + 1; j++) {
                            if(j == colfrom) extraWord.add(inBoard[i][j]);
                            else extraWord.add(board[i][j].getLetter());
                        }
                        wordList.add(extraWord);
                        System.out.println(wordToString(extraWord));
                    }
                }
            }
        }

        for(int i = 0; i < wordList.size(); i++) {
            String a = wordToString(wordList.get(i));
            wordsPlayed.add(a);
            if(!isValidWord(a)) return 4;
        }
        if(!isHoriz) {
            for(int i = 0; i < wordList.size(); i++) {
                playWord(wordList.get(i),rowsfrom.get(i),colsfrom.get(i),rowsto.get(i),colsto.get(i));
            }
        }
        else {
            for(int i = 0; i < wordList.size(); i++) {
                playWord(wordList.get(i),rowsfrom.get(i),colsfrom.get(i),rowsto.get(i),colsto.get(i));
            }
        }

        if(!giveLetters()){
            return 5;
        }
        turnCount++;
        skipCount = 0;
        messageToSend = generateMessage();
        return 0;
    }

    /**
	 * skips player's turn and increments the skip counter
	 */
	public void skipTurn() {
		turnCount++;
		skipCount++;
	}

	/**
	 * prints out the board
	 */
	public void printBoard(){
		for (Tile[] row: board){
			for (Tile col : row){
				System.out.print(col.getLetter());
			}
			System.out.println();
		}
	}

	/**
	 * Set board[x][y] to multiplier tile with given attributes
	 * @param x
	 * @param y
	 * @param multType
	 * @param factor
	 */
	public void setMultiplierTile(int x, int y, String multType, int factor){
		board[x][y] = new MultiplierTile(multType,factor);
	}

	/**
	 * Set board[x][y] to generic tile
	 * @param x
	 * @param y
	 */
	public void setGenericTile(int x, int y){
		board[x][y] = new GenericTile();
	}

	/**
	 * returns true if game should end
	 *
	 * @return true if game should end
	 */
	public boolean endGame() {
		if (skipCount >= 3) {
			return true;
		} else if (letterBag.size() == 0) {
			if(getCurrentPlayer().getLetters()==0){
			    return true;
            }
		}
		return false;
	}

	public void printWord(int index){
		System.out.println(dictionary[index]);
	}

	/**
	 * returns the current player
	 *
	 * @return current player
	 */
	public Player getCurrentPlayer() {
		int tcount;
		tcount = turnCount%players.length;
		return players[tcount];
	}

	/**
	 * Return turn count
	 * @return
	 */
	public int getTurnCount()  {
		return turnCount;
	}

    /**
     *
     * @param turn
     */
	public void setTurnCount(int turn) {turnCount = turn;}

    /**
     * Return message to send
     * @return
     */
	public String getMessageToSend() {return messageToSend;}

    /**
     * Return opponent's score
     * @return
     */
	public int getOppScore() {return oppScore;}

	/**
	 * returns if the word is valid
	 *
	 * @param word
	 * @return validity of word
	 */
	private boolean binary(String word, int first, int last) {
		int mid = (first + last) / 2;
		if (last == first) {
			if (dictionary[first].equals(word)) {
				return true;
			} else {
				return false;
			}
		} else {
			if (dictionary[mid].equals(word)) {
				return true;
			} else if (dictionary[mid].compareTo(word) < 0) {
				return binary(word, mid + 1, last);
			} else if (dictionary[mid].compareTo(word) > 0) {
				return binary(word, first, mid - 1);
			} else {
				return false;
			}
		}
	}

	/**
	 * Wrap method for binary search with helper method binary
	 * @param word
	 */

	private boolean isValidWord(String word){
		return binary (word, 0, dictionary.length - 1);
	}

	/**
	 * counts the score of the word and returns it
	 *
	 * @param word
	 * @return word score
	 */
	private int countScore(List<Letter> word, List<Tile> tile) {
		boolean wordMult = false;
		int factor = 1;
		int score = 0;
		for (int i = 0; i < word.size() && i < tile.size(); i++) {
			if (tile.get(i).getMultiplier().equals("word")) {
				wordMult = true;
				factor = tile.get(i).getFactor();
			}
			if (tile.get(i).getMultiplier().equals("letter")) {
				score += word.get(i).getPoint() * tile.get(i).getFactor();
			} else {
				score += word.get(i).getPoint();
			}
		}
		if (wordMult) {
			score *= factor;
		}
		return score;
	}

	/**
	 * gives letters to current player using getCurrentPlayer()
	 */
	private boolean giveLetters() {
		if (letterBag.size() > 0) {
			int tempIndex;
			while (getCurrentPlayer().getLetters() < 7 && letterBag.size() > 0) {
				tempIndex = (int) (Math.random() * letterBag.size());
				getCurrentPlayer().grabLetter(letterBag.get(tempIndex));
				letterBag.remove(tempIndex);
			}
			return true;
		}else{
		    return false;
        }
	}

	/**
	 * gives letters to indexed player
	 *
	 * @param index
	 */
	private void giveLetters(int index) {
		if (letterBag.size() > 0) {
			int tempIndex;
			while (players[index].getLetters() < 7 && letterBag.size() > 0) {
				tempIndex = (int) (Math.random() * letterBag.size());
				players[index].grabLetter(letterBag.get(tempIndex));
				letterBag.remove(tempIndex);
			}
		}
	}

	/**
	 * returns a word in a string from a list of letters
	 *
	 * @param word
	 * @return word
	 */
	private String wordToString(List<Letter> word) {
		String a = "";
		for (Letter x : word) {
			a += x.getLetter();
		}
		return a;
	}

	/**
	 * Precondition: either colFrom and colTo are equal or rowFrom and rowTo are equal
	 * @param rowFrom
	 * @param colFrom
	 * @param rowTo
	 * @param colTo
	 * @return if it's horizontal
	 */
	private boolean isHorizontal(int rowFrom, int colFrom, int rowTo, int colTo){
		if (colFrom == colTo){
			return false;
		}else{
			return true;
		}
	}

	/**
	 * returns a list of either row tiles or col tiles based on string input.
	 * String should be either "row" or "col", based on which one is CHANGING
	 * constant is the value of the nonchanging row/col
	 *
	 * @param changingRowOrCol
	 * @param from
	 * @param to
	 * @param constant
	 * @return
	 */
	private List<Tile> tilesFromIndexes(String changingRowOrCol, int from, int to, int constant) {
		List<Tile> tiles = new ArrayList<Tile>();
		try {
			if (changingRowOrCol.toLowerCase().equals("row")) {
				for (int i = from; i < to; i++) {
					tiles.add(board[i][constant]);
				}
			} else if (changingRowOrCol.toLowerCase().equals("col")) {
				for (int i = from; i < to; i++) {
					tiles.add(board[constant][i]);
				}
			}
			return tiles;
		} catch (IndexOutOfBoundsException e) {
			return tiles;
		}
	}
}