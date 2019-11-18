package com.example.capapp;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.io.IOException;
import java.util.UUID;

public class DisplayPositionActivity extends AppCompatActivity {
    private static final String TAG = "DisplayPositionActivity";
    private static final String appName = "CapApp";
    private static final UUID MY_UUID_INSECURE =
            UUID.fromString("8ce255c0-200a-11e0-ac64-0800200c9a66");
    private final BluetoothAdapter BA;
    Context mContext;

    private AcceptThread mInsecureAcceptThread;

    /** Constructor**/
    public DisplayPositionActivity(Context context) {
        mContext = context;
        BA = BluetoothAdapter.getDefaultAdapter();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_position);

        // Get the Intent that started this activity and extract the string
        Intent intent = getIntent();
        String position = intent.getStringExtra(MainActivity.EXTRA_MESSAGE);

        // Capture the layout's TextView and set the string as its text
        TextView textView = findViewById(R.id.textView);
        textView.setText(position);
    }

    /**
     ** THREADS
     **/

    /** Accept Thread - listens for incoming connections **/
    private class AcceptThread extends Thread {
        // local server socket
        public final BluetoothServerSocket serverSocket;
        public AcceptThread() {
            BluetoothServerSocket tmp = null;

            // listening server socket
            try {
                tmp = BA.listenUsingInsecureRfcommWithServiceRecord(appName, MY_UUID_INSECURE);
                Log.d(TAG, "AcceptThread: Setting up server using " + MY_UUID_INSECURE);
            } catch(IOException e){
                Log.e(TAG, "AcceptThread: IOException caught: " + e.getMessage());
            }
            serverSocket = tmp;
        }

        /** Runs threads from AcceptThread**/
        public void run() {
            Log.d(TAG, "run: AcceptThread running");
            BluetoothSocket socket = null;

            try {
                // Blocking call - only runs when connection successful
                Log.d(TAG, "run: RFCOM socket server start");
                socket = serverSocket.accept();

                Log.d(TAG, "run: RFCOM socket accepted connection");

            } catch(IOException e) {
                Log.e(TAG, "AcceptThread: IOException caught: " + e.getMessage());
            }

            if(socket != null) {
                //connected(socket, BTDevice);
            }
            Log.i(TAG, "END AcceptThread");
        }

        public void cancel() {
            Log.d(TAG, "cancel: Cancelling AcceptThread");
            try {
                serverSocket.close();
            } catch(IOException e) {
                Log.e(TAG, "cancel: Close of AcceptThread serverSocket failed: " + e.getMessage());
            }
        }
    }

}
