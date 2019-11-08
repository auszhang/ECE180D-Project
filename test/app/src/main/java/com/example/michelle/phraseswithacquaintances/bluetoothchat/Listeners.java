package com.example.michelle.phraseswithacquaintances.bluetoothchat;

import android.content.ClipData;
import android.content.ClipDescription;
import android.graphics.Color;
import android.util.Log;
import android.view.DragEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

import com.example.michelle.phraseswithacquaintances.game.*;

/**
 * Click and drag listeners
 */
public class Listeners {

    /**
     * Listener for end turn button
     */
    public static final class MyEndClickListener implements View.OnClickListener {



        private MainActivity mainActivity;
        private TextView turnCount;
        private TextView score;

        public MyEndClickListener(MainActivity m){
            mainActivity=m;
            turnCount = (TextView) mainActivity.findViewById(R.id.turnCount);
            score = (TextView) mainActivity.findViewById(R.id.score);
        }
        public void onClick(View v){
            Letter[][] l=Translator.translateViewToLetter(mainActivity.blockBoard);

            //Print current board, for debug purposes
            String mess = "";
            for(int m = 0; m<9;m++){
                for(int n = 0;n<9;n++){
                    mess+=l[m][n].getLetter();
                }
                mess+="\n";
            }
            Log.i("Player",mess);

            //Play the word
            int message_id = mainActivity.game.playWord(l);
            if(message_id==0 || message_id==5){ //If turn is a valid move
                //Turn off listeners for blocks on board
                int z,w;
                for(z=0;z<mainActivity.blockBoard.length;z++){
                    for(w=0;w<mainActivity.blockBoard.length;w++){
                        if(mainActivity.blockBoard[z][w]!=null){
                            mainActivity.blockBoard[z][w].setOnLongClickListener(null);
                        }
                    }
                }

                if(message_id==5){mainActivity.toast5.show();}
                else{
                    //Refresh player hand
                    Letter[] hand=mainActivity.game.getCurrentPlayer().getPlayerHand();
                    int i;
                    int[] drawables=Translator.translateLetterToDrawable(hand);
                    for(i=0;i<drawables.length;i++){
                        if(mainActivity.playerHand[i]==null){
                            ImageView block = (ImageView) LayoutInflater.from(mainActivity).inflate(R.layout.block,mainActivity.parent,false);
                            block.setX((mainActivity.tileWidth * i)*mainActivity.displayMetrics.density);
                            block.setY(mainActivity.bottom*mainActivity.displayMetrics.density);
                            block.setImageResource(drawables[i]);
                            block.setTag(mainActivity.IMAGEVIEW_TAG+i);
                            block.setId(drawables[i]);
                            block.setOnLongClickListener(new Listeners.MyLongClickListener(mainActivity));
                            mainActivity.parent.addView(block);
                            mainActivity.playerHand[i]=block;
                            mainActivity.playerHand[i].setId(drawables[i]);
                            Log.i("PlayerHand: ","Id: "+drawables[i]);
                        }
                    }
                }

                String message = mainActivity.game.getMessageToSend();
                mainActivity.fragment.sendMessage(message);

            }
            else{
                Log.i("Game", "Invalid move");
                if(message_id==1){mainActivity.toast1.show();}
                else if(message_id==2){mainActivity.toast2.show();}
                else if(message_id==3){mainActivity.toast3.show();}
                else if(message_id==4){mainActivity.toast4.show();}
            }
            turnCount.setText("TURN: "+mainActivity.game.getTurnCount());
            score.setText("YOUR SCORE: "+mainActivity.game.getCurrentPlayer().getPoints());

            if(mainActivity.game.endGame()) {
                Log.i("Game", "Game over");
                if(mainActivity.game.getCurrentPlayer().getPoints()>mainActivity.game.getOppScore()){
                    mainActivity.fragment.sendMessage("&");
                    mainActivity.showEndGame(true);
                }else{
                    mainActivity.fragment.sendMessage("$");
                    mainActivity.showEndGame(false);
                }
            }
        }

    }

