package com.example.capapp;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
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
    private ConnectThread mConnectThread;
    private BluetoothDevice mDevice;
    private UUID deviceUUID;
    ProgressDialog mProgressDialog;


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

        /** Runs threads from AcceptThread automatically**/
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

        /** Cancels the connection. **/
        public void cancel() {
            Log.d(TAG, "cancel: Cancelling AcceptThread");
            try {
                serverSocket.close();
            } catch(IOException e) {
                Log.e(TAG, "cancel: Close of AcceptThread serverSocket failed: " + e.getMessage());
            }
        }
    }

    /** Runs while attempting to make an outgoing connection with a device. Connection either succeeds or fails.**/
    private class ConnectThread extends Thread {
        private BluetoothSocket mSocket;

        public ConnectThread(BluetoothDevice device, UUID uuid) {
            Log.d(TAG, "ConnectThread: starting");
            mDevice = device;
            deviceUUID = uuid;
        }

        /** Automatically executes inside of a thread**/
        public void run() {
            BluetoothSocket tmp = null;
            Log.i(TAG, "Run ConnectThread");

            // Get a BluetoothSocket to connect to a bluetooth device
            // Take bluetooth socket and create an RFcomm socket
            try {
                Log.d(TAG, "ConnectThread.run: Trying to create RFcomm socket using uuid: " + MY_UUID_INSECURE);
                tmp = mDevice.createRfcommSocketToServiceRecord(deviceUUID);
            } catch (IOException e) {
                Log.e(TAG, "ConnectThread.run: Could not create RFcomm socket " + e.getMessage());
            }
            mSocket = tmp;

            // Cancel memory intensive discovery
            BA.cancelDiscovery();

            // Make connection to BluetoothSocket
            try {
                // connect() is a blocking call
                mSocket.connect();
                Log.d(TAG, "ConnectThread.run: The connection was successful.");
            } catch (IOException e) {
                // Close the socket
                try {
                    mSocket.close();
                    Log.d(TAG, "ConnectThread.run: Closed socket successfully .");
                } catch (IOException ee) {
                    Log.e(TAG, "ConnectThread.run: Unable to close connection socket " + ee.getMessage());
                }
                Log.d(TAG, "ConnectThread.run: Could not connect to UUID. ");
            }
            connected(mSocket, mDevice);
        }

        /** Cancels the connection. **/
        public void cancel() {
            Log.d(TAG, "cancel: Closing client socket.");
            try {
                mSocket.close();
            } catch(IOException e) {
                Log.e(TAG, "cancel: Close of ConnectionThread client socket failed: " + e.getMessage());
            }
        }
    }

    /** Starts the connection service: Initiates the AcceptThread to begin a session in server mode. Called by the Activity onResume() **/
    public synchronized void start() {
        Log.d(TAG, "Start.");

        // if a ConnectThread exists, cancel it and create a new one, cancels any thread trying to make a connection
        if (mConnectThread == null) {
            mConnectThread.cancel();
            mConnectThread = null;
        }
        // if an AcceptThread doesn't exist, start one
        if (mInsecureAcceptThread == null) {
            mInsecureAcceptThread.cancel();
            mInsecureAcceptThread = new AcceptThread();
            mInsecureAcceptThread.start(); // this start() function is from the Thread class
        }
    }

    /** Initiates the ConnectThread. AcceptThread waits for a connection. ConnectThread starts and attempts to make a connection with AcceptThread**/
    


}
