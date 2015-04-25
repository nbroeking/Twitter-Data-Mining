package main.twitterclassifier;

import android.app.IntentService;
import android.content.Intent;
import android.content.Context;
import android.nfc.Tag;
import android.os.Message;
import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpVersion;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.conn.scheme.PlainSocketFactory;
import org.apache.http.conn.scheme.Scheme;
import org.apache.http.conn.scheme.SchemeRegistry;
import org.apache.http.conn.ssl.SSLSocketFactory;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.protocol.HTTP;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URLEncoder;
import java.security.KeyStore;

import static android.os.Message.obtain;

public class Web extends IntentService {
    private static final String sentiment = "GET SENTIMENT";
    private static final String TAG = "Web service";
    private static final String HOST = "http://gilded.jarahm.com:5000/data";
    /**
     * Starts this service to perform action Foo with the given parameters. If
     * the service is already performing a task this action will be queued.
     *
     */
    public static void getSentiment(Context context) {
        Intent intent = new Intent(context, Web.class);
        intent.setAction(sentiment);
        context.startService(intent);
    }

    public Web() {
        super("Web");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        if (intent != null) {
            if( sentiment.equals(intent.getAction())) {
                handleGetSentiment();
            }
        }
    }

    /**
     * Handle action Foo in the provided background thread with the provided
     * parameters.
     */
    private void handleGetSentiment() {
        Log.d(TAG, "Get Sentiment");
        HttpGet getRequest = new HttpGet(HOST);

        try {
            getRequest.setHeader("Content-type", "application/x-www-form-urlencoded");
            JSONObject json = sendGet(getRequest);

            Log.d(TAG, "Json = " + json.toString());

            JSONArray array = json.getJSONArray("amazon");
            double amazon = array.getDouble(0) / (array.getDouble(0) + array.getDouble(1));
            array = json.getJSONArray("apple");

            double apple = array.getDouble(0) / (array.getDouble(0) + array.getDouble(1));

            array = json.getJSONArray("google");
            double google = array.getDouble(0) / (array.getDouble(0) + array.getDouble(1));

            array = json.getJSONArray("samsung");
            double samsung = array.getDouble(0) / (array.getDouble(0) + array.getDouble(1));

            //Send result
            Intent intent = new Intent();
            intent.setAction("datareceived");
            intent.putExtra("amazon", amazon);
            intent.putExtra("apple", apple);
            intent.putExtra("google", google);
            intent.putExtra("samsung", samsung);

            sendBroadcast(intent);

        } catch (Exception e) {
            Log.e(TAG, "Error creating Post", e);
        }
    }


    /**Helpers that allow us to send http requests
     *
     */
    //This method will send a http get request and return the json object that is returned from the get request
    private JSONObject sendGet(HttpGet get){
        HttpClient client = this.createHttpClient();
        try {
            get.setHeader("Content-type", "application/x-www-form-urlencoded");
            HttpResponse response = client.execute(get);

            HttpEntity entity = response.getEntity();

            InputStream inputStream = null;
            try {
                inputStream = entity.getContent();
                String result;

                // json is UTF-8 by default
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, "UTF-8"), 8);
                StringBuilder sb = new StringBuilder();

                String line;
                while ((line = reader.readLine()) != null) {
                    String addline = line + "\n";
                    sb.append(addline);
                }
                result = sb.toString();

                //JSON Parser
                JSONObject json = new JSONObject(result);
                return json;

            } catch (Exception e) {
                Log.e(TAG, "Error parsing json", e);
            } finally {
                try {
                    if (inputStream != null) inputStream.close();
                } catch (Exception s) {
                    Log.e(TAG, "Could not close stream");
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error creating Get Request", e);
        }
        return null;
    }
    private HttpClient createHttpClient() {
        try {
            KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
            trustStore.load(null, null);

            SSLSocketFactory sf = new TwitterSocketFactory(trustStore);
            sf.setHostnameVerifier(SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);

            HttpParams params = new BasicHttpParams();
            HttpProtocolParams.setVersion(params, HttpVersion.HTTP_1_1);
            HttpProtocolParams.setContentCharset(params, HTTP.DEFAULT_CONTENT_CHARSET);
            HttpProtocolParams.setUseExpectContinue(params, true);
            HttpConnectionParams.setConnectionTimeout(params, 8000);
            HttpConnectionParams.setSoTimeout(params, 8000);

            SchemeRegistry schReg = new SchemeRegistry();
            schReg.register(new Scheme("http", PlainSocketFactory.getSocketFactory(), 80));
            schReg.register(new Scheme("https", sf, 443));
            ClientConnectionManager conMgr = new ThreadSafeClientConnManager(params, schReg);

            return new DefaultHttpClient(conMgr, params);
        } catch (Exception e) {
            Log.e(TAG, "Error creating client", e);
        }
        return null;
    }
}
