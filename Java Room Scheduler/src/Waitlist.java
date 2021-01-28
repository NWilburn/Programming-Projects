/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.sql.Array;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.sql.Date;
import java.sql.Timestamp;
import java.util.Arrays;

public class Waitlist {
    private static Connection connection;
    private static PreparedStatement addToWaitList;
    private static PreparedStatement getWaitlistList;
    private static ResultSet resultSet;
    private static PreparedStatement getWaitlistByFaculty;
    private static PreparedStatement checkWaitlist;
    
    public static ArrayList<ArrayList<String>> getWaitlistByDate(){
        connection = DBConnection.getConnection();
        ArrayList<ArrayList<String>> waitlistByDate = new ArrayList<ArrayList<String>>();
        try{
            getWaitlistList = connection.prepareStatement("select faculty, date, seats from waitlist order by date");
            resultSet = getWaitlistList.executeQuery();
            
            while(resultSet.next()){
                waitlistByDate.add(new ArrayList<String>(Arrays.asList(resultSet.getString(1), resultSet.getString(2), resultSet.getString(3))));
            }
        }
                catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return waitlistByDate;
    }
    public static ArrayList<String> getWaitlistByFaculty(Object date){
        connection = DBConnection.getConnection();
        ArrayList<String> waitlistByFaculty = new ArrayList<String>();
        try{
            getWaitlistByFaculty = connection.prepareStatement("select faculty, date from waitlist order by date");
            resultSet = getWaitlistByFaculty.executeQuery();

            while (resultSet.next()){
                if (date.toString().equals(resultSet.getString(2))){
                waitlistByFaculty.add(resultSet.getString(1));
                }
            }           
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return waitlistByFaculty;
    }
    public static void checkIfMoveOffWaitlist(){
        connection = DBConnection.getConnection();
        ArrayList<ArrayList<String>> alreadyReservedRooms = Reservations.getRoomsReservedByDate();
        try{
            checkWaitlist = connection.prepareStatement("select faculty, date, seats from waitlist order by timestamp");
            resultSet = checkWaitlist.executeQuery();
            
            while(resultSet.next()){
                for (ArrayList<String> x : RoomQueries.getAllPossibleRooms()){
                    if (Integer.parseInt(resultSet.getString(3)) <= Integer.parseInt(x.get(1)) && alreadyReservedRooms.contains(new ArrayList<String>(Arrays.asList(x.get(0), resultSet.getString(2)))) == false){
                        Reservations.makeReservation(resultSet.getString(1), resultSet.getString(2), resultSet.getString(3));
                        checkWaitlist = connection.prepareStatement("delete from waitlist where faculty = ? and date = ?");
                        checkWaitlist.setString(1, resultSet.getString(1));
                        checkWaitlist.setDate(2, Date.valueOf(resultSet.getString(2)));
                        checkWaitlist.executeUpdate();
                        break;
                    }
                }
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
    }
    public static String addWaitlistEntry(String faculty, Date date, int seats, Timestamp timestamp){
        connection = DBConnection.getConnection();
        for (String p : getWaitlistByFaculty(date)){
            if (faculty.equals(p)){
                return " is already on Waitlist for this date.";
            }
        }
        try{
           addToWaitList = connection.prepareStatement("insert into waitlist (faculty, date, seats, timestamp) values (?, ?, ?, ?)"); 
           addToWaitList.setString(1, faculty);
           addToWaitList.setDate(2, date);
           addToWaitList.setInt(3, seats);
           addToWaitList.setTimestamp(4, timestamp);
           addToWaitList.executeUpdate();
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return " has been put on Waitlist.";
    }
}
