package com.example.capapp;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.icu.util.Output;
import android.os.Bundle;
import android.renderscript.ScriptGroup;
import android.util.Log;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.Charset;
import java.util.UUID;

public class DisplayPositionActivity extends AppCompatActivity {
    private static final String TAG = "DisplayPositionActivity";
    private static final String appName = "CapApp";
    private static final UUID MY_UUID_INSECURE =
            UUID.fromString("8ce255c0-200a-11e0-ac64-0800200c9a66");
    private static BluetoothAdapter BA;
    private static Context mContext;

    private AcceptThread mInsecureAcceptThread;
    private ConnectThread mConnectThread;
    private BluetoothDevice mDevice;
    private UUID deviceUUID;
    ProgressDialog mProgressDialog;
    private ConnectedThread mConnectedThread;


    /** Constructor**/
    public DisplayPositionActivity(Context context) {
        mContext = context;
        BA = BluetoothAdapter.getDefaultAdapter();
    }

    public DisplayPositionActivity() {
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
        Log.d(TAG, "Server started.");

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
    public void startClient(BluetoothDevice device, UUID uuid) {
        Log.d(TAG, "Client started.");

        // Create process dialog box
        mProgressDialog = ProgressDialog.show(mContext, "Connecting Bluetooth"
                , "Please wait...", true);

        mConnectThread = new ConnectThread(device, uuid);
        mConnectThread.start();

    }

    /** Manages a successful thread connection**/
    private class ConnectedThread extends Thread {
        private final BluetoothSocket mSocket;
        private final InputStream mInStream;
        private final OutputStream mOutStream;

        public ConnectedThread(BluetoothSocket socket) {
            Log.d(TAG, "ConnectedThread: Starting.");
            mSocket = socket;
            InputStream tmpIn = null;
            OutputStream tmpOut = null;

            // dismiss process dialog box since connection is successful
            mProgressDialog.dismiss();

            // get inputs and outputs from in/out stream
            try {
                tmpIn = mSocket.getInputStream();
                tmpOut = mSocket.getOutputStream();
            } catch (IOException e) {
                e.printStackTrace();
            }
            mInStream = tmpIn;
            mOutStream = tmpOut;
        }

        public void run() {
            // get input from input stream
            byte[] buffer = new byte[1024];
            int bytes;

            // listens to the input stream until exception occurs
            while(true) {
                try {
                    bytes = mInStream.read(buffer);
                    // incoming message as a string
                    String message = new String(buffer, 0, bytes);
                    Log.d(TAG, "InputStream: " + message);
                } catch (IOException e) {
                    Log.e(TAG, "OutputStream: Error reading from InputStream. " + e.getMessage());
                    break;
                }
            }
        }
        /** Call from main activity to send data to Pi**/
        public void write(byte[] bytes) {
            // string to send to OutputStream
            String text = new String(bytes, Charset.defaultCharset());
            Log.d(TAG, "OutputStream: " + text);
            try {
                mOutStream.write(bytes);
            } catch (IOException e) {
                Log.e(TAG, "OutputStream: Error writing to output stream. " + e.getMessage());
            }
        }


        /** Call from main activity to shut down the connection **/
        public void cancel() {
            try {
                mSocket.close();
            } catch (IOException e) { }
        }
    }

    /** Manage connection, perform output stream transmissions, grab input stream transmissions **/
    private void connected(BluetoothSocket mSocket, BluetoothDevice mDevice) {
        Log.d(TAG, "connected(): Starting.");

        // start thread
        mConnectedThread = new ConnectedThread(mSocket);
        mConnectedThread.start();
    }

    /** Write to ConnectedThread unsynchronized. **/
    public void write(byte[] out) {
        // synchronize copy of the ConnectedThread and write it out
        Log.d(TAG, "write: Outer write method called");
        mConnectedThread.write(out);
    }
}
