package com.example.michelle.phraseswithacquaintances.bluetoothchat;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.DisplayMetrics;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ViewAnimator;
import android.support.design.widget.Snackbar;

import com.example.michelle.phraseswithacquaintances.common.activities.SampleActivityBase;
import com.example.michelle.phraseswithacquaintances.common.logger.Log;
import com.example.michelle.phraseswithacquaintances.common.logger.LogFragment;
import com.example.michelle.phraseswithacquaintances.common.logger.LogWrapper;
import com.example.michelle.phraseswithacquaintances.common.logger.MessageOnlyLogFilter;
import com.example.michelle.phraseswithacquaintances.game.*;

import static com.example.michelle.phraseswithacquaintances.bluetoothchat.Translator.translateLetterToDrawable;

/**
 * A simple launcher activity containing a summary sample description, sample log and a custom
 * {@link android.support.v4.app.Fragment} which can display a view.
 * <p>
 * For devices with displays with a width of 720dp or greater, the sample log is always visible,
 * on other devices it's visibility is controlled by an item on the Action Bar.
 */
public class MainActivity extends SampleActivityBase {

    public static final String TAG = "MainActivity";
    private ImageView block;
    private View tile;
    public ViewGroup parent;
    private Button endbutton;
    private Button passbutton;
    public static final String IMAGEVIEW_TAG = "Letter Block";
    public Board game;
    public View[][] tileBoard;
    public View[][] blockBoard;
    public View[] tileHand;
    public ImageView[] playerHand;
    public int tileWidth;
    public int tileHeight;
    public int bottom;
    public DisplayMetrics displayMetrics;
    public Toast toast1, toast2, toast3, toast4, toast5;
    public BluetoothChatFragment fragment;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        parent=(ViewGroup) findViewById(R.id.relLayout);
        setTitle("Phrases with Acquaintances");

