/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package java2ddrawingapplication;

import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.Paint;
import java.awt.Point;
import java.awt.Stroke;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JColorChooser;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;


/**
 *
 * @author acv
 */
public class DrawingApplicationFrame extends JFrame
{
    JPanel topPanel = new JPanel(new GridLayout(2, 1));
    JPanel firstLine = new JPanel();
    JButton undoButton = new JButton("Undo");
    JButton clearButton = new JButton("Clear");
    String[] shapesString = {"Line", "Oval", "Rectangle"};
    JLabel shapeLabel = new JLabel("Shape:");
    JComboBox shapeBox = new JComboBox(shapesString);
    JCheckBox filledCheck = new JCheckBox("Filled");
    JPanel secondLine = new JPanel();
    JCheckBox useGradientCheck = new JCheckBox("Use Gradient");
    JButton firstColor = new JButton("1st Color");
    JColorChooser firstColorChoose = new JColorChooser(Color.RED);
    Color colorOne = firstColorChoose.getColor();
    JButton secondColor = new JButton("2nd Color");
    JColorChooser secondColorChoose = new JColorChooser(Color.RED);
    Color colorTwo = secondColorChoose.getColor();
    Paint paintColor;
    JLabel lineWidth = new JLabel("Line Width:");
    JTextField lineWidthInput = new JTextField("10", 2);
    JLabel dashLengthLabel = new JLabel("Dash Length:");
    JTextField dashLengthInput = new JTextField("15", 2);
    JCheckBox dashedCheck = new JCheckBox("Dashed");
    DrawPanel drawPanel = new DrawPanel();
    JLabel statusLabel = new JLabel("0, 0");
    MyShapes currentShape;
    ArrayList<MyShapes> shapes = new ArrayList<MyShapes>();
    Point pntA;
    Stroke stroke;

    public DrawingApplicationFrame()
    {
        firstLine.add(undoButton);
        firstLine.add(clearButton);
        firstLine.add(shapeLabel);
        firstLine.add(shapeBox);
        firstLine.add(filledCheck);
        secondLine.add(useGradientCheck);
        secondLine.add(firstColor);
        secondLine.add(secondColor);
        secondLine.add(lineWidth);
        secondLine.add(lineWidthInput);
        secondLine.add(dashLengthLabel);
        secondLine.add(dashLengthInput);
        secondLine.add(dashedCheck);
        topPanel.add(firstLine);
        topPanel.add(secondLine);
        drawPanel.setBackground(Color.white);
        
        firstColor.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent event){
                colorOne = JColorChooser.showDialog(topPanel, "Choose First Color", Color.RED);
            }
        });
        secondColor.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent event){
                colorTwo = JColorChooser.showDialog(topPanel, "Choose Second Color", Color.RED);
            }
        });
        
        undoButton.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent event){
                if (shapes.size() > 0){
                    shapes.remove(shapes.size() - 1);
                    repaint();
                }
            }
        });
        
        clearButton.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent event){
                shapes = new ArrayList<MyShapes>();
                repaint();
            }
        });
    }

    private class DrawPanel extends JPanel
    {

        public DrawPanel()
        {
            addMouseMotionListener(new MouseHandler());
            addMouseListener(new MouseHandler());
        }
        @Override
        public void paintComponent(Graphics g)
        {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;
            
            for (MyShapes i: shapes){
                i.draw(g2d);
            }
        }


        private class MouseHandler extends MouseAdapter implements MouseMotionListener
        {
            @Override
            public void mousePressed(MouseEvent event)
            {
                if (useGradientCheck.isSelected()){
                    paintColor = new GradientPaint(0, 0, colorOne, 50, 50, colorTwo, true);
                }
                else{
                    paintColor = colorOne;
                }
                if (dashedCheck.isSelected()){
                    float[] dashLength = {Float.parseFloat(dashLengthInput.getText())};
                    stroke = new BasicStroke(Float.parseFloat(lineWidthInput.getText()), BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND, 10, dashLength, 0);
                } 
                else{
                    stroke = new BasicStroke(Float.parseFloat(lineWidthInput.getText()), BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND);
                }
                pntA = new Point(event.getX(), event.getY());
                if (shapeBox.getSelectedItem() == "Line"){
                    currentShape = new MyLine(pntA, pntA, paintColor, stroke);
                }
                else if (shapeBox.getSelectedItem() == "Oval"){
                    currentShape = new MyOval(pntA, pntA, paintColor, stroke, filledCheck.isSelected());
                }
                else if (shapeBox.getSelectedItem() == "Rectangle"){
                    currentShape = new MyRectangle(pntA, pntA, paintColor, stroke, filledCheck.isSelected());
                }
                shapes.add(currentShape);
                repaint();
            }
            @Override
            public void mouseReleased(MouseEvent event)
            {
            }

            @Override
            public void mouseDragged(MouseEvent event)
            {
                statusLabel.setText(String.format("%d, %d", event.getX(), event.getY()));
                currentShape.setEndPoint(new Point(event.getX(), event.getY()));
                repaint();
            }

            @Override
            public void mouseMoved(MouseEvent event)
            {
                statusLabel.setText(String.format("%d, %d", event.getX(), event.getY()));
            }
        }

    }
}
