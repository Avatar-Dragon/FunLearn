package com.fun.funlearn;

import org.json.JSONArray;

/**
 * Created by hasee on 2017/6/23.
 */

public class Question_info {
    private String category;
    private String type;
    private String difficulty;
    private String question;
    private String correct_answer;
    private JSONArray incorrect_answers;
//    private String[] incorrect_answers;
    public Question_info(String category, String type,String difficulty, String question,String correct_answer, JSONArray incorrect_answers1) {
        this.category = category;
        this.question = question;
        this.difficulty = difficulty;
        this.correct_answer = correct_answer;
        this.type = type;
        this.incorrect_answers = incorrect_answers1;
    }

    public String getCorrect_answer() {
        return correct_answer;
    }

    public String getType() {
        return type;
    }

    public String getQuestion() {
        return question;
    }

    public String getDifficulty() {
        return difficulty;
    }

    public String getCategory() {
        return category;
    }

    public JSONArray getIncorrect_answers() {
        return incorrect_answers;
    }
}
