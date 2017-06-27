package com.fun.funlearn;

import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Debug;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
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
private static final String theurl = "http://172.18.68.121:8000/OpenTrivia/getQuestion?amount=3";
    public static String UPDATE_SCORE = "http://172.18.68.121:8000/User/updateScore";
//    &category=9&difficulty=easy&questuonType=multiple
    private static final String DEBUG_TAG = "NetworkStatusExample";
    private Handler handler = null;
    private static final int UPDATE_CONTENT = 0;
    private static final int POST_SCORE = 1;
    private List<Question_info> Question_List = new ArrayList<Question_info>();
    private TextView Q1;
    private TextView Q2;
    private TextView Q3;
    private String difficulty;
    private String question_type;
    private RadioGroup Choices_1;
    private RadioGroup Choices_2;
    private RadioGroup Choices_3;
    private RadioButton A;
    private RadioButton B;
    private RadioButton C;
    private RadioButton D;
    private RadioButton A2;
    private RadioButton B2;
    private RadioButton C2;
    private RadioButton D2;
    private RadioButton A3;
    private RadioButton B3;
    private RadioButton C3;
    private RadioButton D3;
    private Button Commit;
    private Button Reset;
    private Button To_User_Info;
    private Button Continue;
    private long exitTime = 0;
    private int category;
    private int add_correct = 0;
    private int add_incorrect = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityCollector.addActivity(this);
        setContentView(R.layout.activity_main);



           final Bundle bundle = this.getIntent().getExtras();
            category = bundle.getInt("category");
            difficulty = bundle.getString("difficulty");
            question_type = bundle.getString("question_type");
           Q1 = (TextView) findViewById(R.id.question);
        Q2 = (TextView) findViewById(R.id.question2);
        Q3 = (TextView) findViewById(R.id.question3);
        A = (RadioButton) findViewById(R.id.Choice_A);
        A2 = (RadioButton) findViewById(R.id.Choice_A2);
        A3 = (RadioButton) findViewById(R.id.Choice_A3);
        B = (RadioButton) findViewById(R.id.Choice_B);
        B2 = (RadioButton) findViewById(R.id.Choice_B2);
        B3 = (RadioButton) findViewById(R.id.Choice_B3);
        C = (RadioButton) findViewById(R.id.Choice_C);
        C2 = (RadioButton) findViewById(R.id.Choice_C2);
        C3 = (RadioButton) findViewById(R.id.Choice_C3);
        D = (RadioButton) findViewById(R.id.Choice_D);
        D2 = (RadioButton) findViewById(R.id.Choice_D2);
        D3 = (RadioButton) findViewById(R.id.Choice_D3);
        Choices_1 = (RadioGroup) findViewById(R.id.multi_1);
        Choices_2 = (RadioGroup) findViewById(R.id.multi_2);
        Choices_3 = (RadioGroup) findViewById(R.id.multi_3);
        Reset = (Button) findViewById(R.id.reset);
        Commit = (Button) findViewById(R.id.commit);
        To_User_Info = (Button) findViewById(R.id.to_userinfo);
        Continue = (Button) findViewById(R.id.Continue);
        setHandler();
        ConnectivityManager connMgr = (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);
        final NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if(networkInfo != null&& networkInfo.isConnected()) //表示网络已连接
        {
            add_correct = 0;
            add_incorrect = 0;
            sendRequestWithHttpURLConnection();
        } else {
            Q1.setText("No network connection available.");
        }
        Reset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, SettingActivity.class);
                startActivity(intent);
                User.getinstance().ResetAdd_c();
                User.getinstance().ResetAdd_inc();
            }
        });
        Continue.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                add_correct = 0;
                add_incorrect = 0;
                 A.setBackgroundColor(Color.WHITE);
                B.setBackgroundColor(Color.WHITE);
                C.setBackgroundColor(Color.WHITE);
                D.setBackgroundColor(Color.WHITE);
                A2.setBackgroundColor(Color.WHITE);
                B2.setBackgroundColor(Color.WHITE);
                C2.setBackgroundColor(Color.WHITE);
                D2.setBackgroundColor(Color.WHITE);
                A3.setBackgroundColor(Color.WHITE);
                B3.setBackgroundColor(Color.WHITE);
                C3.setBackgroundColor(Color.WHITE);
                D3.setBackgroundColor(Color.WHITE);
                Choices_1.clearCheck();
                Choices_2.clearCheck();
                Choices_3.clearCheck();
                Question_List.clear();
                sendRequestWithHttpURLConnection();
            }
        });
        Commit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                add_correct = 0;
                add_incorrect = 0;
                for (int i = 0; i < 3; i++) {
                    switch (i) {
                        case 0:
                            for (int j = 0; j < Choices_1.getChildCount(); j++) {
                                RadioButton rd = (RadioButton) Choices_1.getChildAt(j);
                                // xxx：扫描到的button是正确答案
                                boolean xxx = rd.getText().equals(Question_List.get(i).getCorrect_answer());
                                if (xxx) {
                                    rd.setBackgroundColor(Color.GREEN);
//                                    if (rd.isChecked()) User.getinstance().add_correct();
                                    if (rd.isChecked()) {
                                        User.getinstance().add_correct();
                                        add_correct++;
                                    }
                                }
                                if (rd.isChecked() && (!xxx)) {
                                    rd.setBackgroundColor(Color.RED);
                                    User.getinstance().add_incorrect();
                                    add_incorrect++;
                                }
                            }
                            break;
                        case 1:
                            for (int j = 0; j < Choices_2.getChildCount(); j++) {
                                RadioButton rd = (RadioButton) Choices_2.getChildAt(j);
                                boolean xxx = rd.getText().equals(Question_List.get(i).getCorrect_answer());
                                if (xxx) {
                                    rd.setBackgroundColor(Color.GREEN);
                                    if (rd.isChecked()) {
                                        add_correct++;
                                        User.getinstance().add_correct();
                                    }
                                }
                                if (rd.isChecked() && (!xxx)) {
                                    rd.setBackgroundColor(Color.RED);
                                    User.getinstance().add_incorrect();
                                    add_incorrect++;
                                }
                            }
                            break;
                        case 2:
                            for (int j = 0; j < Choices_3.getChildCount(); j++) {
                                RadioButton rd = (RadioButton) Choices_3.getChildAt(j);
                                boolean xxx = rd.getText().equals(Question_List.get(i).getCorrect_answer());
                                if (xxx) {
                                    rd.setBackgroundColor(Color.GREEN);
                                    if (rd.isChecked()) {
                                        add_correct++;
                                        User.getinstance().add_correct();
                                    }
                                }
                                if (rd.isChecked() && (!xxx)) {
                                    rd.setBackgroundColor(Color.RED);
                                    User.getinstance().add_incorrect();
                                    add_incorrect++;
                                }
                            }
                            break;
                    }
                }
                sendRequestByPost(UPDATE_SCORE);
            }
        });

        To_User_Info.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, User_Info_Activity.class);
                intent.putExtras(bundle);//附带上额外的数据
                startActivity(intent);
            }
        });
        if (this.getIntent().getFlags() == 1) {
            Continue.performClick();
        }
    }
    public void AppExit(Context context) {
        try {
            ActivityCollector.finishAll();
            ActivityManager activityMgr = (ActivityManager) context
                    .getSystemService(Context.ACTIVITY_SERVICE);
            activityMgr.killBackgroundProcesses(context.getPackageName());
            System.exit(0);
        } catch (Exception ignored) {}
    }
    @Override
