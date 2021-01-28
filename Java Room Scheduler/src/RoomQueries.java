/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;


public class RoomQueries {
    private static Connection connection;
    private static PreparedStatement getRoomsList;
    private static ResultSet resultSet;
    private static PreparedStatement addRoomCmd;
    private static PreparedStatement dropRoomCmd;
    private static PreparedStatement getAllRoomsList;
    
    public static ArrayList<ArrayList<String>> getAllPossibleRooms(){
        connection = DBConnection.getConnection();
        ArrayList<ArrayList<String>> rooms = new ArrayList<ArrayList<String>>();
        
        try{
            getRoomsList = connection.prepareStatement("select name, seats from rooms order by seats");
            resultSet = getRoomsList.executeQuery();
            
            while (resultSet.next()){
                rooms.add(new ArrayList<String>(Arrays.asList(resultSet.getString(1), resultSet.getString(2))));
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return rooms;
    }
    public static ArrayList<String> getAllRooms(){
        connection = DBConnection.getConnection();
        ArrayList<String> allRooms = new ArrayList<String>();
        try{
            getAllRoomsList = connection.prepareStatement("select name from rooms order by seats");
            resultSet = getAllRoomsList.executeQuery();
            
            while (resultSet.next()){
                allRooms.add(resultSet.getString(1));
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return allRooms;
    }
    public static String addRoom(String name, String seats){
        connection = DBConnection.getConnection();
        
        try{
            addRoomCmd = connection.prepareStatement("insert into rooms (name, seats) values (?, ?)");
            addRoomCmd.setString(1, name);
            addRoomCmd.setInt(2, Integer.parseInt(seats));
            addRoomCmd.executeUpdate();
            
            Waitlist.checkIfMoveOffWaitlist();
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return "Room " + name + " with " + seats + " seats has been added to rooms.";
    }
    public static String dropRoom(String name){
        connection = DBConnection.getConnection();
        
        try{
            dropRoomCmd = connection.prepareStatement("delete from rooms where name = ?");
            dropRoomCmd.setString(1, name);
            dropRoomCmd.executeUpdate();
            
            dropRoomCmd = connection.prepareStatement("select faculty, room, date, seats from reservations order by date");
            resultSet = dropRoomCmd.executeQuery();
            
            while (resultSet.next()){
                if (resultSet.getString(2).equals(name)){
                    Reservations.cancelReservation(resultSet.getString(1), resultSet.getString(3));
                    Reservations.makeReservation(resultSet.getString(1), resultSet.getString(3), resultSet.getString(4));
                }
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return "Room " + name + " has been dropped.";
    }
}
