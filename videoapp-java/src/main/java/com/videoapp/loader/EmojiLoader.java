//package com.videoapp.loader;
//
//import java.io.File;
//import java.io.FileInputStream;
//import java.io.IOException;
//import java.sql.Connection;
//import java.sql.DriverManager;
//import java.sql.PreparedStatement;
//import java.sql.SQLException;
//
//public class EmojiLoader {
//
//    public static void main(String[] args) {
//        // JDBC connection parameters
//        String url = "jdbc:mysql://localhost:3306/automation_video_data";
//        String username = "root";
//        String password = "root";
//
//        // Folder containing emojis
//        String folderPath = "G:\\Automation_Video_Project\\videoapp\\Data\\emojies";
//
//        // JDBC connection
//        try (Connection conn = DriverManager.getConnection(url, username, password)) {
//            // Iterate over files in the folder
//            File folder = new File(folderPath);
//            File[] files = folder.listFiles();
//            if (files != null) {
//                for (File file : files) {
//                    // Insert each emoji into the database
//                    insertEmoji(conn, file.getName(), file);
//                }
//            }
//        } catch (SQLException | IOException e) {
//            e.printStackTrace();
//        }
//    }
//
//    private static void insertEmoji(Connection conn, String emojiName, File emojiFile) throws SQLException, IOException {
//        // SQL query to insert emoji into database
//        String sql = "INSERT INTO emojis (name, emoji, created_by, created_date, updated_by, updated_date) VALUES (?, ?, 'system', CURRENT_TIMESTAMP, 'system', NULL)";
//
//        try (PreparedStatement statement = conn.prepareStatement(sql)) {
//            // Set parameters
//            statement.setString(1, emojiName);
//            FileInputStream inputStream = new FileInputStream(emojiFile);
//            statement.setBinaryStream(2, inputStream);
//
//            // Execute query
//            statement.executeUpdate();
//        }
//    }
//}
