package com.fun.funlearn;

import android.content.Context;
import android.graphics.Bitmap;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Debug;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
private static final String theurl = "http://172.18.68.121:8000/OpenTrivia/getQuestion?amount=1&category=9&difficulty=easy&questuonType=multiple";
    private static final String DEBUG_TAG = "NetworkStatusExample";
    private Handler handler = null;
    private static final int UPDATE_CONTENT = 0;
    private static final int SEC_UPDATE_CONTENT = 1;
    private List<Question_info> Question_List = new ArrayList<Question_info>();
    private TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button search = (Button) findViewById(R.id.search);
        textView = (TextView) findViewById(R.id.url);
        setHandler();
        // 先搜索一番，拿到数据来初始化界面
        ConnectivityManager connMgr = (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);
        final NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        search.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(networkInfo != null&& networkInfo.isConnected()) //表示网络已连接
                {
                    sendRequestWithHttpURLConnection();

//                    new DownloadWebpageText().execute(stringUrl);
//创建AsyncTask实例并执行
                } else{
                    textView.setText("No network connection available.");
                }
            }
        });
    }
//    public String readIt(InputStream stream, int len)throws IOException,
//            UnsupportedEncodingException {
//        Reader reader = null;
//        reader = new InputStreamReader(stream, "UTF-8");
//        char[] buffer = new char[len];
//        reader.read(buffer);
//        return new String(buffer);
//    }
private void sendRequestWithHttpURLConnection() {
    new Thread(new Runnable() {
        @Override
        public void run() {
            request(theurl);
        }
    }).start();
}
private void setHandler() {
    handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what) {
                case UPDATE_CONTENT:
                    String string = (String)msg.obj;
                    // 清空界面
//                    newsList.clear();
                    try {
                        JSONArray jsonArray = null;
                        JSONObject json = new JSONObject(string);
                        string = json.getString("results");
                        jsonArray = new JSONArray(string);
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONObject jsonObject = jsonArray.getJSONObject(i);
                            Question_info question_info = new Question_info(jsonObject.getString("category"),
                                    jsonObject.getString("type"),
                                    jsonObject.getString("difficulty"),
                                    jsonObject.getString("question"),
                                    jsonObject.getString("correct_answer"),
                                    jsonObject.getJSONArray("incorrect_answers")
                                    );
//                            textView.setText(question_info.getQuestion());
                                Question_List.add(question_info);
                        }

                    } catch (JSONException ex) {
                        Log.d("log", "json error");
                        Toast.makeText(getApplicationContext(), "龙哥电脑没开",
                                Toast.LENGTH_SHORT).show();
                    } finally {
//                        newsAdapter.notifyDataSetChanged();
                    }
                    break;
//                case SEC_UPDATE_CONTENT:
//                    Map<String, Object> map = (Map<String, Object>)msg.obj;
//                    ImageView pic = (ImageView)map.get("picture");
//                    Bitmap bitmap = (Bitmap)map.get("bitmap");
//                    pic.setImageBitmap(bitmap);
//                    break;
//                default:
//                    break;
            }
        }
    };
}
    public String request(String httpUrl) {
        BufferedReader reader = null;
        String result = null;
        StringBuffer sbf = new StringBuffer();
//        httpUrl = httpUrl + "?" + httpArg;
        try {
            URL url = new URL(httpUrl);
            HttpURLConnection connection = (HttpURLConnection) url
                    .openConnection();
            connection.setRequestMethod("GET");
            // 填入apikey到HTTP header
            //connection.setRequestProperty("apikey", apikey);
//            connection.connect();
//            int code =  connection.getResponseCode();
            String strRead = null;
            InputStream is = connection.getInputStream();
            reader = new BufferedReader(new InputStreamReader(is));
            while ((strRead = reader.readLine()) != null) {
                sbf.append(strRead);
                sbf.append("\r\n");
            }
            reader.close();
            result = sbf.toString();

            // 发送message
            Message message = new Message();
            message.what = UPDATE_CONTENT;
            message.obj = result;
            handler.sendMessage(message);
        } catch (Exception e) {
            e.printStackTrace();
            Log.d("log", "error");
            textView.setText("龙哥电脑没开");
        }
        return result;
    }
}
