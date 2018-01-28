package com.example.sanuj.iletapp;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.p2p.WifiP2pDevice;
import android.net.wifi.p2p.WifiP2pDeviceList;
import android.net.wifi.p2p.WifiP2pManager;
import android.os.Bundle;
import android.util.Log;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class MainActivity extends Activity {


    private final IntentFilter intentFilter = new IntentFilter();
    WifiP2pManager.Channel mChannel;
    WifiP2pManager mManager;
    ILETReceiver receiver;
    PeerListener peerListListener;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Indicates a change in the Wi-Fi P2P status.
        intentFilter.addAction(WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION);

        // Indicates a change in the list of available peers.
        intentFilter.addAction(WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION);

        // Indicates the state of Wi-Fi P2P connectivity has changed.
        intentFilter.addAction(WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION);

        // Indicates this device's details have changed.
        intentFilter.addAction(WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION);

        mManager = (WifiP2pManager) getSystemService(Context.WIFI_P2P_SERVICE);
        mChannel = mManager.initialize(this, getMainLooper(), null);

        mManager.discoverPeers(mChannel, new WifiP2pManager.ActionListener() {

            @Override
            public void onSuccess() {
                Log.v("TAG", "Hello! success");
                // Code for when the discovery initiation is successful goes here.
                // No services have actually been discovered yet, so this method
                // can often be left blank. Code for peer discovery goes in the
                // onReceive method, detailed below.
            }

            @Override
            public void onFailure(int reasonCode) {
                Log.v("TAG", "fail");
                // Code for when the discovery initiation fails goes here.
                // Alert the user that something went wrong.
            }
        });
        Log.v("TAG", "peer listener");
        peerListListener = new PeerListener();

    }

    class PeerListener implements WifiP2pManager.PeerListListener {
        private List<WifiP2pDevice> peers = new ArrayList<WifiP2pDevice>();
        @Override
        public void onPeersAvailable(WifiP2pDeviceList peerList) {
                Log.v("TAG", "success on peers available");
                Collection<WifiP2pDevice> refreshedPeers = peerList.getDeviceList();
                if (!refreshedPeers.equals(peers)) {
                peers.clear();
                peers.addAll(refreshedPeers);

                // If an AdapterView is backed by this data, notify it
                // of the change. For instance, if you have a ListView of
                // available peers, trigger an update.
                //((WiFiPeerListAdapter) getListAdapter()).notifyDataSetChanged();

                // Perform any other updates needed based on the new list of
                // peers connected to the Wi-Fi P2P network.
                }

                if (peers.size() == 0) {
                Log.d("WiFiDirectActivity.TAG", "No devices found");
                return;
                }
                else
                    Log.d("TAG", "Peer list size: " + peers.size());
        }
    }

    public class ILETReceiver extends BroadcastReceiver {

        WifiP2pManager.PeerListListener pll;

        ILETReceiver(WifiP2pManager mManager, WifiP2pManager.Channel mChannel, Context ctx, WifiP2pManager.PeerListListener peerListListener) {
            pll = peerListListener;

        }

        @Override
        public void onReceive(Context context, Intent intent) {
            Log.v("TAG", "success onReceive");
            String action = intent.getAction();
            if (WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION.equals(action)) {
                // Determine if Wifi P2P mode is enabled or not, alert
                // the Activity.
                int state = intent.getIntExtra(WifiP2pManager.EXTRA_WIFI_STATE, -1);
                if (state == WifiP2pManager.WIFI_P2P_STATE_ENABLED) {
                    //context.setIsWifiP2pEnabled(true);
                } else {
                    //activity.setIsWifiP2pEnabled(false);
                }
                Log.v("TAG", "success ");
            } else if (WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION.equals(action)) {

                // The peer list has changed! We should probably do something about
                // that.
                // Request available peers from the wifi p2p manager. This is an
                // asynchronous call and the calling activity is notified with a
                // callback on PeerListListener.onPeersAvailable()
                if (mManager != null) {
                    mManager.requestPeers(mChannel, pll);
                }
                Log.d("WiFiDirectActivity.TAG", "P2P peers changed");
                Log.v("TAG", "success we called requestPeers");
            } else if (WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION.equals(action)) {

                // Connection state changed! We should probably do something about
                // that.
            } else if (WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION.equals(action)) {
//            DeviceListFragment fragment = (DeviceListFragment) activity.getFragmentManager()
//                    .findFragmentById(R.id.frag_list);
//            fragment.updateThisDevice((WifiP2pDevice) intent.getParcelableExtra(
//                    WifiP2pManager.EXTRA_WIFI_P2P_DEVICE));

            }
        }
    }



    /** register the ILETReceiver with the intent values to be matched */
    @Override
    public void onResume() {
        Log.v("TAG", "success onResume");
        super.onResume();
        receiver = new ILETReceiver(mManager, mChannel, this, peerListListener);
        registerReceiver(receiver, intentFilter);
    }

    @Override
    public void onPause() {
        Log.v("TAG", "success onPause");
        super.onPause();
        unregisterReceiver(receiver);
    }
}

