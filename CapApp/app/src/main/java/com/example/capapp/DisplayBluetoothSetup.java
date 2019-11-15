package com.example.capapp;

import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;
import java.util.ArrayList;

public class DisplayBluetoothSetup extends AppCompatActivity implements AdapterView.OnItemClickListener {
    private static final String TAG = "DisplayBluetoothSetup";
    private BluetoothAdapter BA;
    private ArrayList<BluetoothDevice> deviceArrayList = new ArrayList<>();
    private DeviceListAdapter mDeviceAdapter;
    ListView lv;


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_bluetooth_setup);

        Button button_on_off = (Button) findViewById((R.id.button_on_off));
        Button discover_button =(Button)findViewById(R.id.discover_button);
        lv = (ListView)findViewById(R.id.listView);

        BA = BluetoothAdapter.getDefaultAdapter();

        deviceArrayList = new ArrayList<>();

        // Broadcasts when pairing (band state change)
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_BOND_STATE_CHANGED);
        registerReceiver(mBroadcastReceiver2, filter);

        lv.setOnItemClickListener(DisplayBluetoothSetup.this);

        button_on_off.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Log.d(TAG, "onClick: enabling/disabling bluetooth.");
                enableDisableBT();
            }
        });
    }

    /** Toggles Bluetooth, called by the Bluetooth ON/OFF button **/
    public void enableDisableBT(){
        if(BA == null){
            Log.d(TAG, "enableDisableBT: Does not have BT capabilities.");
        }
        if(!BA.isEnabled()){
            Log.d(TAG, "enableDisableBT: enabling BT.");
            Intent enableBTIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivity(enableBTIntent);
            IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
            registerReceiver(mBroadcastReceiver1, BTIntent);
        }
        if(BA.isEnabled()){
            Log.d(TAG, "enableDisableBT: disabling BT.");
            BA.disable();
            Toast.makeText(getApplicationContext(), "Bluetooth has been disabled successfully." ,Toast.LENGTH_LONG).show();
            IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
            registerReceiver(mBroadcastReceiver1, BTIntent);
        }

    }

    /** Finds unpaired devices, called by Discover button **/
    public void findDevices(View view) {
        Log.d(TAG, "btnDiscover: Looking for unpaired devices.");

        if(BA.isDiscovering()){
            BA.cancelDiscovery();
            Log.d(TAG, "btnDiscover: Canceling discovery.");

            //check BT permissions in manifest
            checkBTPermissions();

            BA.startDiscovery();
            IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
            registerReceiver(mBroadcastReceiver3, discoverDevicesIntent);
        }
        if(!BA.isDiscovering()){

            //check BT permissions in manifest
            checkBTPermissions();

            BA.startDiscovery();
            IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
            registerReceiver(mBroadcastReceiver3, discoverDevicesIntent);
        }
    }

    /** Checks Bluetooth permissions for API version 17+ (Lollipop?) **/
    private void checkBTPermissions() {
        if(Build.VERSION.SDK_INT > Build.VERSION_CODES.LOLLIPOP){
            int permissionCheck = 0;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                permissionCheck = this.checkSelfPermission("Manifest.permission.ACCESS_FINE_LOCATION");
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                permissionCheck += this.checkSelfPermission("Manifest.permission.ACCESS_COARSE_LOCATION");
            }
            if (permissionCheck != 0) {

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    this.requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001); //Any number
                }
            }
        }else{
            Log.d(TAG, "checkBTPermissions: No need to check permissions. SDK version < LOLLIPOP.");
        }
    }

    /** Handles clicking on a discovered device **/
    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        // cancel discovery since it's memory intensive
        BA.cancelDiscovery();
        Log.d(TAG, "onItemClick: You clicked on a device. ");
        String deviceName = deviceArrayList.get(position).getName();
        String deviceAddress = deviceArrayList.get(position).getAddress();
        Log.d(TAG, "onItemClick: deviceName =  " + deviceName);
        Log.d(TAG, "onItemClick: deviceAddress =  " + deviceAddress);

        // create bond, requires API 17+ (Jelly Bean MR2)
        if(Build.VERSION.SDK_INT > Build.VERSION_CODES.JELLY_BEAN_MR2) {
            Log.d(TAG, "Trying to pair with " + deviceName);
            deviceArrayList.get(position).createBond();
        }

    }

    /** Destructor to clear memory intensive receivers**/
    @Override
    protected void onDestroy() {
        Log.d(TAG, "onDestroy: called.");
        super.onDestroy();
        unregisterReceiver(mBroadcastReceiver1);
        unregisterReceiver(mBroadcastReceiver2);
        unregisterReceiver(mBroadcastReceiver3);

    }

    /**
     ** BROADCAST RECEIVERS BELOW
     **/

    /** 1.) BroadcastReceiver for ACTION_FOUND -- each time an unpaired device is "discovered" **/
    private final BroadcastReceiver mBroadcastReceiver1 = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            // When discovery finds a device
            if (action.equals(BA.ACTION_STATE_CHANGED)) {
                final int state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BA.ERROR);

                switch(state){
                    case BluetoothAdapter.STATE_OFF:
                        Log.d(TAG, "onReceive: STATE OFF");
                        break;
                    case BluetoothAdapter.STATE_TURNING_OFF:
                        Log.d(TAG, "mBroadcastReceiver1: STATE TURNING OFF");
                        break;
                    case BluetoothAdapter.STATE_ON:
                        Log.d(TAG, "mBroadcastReceiver1: STATE ON");
                        break;
                    case BluetoothAdapter.STATE_TURNING_ON:
                        Log.d(TAG, "mBroadcastReceiver1: STATE TURNING ON");
                        break;
                }
            }
        }
    };

    /** 2.) BroadcastReceiver for selecting devices from the list **/
    private final BroadcastReceiver mBroadcastReceiver2 = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();

            if(action.equals(BluetoothDevice.ACTION_BOND_STATE_CHANGED)) {
                BluetoothDevice mDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);

                // case 1: detected device is already bonded
                if (mDevice.getBondState() == BluetoothDevice.BOND_BONDED) {
                    Log.d(TAG, "BroadcastReceiver: BOND_BONDED. ");
                    Log.d(TAG, "BroadCastReceiver: ############### Bonded with " + mDevice.getName() + "@" + mDevice.getAddress());
                    Toast.makeText(getApplicationContext(), "Successfully paired with " + mDevice.getName(),Toast.LENGTH_SHORT).show();
                }

                // case 2: detected device is currently bonding
                if (mDevice.getBondState() == BluetoothDevice.BOND_BONDING) {
                    Log.d(TAG, "BroadcastReceiver: BOND_BONDING. ");
                }
                // case 3: detected device is breaking a bond
                if (mDevice.getBondState() == BluetoothDevice.BOND_NONE) {
                    Log.d(TAG, "BroadcastReceiver: BOND_NONE. ");
                }
            }
        }
    };


    /** 3.) Broadcast Receiver for listing devices that are not yet paired - Executed by btnDiscover() method. **/
    private BroadcastReceiver mBroadcastReceiver3 = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();
            Log.d(TAG, "onReceive: ACTION FOUND.");

            if (action.equals(BluetoothDevice.ACTION_FOUND)){
                BluetoothDevice device = intent.getParcelableExtra (BluetoothDevice.EXTRA_DEVICE);
                deviceArrayList.add(device);
                Log.d(TAG, "onReceive: " + device.getName() + ": " + device.getAddress());
                mDeviceAdapter = new DeviceListAdapter(context, R.layout.device_adapter_view, deviceArrayList);
                lv.setAdapter(mDeviceAdapter);
            }
        }
    };


//    public void visible(View v){
//        Intent getVisible = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
//        startActivityForResult(getVisible, 0);
//    }

//    public void list(View v){
//        pairedDevices = BA.getBondedDevices();
//
//        ArrayList list = new ArrayList();
//
//        for(BluetoothDevice bt : pairedDevices) list.add(bt.getName());
//        Toast.makeText(getApplicationContext(), "Showing Paired Devices",Toast.LENGTH_SHORT).show();
//
//        final ArrayAdapter adapter = new  ArrayAdapter(this,android.R.layout.simple_list_item_1, list);
//
//        lv.setAdapter(adapter);
//    }
}