    /**
     * Listener for pass turn button
     */
    public static final class MyPassClickListener implements View.OnClickListener {
        public MainActivity mainActivity;
        private TextView turnCount;
        public MyPassClickListener(MainActivity m){
            mainActivity=m;
            turnCount= (TextView) mainActivity.findViewById(R.id.turnCount);
        }
        public void onClick(View v){
            mainActivity.game.skipTurn();
            turnCount.setText("TURN: "+mainActivity.game.getTurnCount());
            if(mainActivity.game.endGame()){
                Log.i("Game","Game over");
                if(mainActivity.game.getCurrentPlayer().getPoints()>mainActivity.game.getOppScore()){
                    mainActivity.fragment.sendMessage("&");
                    mainActivity.showEndGame(true);

                }else{
                    mainActivity.fragment.sendMessage("$");
                    mainActivity.showEndGame(false);
                }
            }else{
                String message = "@0";
                mainActivity.fragment.sendMessage(message);
            }
        }
    }
    /**
     * Long click listener
     */
    public static final class MyLongClickListener implements View.OnLongClickListener {
        public MainActivity mainActivity;
        public MyLongClickListener(MainActivity m){
            mainActivity=m;
        }
        public boolean onLongClick(View v) {

            ClipData.Item item = new ClipData.Item((CharSequence) v.getTag());

            String[] mimeTypes = {ClipDescription.MIMETYPE_TEXT_PLAIN};
            ClipData data = new ClipData(v.getTag().toString(), mimeTypes, item);
            View.DragShadowBuilder shadowBuilder = new View.DragShadowBuilder(v);

            v.startDrag(data, shadowBuilder, v, 0);

            v.setVisibility(View.INVISIBLE);

            return true;
        }
    }

