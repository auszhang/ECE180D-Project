package com.example.michelle.phraseswithacquaintances.bluetoothchat;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import com.example.michelle.phraseswithacquaintances.game.*;

/**
 * Created by michelle.
 */
public class Translator {
    /**
     * Translate View array to Letter array
     * Used to translate blockBoard, null values in blockBoard are translated to empty
     * @param v
     * @return Letter array
     */
    public static Letter[][] translateViewToLetter(View[][] v){
        int x,y;
        Letter[][] output=new Letter[v.length][v[0].length];
        for(x=0;x<v.length;x++){
            for(y=0;y<v[x].length;y++){
                char c;
                int points;
                if(v[x][y]!=null) {
                    int id = v[x][y].getId();
                    if (id == R.drawable.ablock) {
                        c = 'a';
                        points = 1;
                    } else if (id == R.drawable.bblock) {
                        c = 'b';
                        points = 3;
                    } else if (id == R.drawable.cblock) {
                        c = 'c';
                        points = 3;
                    } else if (id == R.drawable.dblock) {
                        c = 'd';
                        points = 2;
                    } else if (id == R.drawable.eblock) {
                        c = 'e';
                        points = 1;
                    } else if (id == R.drawable.fblock) {
                        c = 'f';
                        points = 4;
                    } else if (id == R.drawable.gblock) {
                        c = 'g';
                        points = 2;
                    } else if (id == R.drawable.hblock) {
                        c = 'h';
                        points = 4;
                    } else if (id == R.drawable.iblock) {
                        c = 'i';
                        points = 1;
                    } else if (id == R.drawable.jblock) {
                        c = 'j';
                        points = 8;
                    } else if (id == R.drawable.kblock) {
                        c = 'k';
                        points = 5;
                    } else if (id == R.drawable.lblock) {
                        c = 'l';
                        points = 1;
                    } else if (id == R.drawable.mblock) {
                        c = 'm';
                        points = 3;
                    } else if (id == R.drawable.nblock) {
                        c = 'n';
                        points = 1;
                    } else if (id == R.drawable.oblock) {
                        c = 'o';
                        points = 1;
                    } else if (id == R.drawable.pblock) {
                        c = 'p';
                        points = 3;
                    } else if (id == R.drawable.qblock) {
                        c = 'q';
                        points = 10;
                    } else if (id == R.drawable.rblock) {
                        c = 'r';
                        points = 1;
                    } else if (id == R.drawable.sblock) {
                        c = 's';
                        points = 1;
                    } else if (id == R.drawable.tblock) {
                        c = 't';
                        points = 1;
                    } else if (id == R.drawable.ublock) {
                        c = 'u';
                        points = 1;
                    } else if (id == R.drawable.vblock) {
                        c = 'v';
                        points = 4;
                    } else if (id == R.drawable.wblock) {
                        c = 'w';
                        points = 4;
                    } else if (id == R.drawable.xblock) {
                        c = 'x';
                        points = 8;
                    } else if (id == R.drawable.yblock) {
                        c = 'y';
                        points = 4;
                    } else if (id == R.drawable.zblock) {
                        c = 'z';
                        points = 10;
                    } else {
                        c = ' ';
                        points = 0;
                    }
                    Log.i("Translator","Translated "+c);
                    Letter l = new Letter(c, points);
                    output[x][y] = l;
                }else{
                    output[x][y]=new Letter(' ',0);
                }
            }
        }
        return output;
    }

