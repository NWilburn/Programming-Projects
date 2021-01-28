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
import java.sql.Date;
import java.sql.Timestamp;
import java.util.Arrays;
public class Reservations {
    
    private static Connection connection;
    private static PreparedStatement addReservation;
    private static PreparedStatement getReservationList;
    private static PreparedStatement getReservedRoomsList;
    private static String assignedRoom;
    private static ResultSet resultSet;
    private static Timestamp reservationTimestamp;
    private static PreparedStatement cancelReservation;
    private static PreparedStatement getReservationsByFaculty;
    
    public static ArrayList<ArrayList<String>> getReservationsByDate(Object date){
        connection = DBConnection.getConnection();
        ArrayList<ArrayList<String>> reservationsByDate = new ArrayList<ArrayList<String>>();
        try{
            getReservationList = connection.prepareStatement("select faculty, room, date from reservations order by date");
            resultSet = getReservationList.executeQuery();
            
            while(resultSet.next()){
                if (date.toString().equals(resultSet.getString(3))){
                    reservationsByDate.add(new ArrayList<String>(Arrays.asList(resultSet.getString(1), resultSet.getString(2))));
                }
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return reservationsByDate;
    }
    public static ArrayList<ArrayList<String>> getRoomsReservedByDate(){
        connection = DBConnection.getConnection();
        ArrayList<ArrayList<String>> reservedRooms = new ArrayList<ArrayList<String>>();
        try{
            getReservedRoomsList = connection.prepareStatement("select room, date from reservations order by date");
            resultSet = getReservedRoomsList.executeQuery();
            
            while (resultSet.next()){
                reservedRooms.add(new ArrayList<String>(Arrays.asList(resultSet.getString(1), resultSet.getString(2))));
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return reservedRooms;
    }
    public static ArrayList<String> getReservationsByFaculty(Object date){
        connection = DBConnection.getConnection();
        ArrayList<String> reservationsByFaculty = new ArrayList<String>();
        try{
            getReservationsByFaculty = connection.prepareStatement("select faculty, date from reservations order by date");
            resultSet = getReservationsByFaculty.executeQuery();
            
            while (resultSet.next()){
                if (date.toString().equals(resultSet.getString(2))){
                    reservationsByFaculty.add(resultSet.getString(1));
                }
            }           
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return reservationsByFaculty;
    }
    public static String cancelReservation(Object faculty, Object date){
        connection = DBConnection.getConnection();
        ArrayList<String> reservedRooms = getReservationsByFaculty(date);
        ArrayList<String> waitlistRooms = Waitlist.getWaitlistByFaculty(date);
        try{
            if (reservedRooms.contains(faculty.toString())){
                cancelReservation = connection.prepareStatement("delete from reservations where faculty = ? and date = ?");
                cancelReservation.setString(1, faculty.toString());
                cancelReservation.setDate(2, Date.valueOf(date.toString()));
                cancelReservation.executeUpdate();
                Waitlist.checkIfMoveOffWaitlist();
            }
            else if (waitlistRooms.contains(faculty.toString())){
                cancelReservation = connection.prepareStatement("delete from waitlist where faculty = ? and date = ?");
                cancelReservation.setString(1, faculty.toString());
                cancelReservation.setDate(2, Date.valueOf(date.toString()));
                cancelReservation.executeUpdate();
            }
            else{
                return "'s reservation does not exist.";
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return "'s reservation has been cancelled.";
    }
    public static String makeReservation(Object faculty, Object date, String seats){
        connection = DBConnection.getConnection();
        for (String u : getReservationsByFaculty(date)){
            if (faculty.toString().equals(u)){
                return " already has a reservation for this date.";
            }
        }
        ArrayList<ArrayList<String>> alreadyReservedRooms = getRoomsReservedByDate();      
        try{
            reservationTimestamp = new Timestamp(System.currentTimeMillis());
            assignedRoom = "None";
            for (ArrayList<String> x : RoomQueries.getAllPossibleRooms()){
                if (Integer.parseInt(seats) <= Integer.parseInt(x.get(1)) && alreadyReservedRooms.contains(new ArrayList<String>(Arrays.asList(x.get(0), date.toString()))) == false){
                    assignedRoom = x.get(0);
                    break;
                }
            }
            if (assignedRoom.equals("None")){
                return Waitlist.addWaitlistEntry(faculty.toString(), Date.valueOf(date.toString()), Integer.parseInt(seats), reservationTimestamp);
            }
            
            addReservation = connection.prepareStatement("insert into reservations (faculty, date, room, seats, timestamp) values (?,?,?,?,?)");
            addReservation.setString(1, faculty.toString());
            addReservation.setDate(2, Date.valueOf(date.toString()));
            addReservation.setString(3, assignedRoom);
            addReservation.setInt(4, Integer.parseInt(seats));
            addReservation.setTimestamp(5, reservationTimestamp);
            addReservation.executeUpdate();
        }
        
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return "'s reservation for Room " + assignedRoom + " on " + date.toString() + " has been made.";
    }
}
