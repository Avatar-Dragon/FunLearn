package com.fun.funlearn;

/**
 * Created by hasee on 2017/6/26.
 */

public class User {
    private int total_correct;
    private int total_incorrect;
    private int total_number;
    private String password;
    private String username;
    private int add_c;
    private int add_in;
    private User(){
        add_c = 0;
        add_in = 0;
    }

    private static User singleton;

    public  static User getinstance() {
        if (singleton == null) {
            singleton = new User();
        }
        return singleton;
    }
    public int getTotal_correct() {
        return total_correct;
    }

    public int getTotal_incorrect() {
        return total_incorrect;
    }

    public int getTotal_number() {
        return total_correct+total_incorrect;
    }

    public void add_correct() {
        total_correct++;
//        return ++add_c;
    }
    public void add_incorrect() {
        total_incorrect++;
//        return ++add_in;
    }
    public void ResetAdd_c () {
        add_c = 0;
    }
    public void ResetAdd_inc () {
        add_in = 0;
    }
    public void setTotal_correct(int c) {
        total_correct = c;
    }
    public void setTotal_incorrect(int i) {
        total_incorrect = i;
    }
    public String getPassword() {
        return password;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String u) {
        username = u;
    }

    public void setPassword(String p) {
        password = p;
    }


}