    /**
     * Translate single View to Letter
     * @param v
     * @return
     */
    public static Letter translateViewToLetter(View v){
        Letter output;
        char c;
        int points;
        if(v==null){return new Letter(' ',0);}
        int id = v.getId();
        if (id == R.drawable.ablock) {
            c = 'a';
            points = 1;
        } else if (id == R.drawable.bblock) {
            c = 'b';
            points = 3;
        } else if (id == R.drawable.cblock) {
            c = 'c';
            points = 3;
        } else if (id == R.drawable.dblock) {
            c = 'd';
            points = 2;
        } else if (id == R.drawable.eblock) {
            c = 'e';
            points = 1;
        } else if (id == R.drawable.fblock) {
            c = 'f';
            points = 4;
        } else if (id == R.drawable.gblock) {
            c = 'g';
            points = 2;
        } else if (id == R.drawable.hblock) {
            c = 'h';
            points = 4;
        } else if (id == R.drawable.iblock) {
            c = 'i';
            points = 1;
        } else if (id == R.drawable.jblock) {
            c = 'j';
            points = 8;
        } else if (id == R.drawable.kblock) {
            c = 'k';
            points = 5;
        } else if (id == R.drawable.lblock) {
            c = 'l';
            points = 1;
        } else if (id == R.drawable.mblock) {
            c = 'm';
            points = 3;
        } else if (id == R.drawable.nblock) {
            c = 'n';
            points = 1;
        } else if (id == R.drawable.oblock) {
            c = 'o';
            points = 1;
        } else if (id == R.drawable.pblock) {
            c = 'p';
            points = 3;
        } else if (id == R.drawable.qblock) {
            c = 'q';
            points = 10;
        } else if (id == R.drawable.rblock) {
            c = 'r';
            points = 1;
        } else if (id == R.drawable.sblock) {
            c = 's';
            points = 1;
        } else if (id == R.drawable.tblock) {
            c = 't';
            points = 1;
        } else if (id == R.drawable.ublock) {
            c = 'u';
            points = 1;
        } else if (id == R.drawable.vblock) {
            c = 'v';
            points = 4;
        } else if (id == R.drawable.wblock) {
            c = 'w';
            points = 4;
        } else if (id == R.drawable.xblock) {
            c = 'x';
            points = 8;
        } else if (id == R.drawable.yblock) {
            c = 'y';
            points = 4;
        } else if (id == R.drawable.zblock) {
            c = 'z';
            points = 10;
        } else {
            c = ' ';
            points = 0;
        }
        Log.i("Translator","Translated "+c);
        output = new Letter(c, points);
        return output;
    }

    /**
     * Translate Letter array to int array of Drawable ids
     * Used to translate player's hand
     * @param l
     * @return Drawable ids array
     */
    public static int[] translateLetterToDrawable(Letter[] l){
        int x,y;
        int[]output=new int[l.length];
        for(x=0;x<l.length;x++){
            if(l[x].getLetter().equals("a")){
                output[x]=R.drawable.ablock;
            }else if (l[x].getLetter().equals("b")){
                output[x]=R.drawable.bblock;
            }else if (l[x].getLetter().equals("c")){
                output[x]=R.drawable.cblock;
            }else if (l[x].getLetter().equals("d")){
                output[x]=R.drawable.dblock;
            }else if (l[x].getLetter().equals("e")){
                output[x]=R.drawable.eblock;
            }else if (l[x].getLetter().equals("f")){
                output[x]=R.drawable.fblock;
            }else if (l[x].getLetter().equals("g")){
                output[x]=R.drawable.gblock;
            }else if (l[x].getLetter().equals("h")){
                output[x]=R.drawable.hblock;
            }else if (l[x].getLetter().equals("i")){
                output[x]=R.drawable.iblock;
            }else if (l[x].getLetter().equals("j")){
                output[x]=R.drawable.jblock;
            }else if (l[x].getLetter().equals("k")){
                output[x]=R.drawable.kblock;
            }else if (l[x].getLetter().equals("l")){
                output[x]=R.drawable.lblock;
            }else if (l[x].getLetter().equals("m")){
                output[x]=R.drawable.mblock;
            }else if (l[x].getLetter().equals("n")){
                output[x]=R.drawable.nblock;
            }else if (l[x].getLetter().equals("o")){
                output[x]=R.drawable.oblock;
            }else if (l[x].getLetter().equals("p")){
                output[x]=R.drawable.pblock;
            }else if (l[x].getLetter().equals("q")){
                output[x]=R.drawable.qblock;
            }else if (l[x].getLetter().equals("r")){
                output[x]=R.drawable.rblock;
            }else if (l[x].getLetter().equals("s")){
                output[x]=R.drawable.sblock;
            }else if (l[x].getLetter().equals("t")){
                output[x]=R.drawable.tblock;
            }else if (l[x].getLetter().equals("u")){
                output[x]=R.drawable.ublock;
            }else if (l[x].getLetter().equals("v")){
                output[x]=R.drawable.vblock;
            }else if (l[x].getLetter().equals("w")){
                output[x]=R.drawable.wblock;
            }else if (l[x].getLetter().equals("x")){
                output[x]=R.drawable.xblock;
            }else if (l[x].getLetter().equals("y")){
                output[x]=R.drawable.yblock;
            }else if (l[x].getLetter().equals("z")){
                output[x]=R.drawable.zblock;
            }else{
                break;
            }
        }
        return output;
    }

