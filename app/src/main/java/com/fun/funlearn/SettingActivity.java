package com.fun.funlearn;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
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
        setContentView(R.layout.activity_setting);
        mContext = SettingActivity.this;
        exlist_lol = (ExpandableListView) findViewById(R.id.exlist_lol);
        final TextView category = (TextView) findViewById(R.id.category);
        final TextView difficulty = (TextView) findViewById(R.id.difficulty);
        final TextView question_typy = (TextView) findViewById(R.id.question_type);
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
        lData.add(new Item(R.mipmap.iv_lol_icon1, "mediu"));
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
                        question_typy.setText(iData.get(groupPosition).get(childPosition).getiName());
                        break;
                }
                return true;
            }
        });


    }
}
