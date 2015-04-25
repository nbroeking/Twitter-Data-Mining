package main.twitterclassifier;

import android.app.IntentService;
import android.content.Intent;
import android.content.Context;

public class Web extends IntentService {
    private static final String sentiment = "GET SENTIMENT";

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
        // TODO: Handle action
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
