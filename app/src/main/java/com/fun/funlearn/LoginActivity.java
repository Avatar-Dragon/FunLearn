package com.fun.funlearn;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Map;

public class LoginActivity extends AppCompatActivity {
    public static String REGISTER_URL = "http://172.18.68.121:8000/User/register";
    public static String  LOGIN_URL= "http://172.18.68.121:8000/User/login";
    public static String GET_USER_INFO = "http://172.18.68.121:8000/User/userInformation";
    public static String UPDATE_SCORE = "http://172.18.68.121:8000/User/updateScore";
private String Login_User;
    private String passwd;
//    private TextView test;
    private Handler handler = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityCollector.addActivity(this);
        setContentView(R.layout.activity_login);
        Button Login = (Button) findViewById(R.id.login_button);
        Button Register = (Button) findViewById(R.id.register_button);
        final EditText Username = (EditText) findViewById(R.id.username);
        final EditText Password = (EditText) findViewById(R.id.password);
//        test = (TextView) findViewById(R.id.test);
        Login_User = "1234560";
        passwd = "123456";
setHandler();
        Register.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View view) {
        if (Username.getText().toString().isEmpty() || Password.getText().toString().isEmpty()) {
            Toast.makeText(LoginActivity.this, "Something is empty", Toast.LENGTH_SHORT).show();
        } else {
            passwd = Password.getText().toString();
            Login_User = Username.getText().toString();
            sendRequestWithHttpURLConnection(REGISTER_URL);

        }
    }
    });
        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (Username.getText().toString().isEmpty() || Password.getText().toString().isEmpty()) {
                    Toast.makeText(LoginActivity.this, "Something is empty", Toast.LENGTH_SHORT).show();
                } else {
                    passwd = Password.getText().toString();
                    Login_User = Username.getText().toString();
                    User.getinstance().setPassword(passwd);
                    User.getinstance().setUsername(Login_User);
                    sendRequestWithHttpURLConnection(GET_USER_INFO);
                    sendRequestWithHttpURLConnection(LOGIN_URL);

                }
            }
        });

    }
    private void sendRequestWithHttpURLConnection(final String httpurl) {
        new Thread(new Runnable() {
            @Override
            public void run() {

                request(httpurl);
            }
        }).start();
    }


    public String request(String httpurl) {
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
                 data = "username="+ URLEncoder.encode(Login_User, "UTF-8")+
                        "&password="+ URLEncoder.encode(passwd, "UTF-8");
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
            if (httpurl.equals(REGISTER_URL)) {
                m.what = 0;
            } else if (httpurl.equals(LOGIN_URL)) {
                m.what = 1;
            } else {
                m.what = 2;
            }
handler.sendMessage(m);
                return msg;
//            return result;
        }catch(Exception e){e.printStackTrace();}

        return msg;
    }
    private void setHandler() {
        handler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);
                String string = (String)msg.obj;
                switch (msg.what) {
                    case 0://register
                        if (string.equals("{\"response_code\": 0}")) {
                            Toast.makeText(LoginActivity.this, "Registered successfully", Toast.LENGTH_SHORT).show();
                        } else if (string.equals("{\"response_code\": 3}")) {
                            Toast.makeText(LoginActivity.this, "User registered", Toast.LENGTH_SHORT).show();
                        }else {
                            Toast.makeText(LoginActivity.this, "Other error", Toast.LENGTH_SHORT).show();
                        }
                        break;
                    case 1://login
                        if (string.equals("{\"response_code\": 0}")) {
                            Toast.makeText(LoginActivity.this, "Login successfully", Toast.LENGTH_SHORT).show();
                            Intent intent = new Intent(LoginActivity.this, SettingActivity.class);
                            intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                            startActivity(intent);
//                            test.setText(msg);
                        } else if (string.equals("{\"response_code\": 3}")) {
                            Toast.makeText(LoginActivity.this, "User doesn't exit", Toast.LENGTH_SHORT).show();
                        } else if (string.equals("{\"response_code\": 4}")){
                            Toast.makeText(LoginActivity.this, "Wrong password", Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(LoginActivity.this, "Other error", Toast.LENGTH_SHORT).show();
                        }
                        break;
                    case 2:
                        try {
                            JSONObject json = new JSONObject(string);
                                 json = json.getJSONObject("user");
                                 User.getinstance().setTotal_correct(json.getInt("correctNumber"));
                                 User.getinstance().setTotal_incorrect(json.getInt("wrongNumber"));
                        } catch (JSONException ex) {
                            Log.d("log", "json error");
                        } finally {
//                            newsAdapter.notifyDataSetChanged();
                        }
                        break;
                }
                }
            };

        }
    }



