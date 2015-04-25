package main.twitterclassifier;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.nfc.Tag;
import android.os.ResultReceiver;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;


public class MainActivity extends ActionBarActivity {

    private static final String TAG = "Main Activity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        IntentFilter filter = new IntentFilter("datareceived");
        registerReceiver(receiver, filter);

        //Get the sentiment on the other thread
        Web.getSentiment(this);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(receiver);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar wills
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void update( double amazon, double apple, double google, double samsung){
        Log.d(TAG, "Amazon " + amazon + " apple " + apple + " google " + google +" samsung " + samsung);
        ImageView amazonImage = (ImageView)this.findViewById(R.id.amazon);
        ImageView appleImage = (ImageView)this.findViewById(R.id.apple);
        ImageView googleImage = (ImageView)this.findViewById(R.id.google);
        ImageView samsungImage = (ImageView)this.findViewById(R.id.samsung);

        Drawable happy = getResources().getDrawable(R.drawable.happy);
        Drawable frowny = getResources().getDrawable(R.drawable.frowny);
        if( amazon < .5){
            amazonImage.setImageDrawable(frowny);
        }
        else{
            amazonImage.setImageDrawable(happy);
        }

        if( apple < .5){
            appleImage.setImageDrawable(frowny);
        }
        else{
            appleImage.setImageDrawable(happy);
        }

        if( google < .5){
            googleImage.setImageDrawable(frowny);
        }
        else{
            googleImage.setImageDrawable(happy);
        }
        if( samsung < .5){
            samsungImage.setImageDrawable(frowny);
        }
        else{
            samsungImage.setImageDrawable(happy);
        }
    }
    private BroadcastReceiver receiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {

            MainActivity.this.update(intent.getDoubleExtra("amazon", 0.0), intent.getDoubleExtra("apple",0.0), intent.getDoubleExtra("google",0.0), intent.getDoubleExtra("samsung",0.0));
        }
    };
}
