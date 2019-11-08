package com.example.michelle.phraseswithacquaintances.game;


public class GenericTile extends Tile {

	private final String GENERIC_MULTIPLIER = "";

	public GenericTile(){
		super();
	}

	@Override
	public String getMultiplier(){
		return GENERIC_MULTIPLIER;
	}

	@Override
	public int getFactor(){
		return 1;
	}

	@Override
	public boolean isMult(){
		return false;
	}

	@Override
	public boolean isWordMult(){
		return false;
	}

	@Override
	public String toString() {
		String a = "";
		a += super.getLetter().toString() + "," + 1;
		return a;
	}
}
