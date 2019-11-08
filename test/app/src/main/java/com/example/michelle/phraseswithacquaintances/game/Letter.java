package com.example.michelle.phraseswithacquaintances.game;

public class Letter {

	private String letter;
	private int pointVal;
	
	public Letter (char tileLetter, int point){
		letter = "";
		letter += tileLetter;
		pointVal = point;
	}
	
	public boolean equals(Letter other){
		if (letter.equals(other.getLetter())){
			return true;
		}
		return false;
	}
	
	public String getLetter(){
		return letter;
	}
	
	public int getPoint(){
		return pointVal;
	}
	
	public void setLetter(char tileLetter, int point){
		letter = "";
		letter += tileLetter;
		pointVal = point;
	}

	public boolean isEmpty(){
		if(pointVal==0){
			return true;
		}else{return false;}
	}
	
	public String toString(){
		String a = "";
		a += letter;
		return a;
	}
}