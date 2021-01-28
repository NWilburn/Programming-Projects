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
/**
 *
 * @author nwilb
 */
public class Dates {
    private static Connection connection;
    private static PreparedStatement addDate;
    private static PreparedStatement getDateList;
    private static ResultSet resultSet;
    
    public static String addDate(Date date){
        connection = DBConnection.getConnection();
        
        try{
            addDate = connection.prepareStatement("insert into dates (date) values (?)");
            addDate.setDate(1, date);
            addDate.executeUpdate();
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return date.toString() + " has been added.";
    }
    
    public static ArrayList<Date> getAllDates(){
        connection = DBConnection.getConnection();
        ArrayList<Date> dates = new ArrayList<Date>(); 
        
        try{
            getDateList = connection.prepareStatement("select date from dates order by date");
            resultSet = getDateList.executeQuery();
            
            while(resultSet.next()){
                dates.add(resultSet.getDate(1));
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return dates;
    }
}
