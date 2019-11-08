package com.example.michelle.phraseswithacquaintances.game;


public class MultiplierTile extends Tile {

	private String multiplier;
	private final int FACTOR;

	/**
	 * Multiplier in form "word/letter" and multiplying FACTOR
	 * for example, new MultiplierTile("word", 3) would be a 3x word score
	 * @param multType, inFactor
	 */
	public MultiplierTile(String multType, int inFactor){
		multiplier = multType;
		FACTOR = inFactor;
	}

	@Override
	public boolean isWordMult(){
		if (multiplier.toLowerCase().equals("word")){
			return true;
		}
		return false;
	}

	@Override
	public String getMultiplier() {
		return multiplier;
	}

	@Override
	public int getFactor(){
		if (multiplier.toLowerCase().equals("word")){
			return 1;
		}
		else{
			return FACTOR;
		}
	}

	@Override
	public boolean isMult(){
		return true;
	}

	@Override
	public String toString(){
		String a = "";
		a += super.getLetter().toString() + "," + multiplier;
		return a;
	}
}

