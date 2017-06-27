package com.fun.funlearn;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ExpandableListView;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.util.ArrayList;
public class SettingActivity extends AppCompatActivity {
    private ArrayList<Group> gData = null;
    private ArrayList<ArrayList<Item>> iData = null;
    private ArrayList<Item> lData = null;
    private Context mContext;
    private ExpandableListView exlist_lol;
    private MyBaseExpandableListAdapter myAdapter = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityCollector.addActivity(this);
        setContentView(R.layout.activity_setting);
        mContext = SettingActivity.this;
        exlist_lol = (ExpandableListView) findViewById(R.id.exlist_lol);
        final TextView category = (TextView) findViewById(R.id.category);
        final TextView difficulty = (TextView) findViewById(R.id.difficulty);
        final TextView question_type = (TextView) findViewById(R.id.question_type);
        //数据准备
        gData = new ArrayList<Group>();
        iData = new ArrayList<ArrayList<Item>>();
        gData.add(new Group("Category"));
        gData.add(new Group("Difficulty"));
        gData.add(new Group("Question Type"));

        lData = new ArrayList<Item>();

        //Category
        lData.add(new Item(R.mipmap.iv_lol_icon3,"General Knowledge"));
        lData.add(new Item(R.mipmap.iv_lol_icon4,"Entertainment: Books"));
        lData.add(new Item(R.mipmap.iv_lol_icon13,"Entertainment: Film"));
        lData.add(new Item(R.mipmap.iv_lol_icon14,"Entertainment: Music"));
        lData.add(new Item(R.mipmap.iv_lol_icon9, "Entertainment: Musicals & Theatres"));
        lData.add(new Item(R.mipmap.iv_lol_icon11, "Entertainment: Television"));
        lData.add(new Item(R.mipmap.iv_lol_icon6, "Entertainment: Video Games"));
        lData.add(new Item(R.mipmap.iv_lol_icon10, "Entertainment: Board Games"));
        lData.add(new Item(R.mipmap.iv_lol_icon12, "Entertainment: Science & Nature"));
        iData.add(lData);
        //Difficulty
        lData = new ArrayList<Item>();
        lData.add(new Item(R.mipmap.iv_lol_icon1, "medium"));
        lData.add(new Item(R.mipmap.iv_lol_icon7, "easy"));
        lData.add(new Item(R.mipmap.iv_lol_icon8, "hard"));
        iData.add(lData);
        //Boolern Or Multiple
        lData = new ArrayList<Item>();
        lData.add(new Item(R.mipmap.iv_lol_icon2, "multiple"));
        lData.add(new Item(R.mipmap.iv_lol_icon5, "boolean"));

        iData.add(lData);

        myAdapter = new MyBaseExpandableListAdapter(gData,iData,mContext);
        exlist_lol.setAdapter(myAdapter);
        Button button = (Button) findViewById(R.id.verify);

        //为列表设置点击事件
        exlist_lol.setOnChildClickListener(new ExpandableListView.OnChildClickListener() {
            @Override
            public boolean onChildClick(ExpandableListView parent, View v, int groupPosition, int childPosition, long id) {
//                Toast.makeText(mContext, "你点击了：" + iData.get(groupPosition).get(childPosition).getiName(), Toast.LENGTH_SHORT).show();
                switch (groupPosition) {
                    case 0:
                        category.setText(iData.get(groupPosition).get(childPosition).getiName());
                        break;
                    case 1:
                        difficulty.setText(iData.get(groupPosition).get(childPosition).getiName());
                        break;
                    case 2:
                        question_type.setText(iData.get(groupPosition).get(childPosition).getiName());
                        break;
                }
                return true;
            }
        });
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(SettingActivity.this, MainActivity.class);
                Bundle bundle = new Bundle();//该类用作携带数据
                bundle.putString("difficulty", difficulty.getText().toString());
                bundle.putString("question_type", question_type.getText().toString());
                int category = 9;
                switch (difficulty.getText().toString()) {
                    case "General Knowledge":
                        category = 9;
                        break;
                    case "Entertainment: Books":
                        category = 10;
                        break;
                    case "Entertainment: Film":
                        category = 11;
                        break;
                    case "Entertainment: Music":
                        category = 12;
                        break;
                }
                bundle.putInt("category", category);
                intent.putExtras(bundle);//附带上额外的数据
//                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                intent.setFlags(0);
                startActivity(intent);
            }
        });

    }
}