    /**
     * Drag listener for generic tiles
     */
    public static class MyDragListener implements View.OnDragListener {
        public MainActivity mainActivity;
        private int x=-1,y=-1,z=-1;
        public MyDragListener(MainActivity m){
            mainActivity=m;
        }
        public boolean onDrag(View v, DragEvent event){
            final View view = (View) event.getLocalState();
            int id=v.getId();
            switch(event.getAction()){
                case DragEvent.ACTION_DRAG_STARTED:
                    break;
                case DragEvent.ACTION_DRAG_ENTERED:
                    v.setBackgroundColor(Color.RED);
                    break;
                case DragEvent.ACTION_DRAG_EXITED:
                    v.setBackgroundResource(R.drawable.tilesmall);
                    break;
                case DragEvent.ACTION_DROP:
                    if(id==R.id.tilegeneric) {
                        int q, r;
                        //Determine coordinates of which tile this listener belongs to
                        for (q = 0; q < mainActivity.tileBoard.length; q++) {
                            for (r = 0; r < mainActivity.tileBoard[q].length; r++) {
                                if (v == mainActivity.tileBoard[q][r]) {
                                    x = q;
                                    y = r;
                                }
                            }
                        }
                        //Determine coordinate of which tile letter belongs to
                        for(q = 0; q < 7; q++){
                            if(mainActivity.playerHand[q]!=null && view==mainActivity.playerHand[q]){
                                z = q;
                            }
                        }
                        Log.i("Coordinate", "x "+x+" y "+y);
                        if (x != -1 && y != -1) {
                            if(mainActivity.blockBoard[x][y]==null) {
                                //Place block in new loc
                                view.setX(v.getX());
                                view.setY(v.getY());
                                view.bringToFront();
                                mainActivity.blockBoard[x][y] = view;
                                if (z!=-1){
                                    //If block is being moved from player hand, remove from hand
                                    mainActivity.game.getCurrentPlayer().removeLetter(z);
                                    mainActivity.playerHand[z]=null;
                                }else{
                                    //If block is being moved from another loc on the board, null prev loc
                                    int s=0,t=0;
                                    for(s=0;s<mainActivity.blockBoard.length;s++){
                                        for(t=0;t<mainActivity.blockBoard.length;t++){
                                            if(view==mainActivity.blockBoard[s][t] && (s!=x || t!=y)){
                                                mainActivity.blockBoard[s][t]=null;
                                                Log.i("BoardNull","s "+s+" t "+t);
                                                break;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }else if(id ==R.id.tilehand){
                        int q;
                        //Determine coordinates of which tile this listener belongs to
                        for (q = 0; q < mainActivity.tileHand.length; q++) {
                            if (v == mainActivity.tileHand[q]) {
                                x = q;
                            }
                        }
                        //Determine coordinate of which tile letter belongs to
                        for(q = 0; q < 7; q++){
                            if(mainActivity.playerHand[q]!=null && view==mainActivity.playerHand[q]){
                                z = q;
                            }
                        }
                        if(x!=-1){
                            if(mainActivity.playerHand[x]==null){
                                //Place block in new loc
                                view.setX(v.getX());
                                view.setY(v.getY());
                                view.bringToFront();
                                mainActivity.playerHand[x] = (ImageView)view;
                                if (z!=-1){
                                    //If block is being moved from player hand, remove from hand
                                    Log.i("HandNull", "z "+z);
                                    mainActivity.game.getCurrentPlayer().removeLetter(z);
                                    mainActivity.playerHand[z]=null;
                                }else{
                                    //If block is being moved from another loc on the board, null prev loc
                                    int s=0,t=0;
                                    for(s=0;s<mainActivity.blockBoard.length;s++){
                                        for(t=0;t<mainActivity.blockBoard.length;t++){
                                            if(view==mainActivity.blockBoard[s][t] && (s!=x || t!=y)){
                                                mainActivity.blockBoard[s][t]=null;
                                                Log.i("BoardNull","s "+s+" t "+t);
                                                break;
                                            }
                                        }
                                    }
                                }
                                mainActivity.game.getCurrentPlayer().putLetter(Translator.translateViewToLetter(view),x);
                            }
                        }
                    }
                    break;
                case DragEvent.ACTION_DRAG_ENDED:
                    v.setBackgroundResource(R.drawable.tilesmall);
                    view.post(new Runnable() {
                        public void run() {
                            view.setVisibility(View.VISIBLE);
                        }
                    });
                    break;
                default:
                    break;
            }

            return true;
        }
    }

    /**
     * Drag listener for special tiles
     */
    public static class MyDragListener2 implements View.OnDragListener {
        public MainActivity mainActivity;
        private int x=-1,y=-1,z=-1;
        public MyDragListener2(MainActivity m){
            mainActivity=m;
        }
        public boolean onDrag(View v, DragEvent event){
            final View view = (View) event.getLocalState();
            int id=v.getId();
            switch(event.getAction()){
                case DragEvent.ACTION_DRAG_STARTED:
                    break;
                case DragEvent.ACTION_DRAG_ENTERED:
                    v.setBackgroundColor(Color.RED);
                    break;
                case DragEvent.ACTION_DRAG_EXITED:
                    if(id==R.id.tilestar){
                        v.setBackgroundResource(R.drawable.tilestar);
                    }else if(id==R.id.tiledoubleletter){
                        v.setBackgroundResource((R.drawable.tiledoubleletter));
                    }else if(id==R.id.tiletripleletter){
                        v.setBackgroundResource(R.drawable.tiletripleletter);
                    }else if(id==R.id.tiledoubleword){
                        v.setBackgroundResource(R.drawable.tiledoubleword);
                    }else if(id==R.id.tiletripleword){
                        v.setBackgroundResource(R.drawable.tiletripleword);
                    }
                    break;
                case DragEvent.ACTION_DROP:
                    int q, r;
                    //Determine coordinates of which tile this listener belongs to
                    for (q = 0; q < mainActivity.tileBoard.length; q++) {
                        for (r = 0; r < mainActivity.tileBoard[q].length; r++) {
                            if (v == mainActivity.tileBoard[q][r]) {
                                x = q;
                                y = r;
                            }
                        }
                    }
                    //Determine coordinate of which tile letter belongs to
                    for(q = 0; q < 7; q++){
                        if(mainActivity.playerHand[q]!=null && view==mainActivity.playerHand[q]){
                            z = q;
                        }
                    }
                    Log.i("Coordinate", "x "+x+" y "+y);
                    if (x != -1 && y != -1) {
                        if(mainActivity.blockBoard[x][y]==null) {
                            //Place block in new loc
                            view.setX(v.getX());
                            view.setY(v.getY());
                            view.bringToFront();
                            mainActivity.blockBoard[x][y] = view;
                            if (z!=-1){
                                //If block is being moved from player hand, remove from hand
                                Log.i("HandNull", "z "+z);
                                mainActivity.game.getCurrentPlayer().removeLetter(z);
                                mainActivity.playerHand[z]=null;
                            }else{
                                //If block is being moved from another loc on the board, null prev loc
                                int s=0,t=0;
                                for(s=0;s<mainActivity.blockBoard.length;s++){
                                    for(t=0;t<mainActivity.blockBoard.length;t++){
                                        if(view==mainActivity.blockBoard[s][t] && (s!=x || t!=y)){
                                            mainActivity.blockBoard[s][t]=null;
                                            Log.i("BoardNull","s "+s+" t "+t);
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    break;
                case DragEvent.ACTION_DRAG_ENDED:
                    if(id==R.id.tilestar){
                        v.setBackgroundResource(R.drawable.tilestar);
                    }else if(id==R.id.tiledoubleletter){
                        v.setBackgroundResource((R.drawable.tiledoubleletter));
                    }else if(id==R.id.tiletripleletter){
                        v.setBackgroundResource(R.drawable.tiletripleletter);
                    }else if(id==R.id.tiledoubleword){
                        v.setBackgroundResource(R.drawable.tiledoubleword);
                    }else if(id==R.id.tiletripleword){
                        v.setBackgroundResource(R.drawable.tiletripleword);
                    }
                    view.post(new Runnable() {
                        public void run() {
                            view.setVisibility(View.VISIBLE);
                        }
                    });
                    break;
                default:
                    break;
            }

            return true;
        }
    }
}
