package com.fun.funlearn;

import android.app.ActivityManager;
import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.icu.math.BigDecimal;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class User_Info_Activity extends AppCompatActivity {
    private long exitTime = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        ActivityCollector.addActivity(this);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user__info_);
        final Bundle bundle = this.getIntent().getExtras();
        TextView c = (TextView) findViewById(R.id.correct);
        c.setText(String.valueOf(User.getinstance().getTotal_correct()));
        final TextView i = (TextView) findViewById(R.id.incorrect);
        i.setText(String.valueOf(User.getinstance().getTotal_incorrect()));
        TextView t = (TextView) findViewById(R.id.total);
        t.setText(String.valueOf(User.getinstance().getTotal_number()));
        TextView n = (TextView) findViewById(R.id.Userinfo_username);
        n.setText(String.valueOf(User.getinstance().getUsername()));
        float acc = (float) User.getinstance().getTotal_correct() / (float) User.getinstance().getTotal_number();
        acc = acc * 100;
        Button Continue = (Button) findViewById(R.id.Userinfo_continue);
        String acc_1 = acc + "%";
        TextView a = (TextView) findViewById(R.id.accuracy);
        a.setText(acc_1);
        Continue.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Info_Activity.this, MainActivity.class);
                intent.addFlags(1);
                Bundle bundle1 = new Bundle();
                bundle1 = bundle;
                intent.putExtras(bundle);//附带上额外的数据
                startActivity(intent);
            }
        });
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
}
