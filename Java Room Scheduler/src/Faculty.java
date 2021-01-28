
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author acv
 */
public class Faculty
{
    private static Connection connection;
    private static ArrayList<String> faculty = new ArrayList<String>();
    private static PreparedStatement addFaculty;
    private static PreparedStatement getFacultyList;
    private static ResultSet resultSet;
    private static String outcomeStatement;
    private static PreparedStatement getFacultyStatusList;
    
    public static String addFaculty(String name)
    {
        connection = DBConnection.getConnection();
        try
        {
            addFaculty = connection.prepareStatement("insert into faculty (name) values (?)");
            addFaculty.setString(1, name);
            try{
                addFaculty.executeUpdate();
                outcomeStatement = " was successfully added to Faculty";
            }
            catch(Exception e){
                outcomeStatement = " was unsuccessfully added to Faculty.";
            }
        }
        catch(SQLException sqlException)
        {
            sqlException.printStackTrace();
        }
        return outcomeStatement;
    }
    
    public static ArrayList<String> getFacultyList()
    {
        connection = DBConnection.getConnection();
        ArrayList<String> faculty = new ArrayList<String>();
        try
        {
            getFacultyList = connection.prepareStatement("select name from faculty order by name");
            resultSet = getFacultyList.executeQuery();
            
            while(resultSet.next())
            {
                faculty.add(resultSet.getString(1));
            }
        }
        catch(SQLException sqlException)
        {
            sqlException.printStackTrace();
        }
        return faculty;
        
    }
    
    public static ArrayList<ArrayList<String>> getFacultyStatus(Object faculty){
        connection = DBConnection.getConnection();
        ArrayList<ArrayList<String>> facultyStatusList = new ArrayList<ArrayList<String>>();
        try{
            getFacultyStatusList = connection.prepareStatement("select faculty, room, date from reservations order by date");
            resultSet = getFacultyStatusList.executeQuery();
            
            while (resultSet.next()){
                if (resultSet.getString(1).equals(faculty.toString())){
                    facultyStatusList.add(new ArrayList<String>(Arrays.asList(resultSet.getString(2), resultSet.getString(3))));
                }
            }
        }
        catch(SQLException sqlException){
            sqlException.printStackTrace();
        }
        return facultyStatusList;
    }
}
