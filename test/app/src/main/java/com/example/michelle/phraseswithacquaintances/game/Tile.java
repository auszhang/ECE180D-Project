package com.example.michelle.phraseswithacquaintances.game;


public abstract class Tile {

	private Letter placeHold;
	private boolean isEmpty;

	public Tile(){
		placeHold = new Letter(' ', 0);
		isEmpty = true;
	}

	public boolean isEmpty(){
		return isEmpty;
	}

	public void setLetter(Letter letter){
		placeHold = letter;
		if (placeHold.equals(new Letter(' ', 0))){
			isEmpty = true;
		}else{
			isEmpty = false;
		}
	}

	public Letter getLetter(){
		return placeHold;
	}

	public int getTileScore(){
		return placeHold.getPoint() * getFactor();
	}

	public abstract boolean isWordMult();
	public abstract String getMultiplier();
	public abstract boolean isMult();
	public abstract int getFactor();
	public abstract String toString();

}