        if (savedInstanceState == null) {
            try {
                game = new Board(1,MainActivity.this);
            }catch(Exception e){
                android.util.Log.i("Exception","IO Exception");
            }

            FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
            fragment = new BluetoothChatFragment();
            transaction.replace(R.id.sample_content_fragment, fragment);
            transaction.commit();

            displayMetrics = this.getResources().getDisplayMetrics();
            float height = displayMetrics.heightPixels/displayMetrics.density;
            float width = displayMetrics.widthPixels/displayMetrics.density;
            tile = LayoutInflater.from(this).inflate(R.layout.tile, parent, false);
            tileWidth=tile.getLayoutParams().width/(int)displayMetrics.density;
            tileHeight=tile.getLayoutParams().height/(int)displayMetrics.density;
            bottom = (int) (height-tileHeight*7);

            //This is the array of tile Views that make up the board
            tileBoard=new View[9][9];
            //This is the array of letter block Views that have been played onto the board
            blockBoard=new View[9][9];
            //This is the array of letter block Views that make up the player hand
            playerHand=new ImageView[7];

            //Initialize tileBoard and game.board
            int x, y;
            for(x=0;x<9;x++) {
                for(y=0;y<9;y++) {
                    tile = LayoutInflater.from(this).inflate(R.layout.tile, parent, false);
                    tile.setX((tileWidth * x) * displayMetrics.density);
                    tile.setY(tileWidth*y*displayMetrics.density);
                    parent.addView(tile);
                    if(x==4&&y==4){
                        tile.setBackgroundResource(R.drawable.tilestar);
                        tile.setOnDragListener(new Listeners.MyDragListener2(this));
                        tile.setId(R.id.tilestar);
                        game.setGenericTile(x,y);
                    }else if((x==0||x==8)&&(y==0||y==8)){
                        tile.setBackgroundResource(R.drawable.tiletripleword);
                        tile.setOnDragListener(new Listeners.MyDragListener2(this));
                        tile.setId(R.id.tiletripleword);
                        game.setMultiplierTile(x,y,"word",3);
                    }else if((x==3||x==5)&&(y==3||y==5)){
                        tile.setBackgroundResource(R.drawable.tiledoubleletter);
                        tile.setOnDragListener(new Listeners.MyDragListener2(this));
                        tile.setId(R.id.tiledoubleletter);
                        game.setMultiplierTile(x,y,"letter",2);
                    }else if((x==2||x==6)&&(y==2||y==6)){
                        tile.setBackgroundResource(R.drawable.tiletripleletter);
                        tile.setOnDragListener(new Listeners.MyDragListener2(this));
                        tile.setId(R.id.tiletripleletter);
                        game.setMultiplierTile(x,y,"letter",3);
                    }else if((x==1||x==7)&&(y==1||y==7)){
                        tile.setBackgroundResource(R.drawable.tiledoubleword);
                        tile.setOnDragListener(new Listeners.MyDragListener2(this));
                        tile.setId(R.id.tiledoubleword);
                        game.setMultiplierTile(x,y,"word",2);
                    }else if(((x==4)&&(y==1||y==7))||((y==4)&&(x==1||x==7))){
                        tile.setBackgroundResource(R.drawable.tiledoubleword);
                        tile.setOnDragListener(new Listeners.MyDragListener2(this));
                        tile.setId(R.id.tiledoubleword);
                        game.setMultiplierTile(x,y,"word",2);
                    }else if(((x==0||x==8)&&(y==3||y==5))||((y==0||y==8)&&(x==3||x==5))){
                        tile.setBackgroundResource(R.drawable.tiledoubleletter);
                        tile.setOnDragListener(new Listeners.MyDragListener2(this));
                        tile.setId(R.id.tiledoubleletter);
                        game.setMultiplierTile(x,y,"letter",2);
                    }else{
                        tile.setBackgroundResource(R.drawable.tilesmall);
                        tile.setOnDragListener(new Listeners.MyDragListener(this));
                        tile.setId(R.id.tilegeneric);
                        game.setGenericTile(x,y);
                    }
                    tileBoard[x][y]=tile;
                }
            }

            //Initialize toasts
            Context context = getApplicationContext();
            toast1 = Toast.makeText(context, "Letters must be played to end turn", Toast.LENGTH_SHORT);
            toast2 = Toast.makeText(context, "Letters must be placed in same row or column", Toast.LENGTH_SHORT);
            toast3 = Toast.makeText(context, "First word must use center tile", Toast.LENGTH_SHORT);
            toast4 = Toast.makeText(context, "Not a valid word", Toast.LENGTH_SHORT);
            toast5 = Toast.makeText(context, "No more tiles in the tile bag", Toast.LENGTH_SHORT);


            //Initialize playerHand
            tileHand = new View[7];
            int z;
            for(z=0;z<7;z++){
                double posX=(tileWidth * z)*displayMetrics.density;
                double posY=bottom*displayMetrics.density;
                tile = LayoutInflater.from(this).inflate(R.layout.tile, parent, false);
                tile.setBackgroundResource(R.drawable.tilesmall);
                tile.setX((int)posX);
                tile.setY((int)posY);
                parent.addView(tile);
                tile.setOnDragListener(new Listeners.MyDragListener(this));
                tile.setId(R.id.tilehand);
                tileHand[z]=tile;

                block=(ImageView) LayoutInflater.from(this).inflate(R.layout.block,parent,false);
                block.setTag(IMAGEVIEW_TAG+z);
                block.setX(tile.getX());
                block.setY(tile.getY());
                parent.addView(block);
                block.bringToFront();
                block.setOnLongClickListener(new Listeners.MyLongClickListener(this));
                playerHand[z]=block;
            }

            //Get player hand, draw onto board
            Letter[] l=game.getCurrentPlayer().getPlayerHand();
            int[] drawables= translateLetterToDrawable(l);
            int i;
            for(i=0;i<drawables.length&&i<playerHand.length;i++){
                playerHand[i].setImageResource(drawables[i]);
                playerHand[i].setId(drawables[i]);
                android.util.Log.i("PlayerHand: ","Id: "+drawables[i]);
            }

            endbutton = (Button) findViewById(R.id.endbutton);
            endbutton.setOnClickListener(new Listeners.MyEndClickListener(this));
            passbutton = (Button) findViewById(R.id.passbutton);
            passbutton.setOnClickListener(new Listeners.MyPassClickListener(this));
            /*game.decodeMessage("v104s1p3a'r1s1!h106s1p3i1n2a1c3h2!v614h2u2g4s1!v436b3o2o2k4!v533u3!h436L2o2G4s1!h616A1wga1k4e1n2!v268w6i1n2!@32");
            updateBoardUI();
            game.setTurnCount(7);
            game.getCurrentPlayer().setPoints(20);
            TextView turnCount = this.findViewById(R.id.turnCount);
            turnCount.setText("TURN: "+7);
            TextView points = this.findViewById(R.id.score);
            points.setText("YOUR SCORE: "+20);*/
        }
    }

    public void updateBoardUI(){
        int x,y;
        for(x = 0; x<9; x++){
            for(y = 0; y<9; y++){
                blockBoard[x][y] = null;
                int drawable = translateLetterToDrawable(game.board[x][y].getLetter());
                if(drawable!=0){
                    ImageView block = (ImageView) LayoutInflater.from(this).inflate(R.layout.block,parent,false);
                    block.setX((tileWidth * x)*displayMetrics.density);
                    block.setY(tileWidth*y*displayMetrics.density);
                    block.setImageResource(drawable);
                    block.setId(drawable);
                    parent.addView(block);
                    blockBoard[x][y]=block;
                }
            }
        }
        TextView turnCount = this.findViewById(R.id.turnCount);
        turnCount.setText("TURN: "+game.getTurnCount());
        TextView oppScore = this.findViewById(R.id.opponentScore);
        oppScore.setText("OPPONENT SCORE: "+game.getOppScore());
    }

    public void showEndGame(boolean youWon){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        if (youWon) {
            int points = game.getCurrentPlayer().getPoints()-game.getOppScore();
            builder.setMessage("Congrats, you won the game! You beat your opponent by "+points+" points.")
                    .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {

                        }
                    });
            // Create the AlertDialog object and return it
            AlertDialog alertDialog = builder.create();
            alertDialog.show();
        }else{
            int points = game.getOppScore()-game.getCurrentPlayer().getPoints();
            builder.setMessage("Sorry, you lost the game. You lost by "+points+" points.")
                    .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {

                        }
                    });
            // Create the AlertDialog object and return it
            AlertDialog alertDialog = builder.create();
            alertDialog.show();
        }
    }
}