    /**
     * Translate single Letter array to Drawable id
     * @param l
     * @return Drawable id
     */
    public static int translateLetterToDrawable(Letter l){
        int output = 0;
        if(l.getLetter().equals("a")){
            output=R.drawable.ablock;
        }else if (l.getLetter().equals("b")){
            output=R.drawable.bblock;
        }else if (l.getLetter().equals("c")){
            output=R.drawable.cblock;
        }else if (l.getLetter().equals("d")){
            output=R.drawable.dblock;
        }else if (l.getLetter().equals("e")){
            output=R.drawable.eblock;
        }else if (l.getLetter().equals("f")){
            output=R.drawable.fblock;
        }else if (l.getLetter().equals("g")){
            output=R.drawable.gblock;
        }else if (l.getLetter().equals("h")){
            output=R.drawable.hblock;
        }else if (l.getLetter().equals("i")){
            output=R.drawable.iblock;
        }else if (l.getLetter().equals("j")){
            output=R.drawable.jblock;
        }else if (l.getLetter().equals("k")){
            output=R.drawable.kblock;
        }else if (l.getLetter().equals("l")){
            output=R.drawable.lblock;
        }else if (l.getLetter().equals("m")){
            output=R.drawable.mblock;
        }else if (l.getLetter().equals("n")){
            output=R.drawable.nblock;
        }else if (l.getLetter().equals("o")){
            output=R.drawable.oblock;
        }else if (l.getLetter().equals("p")){
            output=R.drawable.pblock;
        }else if (l.getLetter().equals("q")){
            output=R.drawable.qblock;
        }else if (l.getLetter().equals("r")){
            output=R.drawable.rblock;
        }else if (l.getLetter().equals("s")){
            output=R.drawable.sblock;
        }else if (l.getLetter().equals("t")){
            output=R.drawable.tblock;
        }else if (l.getLetter().equals("u")){
            output=R.drawable.ublock;
        }else if (l.getLetter().equals("v")){
            output=R.drawable.vblock;
        }else if (l.getLetter().equals("w")){
            output=R.drawable.wblock;
        }else if (l.getLetter().equals("x")){
            output=R.drawable.xblock;
        }else if (l.getLetter().equals("y")){
            output=R.drawable.yblock;
        }else if (l.getLetter().equals("z")){
            output=R.drawable.zblock;
        }
        return output;
    }

    /**
     * Translate View array to Tile array
     * Used to translate tileBoard
     * @param v
     * @return Tile array
     */
    public static Tile[][] translateViewToTile(View[][] v){
        Tile[][] output=new Tile[v.length][v[0].length];
        int x,y;
        for(x=0;x<v.length;x++){
            for(y=0;y<v[x].length;y++){
                if(v[x][y].getId()==R.id.tilegeneric){
                    output[x][y]=new GenericTile();
                }else if(v[x][y].getId()==R.id.tilestar||v[x][y].getId()==R.id.tiledoubleword){
                    output[x][y]=new MultiplierTile("word",2);
                }else if(v[x][y].getId()==R.id.tiletripleword){
                    output[x][y]=new MultiplierTile("word",3);
                }else if(v[x][y].getId()==R.id.tiledoubleletter){
                    output[x][y]=new MultiplierTile("letter",2);
                }else if(v[x][y].getId()==R.id.tiletripleletter){
                    output[x][y]=new MultiplierTile("letter",3);
                }
            }
        }
        return output;
    }
}