public boolean onKeyDown(int keyCode, KeyEvent event) {
    if(keyCode == KeyEvent.KEYCODE_BACK && event.getAction() == KeyEvent.ACTION_DOWN){
       if((System.currentTimeMillis()-exitTime) > 2000){
       Toast.makeText(getApplicationContext(), "再按一次退出程序", Toast.LENGTH_SHORT).show();
       exitTime = System.currentTimeMillis();
         } else {
           AppExit(getBaseContext());
            }
        return true;
        }
    return super.onKeyDown(keyCode, event);
}
private void sendRequestWithHttpURLConnection() {
    new Thread(new Runnable() {
        @Override
        public void run() {
            //    &category=9&difficulty=easy&questuonType=multiple
            String httpArg = "&category=" + category + "&difficulty=" + difficulty + "&questionType=" + question_type;
            String httpurl = theurl + httpArg;
            request(httpurl);
        }
    }).start();
}
private void setHandler() {
    handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            String string = (String)msg.obj;
            switch (msg.what) {
                case UPDATE_CONTENT:
                    // 清空界面
//                    newsList.clear();
                    try {
                        JSONArray jsonArray = null;
                        JSONObject json = new JSONObject(string);
                        string = json.getString("results");
                        jsonArray = new JSONArray(string);
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONObject jsonObject = jsonArray.getJSONObject(i);
                            if (question_type.equals("multiple")) {
                                Question_info question_info = new Question_info(jsonObject.getString("category"),
                                        jsonObject.getString("type"),
                                        jsonObject.getString("difficulty"),
                                        jsonObject.getString("question"),
                                        jsonObject.getString("correct_answer"),
                                        jsonObject.getJSONArray("incorrect_answers")
                                );
                                switch (i) {
                                    case 0:
                                        Q1.setText(question_info.getQuestion());
                                        A.setText(question_info.getCorrect_answer());

                                        for (int j = 0; j < jsonObject.getJSONArray("incorrect_answers").length(); j++) {
                                            JSONArray ja = jsonObject.getJSONArray("incorrect_answers");
                                            switch (j) {
                                                case 0:
                                                    B.setText(ja.getString(j));
                                                case 1:
                                                    C.setText(ja.getString(j));
                                                case 2:
                                                    D.setText(ja.getString(j));
                                            }
                                        }
                                        break;
                                    case 1:
                                        Q2.setText(question_info.getQuestion());
                                        A2.setText(question_info.getCorrect_answer());
                                        for (int j = 0; j < jsonObject.getJSONArray("incorrect_answers").length(); j++) {
                                            JSONArray ja = jsonObject.getJSONArray("incorrect_answers");
                                            switch (j) {
                                                case 0:
                                                    B2.setText(ja.getString(j));
                                                case 1:
                                                    C2.setText(ja.getString(j));
                                                case 2:
                                                    D2.setText(ja.getString(j));
                                            }
                                        }
                                        break;
                                    case 2:
                                        Q3.setText(question_info.getQuestion());
                                        A3.setText(question_info.getCorrect_answer());
//                                        JSONArray jsArr = new JSONArray();
//                                        jsArr = jsonObject.getJSONArray("incorrect_answers");
                                        for (int j = 0; j < jsonObject.getJSONArray("incorrect_answers").length(); j++) {
                                            JSONArray ja = jsonObject.getJSONArray("incorrect_answers");
//                                            ja.getString()
                                            switch (j) {
                                                case 0:
                                                    B3.setText(ja.getString(j));
                                                case 1:
                                                    C3.setText(ja.getString(j));
                                                case 2:
                                                    D3.setText(ja.getString(j));
                                            }
                                        }
                                        break;
                                }
                                Question_List.add(question_info);
                            } else {
                                Question_info question_info = new Question_info(jsonObject.getString("category"),
                                        jsonObject.getString("type"),
                                        jsonObject.getString("difficulty"),
                                        jsonObject.getString("question"),
                                        jsonObject.getString("correct_answer"),
                                        jsonObject.getString("incorrect_answers"));
                                switch (i) {
                                    case 0:
                                        Q1.setText(question_info.getQuestion());
                                        A.setText(jsonObject.getString("correct_answer"));
                                        B.setText(jsonObject.getString("incorrect_answers"));
                                        C.setVisibility(View.GONE);
                                        D.setVisibility(View.GONE);
                                        break;
                                    case 1:
                                        Q2.setText(question_info.getQuestion());
                                        A2.setText(jsonObject.getString("correct_answer"));
                                        B2.setText(jsonObject.getString("incorrect_answers"));
                                        C2.setVisibility(View.GONE);
                                        D2.setVisibility(View.GONE);
                                    case 2:
                                        Q3.setText(question_info.getQuestion());
                                        A3.setText(jsonObject.getString("correct_answer"));
                                        B3.setText(jsonObject.getString("incorrect_answers"));
                                        C3.setVisibility(View.GONE);
                                        D3.setVisibility(View.GONE);
                                }
                                Question_List.add(question_info);

                            }

                        }

                    } catch (JSONException ex) {
                        Log.d("log", "json error");
                        Toast.makeText(getApplicationContext(), "龙哥电脑没开",
                                Toast.LENGTH_SHORT).show();
                    } finally {
                    }
                    break;
                case POST_SCORE:
                    try {
                        JSONObject json = new JSONObject(string);
                        if (json.getInt("response_code") == 0)
                        Toast.makeText(MainActivity.this, "ok", Toast.LENGTH_SHORT).show();
                        else {
                            Toast.makeText(MainActivity.this, "failed", Toast.LENGTH_SHORT).show();
                        }
                    } catch (JSONException ex) {
                        Log.d("log", "json error");
                    }
            }
        }
    };
}

    public String request(String httpUrl) {
        BufferedReader reader = null;
        String result = null;
        StringBuffer sbf = new StringBuffer();

        try {
            URL url = new URL(httpUrl);
            HttpURLConnection connection = (HttpURLConnection) url
                    .openConnection();
            connection.setRequestMethod("GET");
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
            Q1.setText("龙哥电脑没开");
        }
        return result;
    }
    private void sendRequestByPost(final String httpurl) {
        new Thread(new Runnable() {
            @Override
            public void run() {

                String msg = "";
                BufferedReader reader = null;
                String result = null;
                StringBuffer sbf = new StringBuffer();
                try{
                    HttpURLConnection conn = (HttpURLConnection) new URL(httpurl).openConnection();
                    conn.setRequestMethod("POST");
                    conn.setReadTimeout(5000);
                    conn.setConnectTimeout(5000);
                    conn.setDoOutput(true);
                    conn.setDoInput(true);
                    conn.setUseCaches(false);
                    String data;
                    data = "username="+ URLEncoder.encode(User.getinstance().getUsername(), "UTF-8")+
                            "&password="+ URLEncoder.encode(User.getinstance().getPassword(), "UTF-8")+
                            "&newScore=" + User.getinstance().getTotal_correct()+ "&correctNumber=" + add_correct+
                            "&wrongNumber=" + add_incorrect;
                    OutputStream out = conn.getOutputStream();
                    out.write(data.getBytes());
                    out.flush();
                    InputStream is = conn.getInputStream();
                    ByteArrayOutputStream message = new ByteArrayOutputStream();
                    int len = 0;
                    // 定义缓冲区
                    byte buffer[] = new byte[1024];
                    // 按照缓冲区的大小，循环读取
                    while ((len = is.read(buffer)) != -1) {
                        // 根据读取的长度写入到os对象中
                        message.write(buffer, 0, len);
                    }
                    // 释放资源
                    is.close();
                    message.close();
                    //返回字符串
                    msg = new String(message.toByteArray());
                    Message m =new Message();
                    m.obj = msg;
                    m.what = POST_SCORE;
                    handler.sendMessage(m);

//            return result;
                }catch(Exception e){e.printStackTrace();}


            }
        }).start();
    }
}
