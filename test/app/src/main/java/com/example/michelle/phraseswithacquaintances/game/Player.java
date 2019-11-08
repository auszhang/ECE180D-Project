package com.example.michelle.phraseswithacquaintances.game;

import java.util.ArrayList;
import java.util.List;

public class Player {

	private Letter letters[];
	private int points;
	private String name;
	private static final int PLAYER_HAND_SIZE = 7;

	public Player(String n) {
		letters = new Letter[PLAYER_HAND_SIZE];
		name = n;
		points = 0;
	}

	public boolean grabLetter(Letter a){
		if(this.getLetters()==PLAYER_HAND_SIZE){return false;}
		else{
			int i = 0;
			while(i<PLAYER_HAND_SIZE){
				if(letters[i]==null){
					letters[i]=a;
					break;
				}else{i++;}
			}
		}
		return true;
	}
	
	public boolean putLetter(Letter a, int index) {
		if (letters[index]!=null) {return false;}
		else{
			letters[index]=a;
		}
		return true;
	}
	public Letter removeLetter (int index){
		Letter removed = letters[index];
		letters[index] = null;
		return removed;
	}

	public int removeLetter(Letter to_remove){
		int index = 0;
		while(index<PLAYER_HAND_SIZE){
			if(letters[index]!=null && letters[index].getLetter().equals(to_remove.getLetter())){
				letters[index]=null;
				break;
			}else{index++;}
		}
		return index;
	}
	
	public int getLetters(){
		int count = 0;
		for(int i = 0; i<PLAYER_HAND_SIZE;i++){
			if(letters[i]!=null){count++;}
		}
		return count;
	}

	public Letter[] getPlayerHand(){return letters;}
	
	public int getPoints(){
		return points;
	}
	
	public String getName(){
		return name;
	}
	
	public void setName(String n){
		name = n;
	}
	
	public void setLetters(Letter[] x){
		letters = x;
	}
	
	public void setPoints(int p){
		points = p;
	}
	
	public void addPoints(int n){
		points += n;
	}
}
